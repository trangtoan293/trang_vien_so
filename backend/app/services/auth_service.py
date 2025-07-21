"""
Authentication service
User authentication, session management, and JWT token handling
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
import uuid
import hashlib
import secrets
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from fastapi import HTTPException, status

from app.models.user import User, UserSession
from app.core.security import verify_password, hash_password, generate_tokens, verify_token
from app.core.config import settings
from app.schemas.user import UserRegisterRequest, UserLoginRequest
from app.schemas.auth import LoginResponse, TokenResponse


class AuthService:
    """Authentication service for user management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def register_user(self, user_data: UserRegisterRequest, ip_address: str = None, user_agent: str = None) -> LoginResponse:
        """Register a new user and create session"""
        
        # Check if user already exists
        existing_user = await self.db.execute(
            select(User).where(User.email == user_data.email)
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        
        # Create new user
        password_hash = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            password_hash=password_hash,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=user_data.phone_number,
            language=user_data.language or "vi",
            timezone=user_data.timezone or "Asia/Ho_Chi_Minh"
        )
        
        self.db.add(new_user)
        await self.db.flush()  # Get the user ID
        
        # Create session and tokens
        tokens, session = await self._create_user_session(
            new_user, ip_address, user_agent, remember_me=False
        )
        
        await self.db.commit()
        
        # Refresh user object to get timestamps
        await self.db.refresh(new_user)
        
        # Create response
        from app.schemas.user import UserResponse
        user_response = UserResponse(
            id=new_user.id,
            email=new_user.email,
            first_name=new_user.first_name,
            last_name=new_user.last_name,
            phone_number=new_user.phone_number,
            avatar=new_user.avatar,
            email_verified=new_user.email_verified,
            email_verified_at=new_user.email_verified_at,
            language=new_user.language,
            timezone=new_user.timezone,
            notification_preferences=new_user.notification_preferences,
            privacy_settings=new_user.privacy_settings,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
            last_login_at=new_user.last_login_at
        )
        
        return LoginResponse(
            success=True,
            message="Registration successful",
            user=user_response,
            tokens=tokens,
            session_id=session.id
        )
    
    async def login_user(self, login_data: UserLoginRequest, ip_address: str = None, user_agent: str = None) -> LoginResponse:
        """Authenticate user and create session"""
        
        # Find user by email
        result = await self.db.execute(
            select(User).where(User.email == login_data.email)
        )
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        
        # Create session and tokens
        tokens, session = await self._create_user_session(
            user, ip_address, user_agent, login_data.remember_me
        )
        
        await self.db.commit()
        
        # Refresh user object to get updated timestamps
        await self.db.refresh(user)
        
        # Create response
        from app.schemas.user import UserResponse
        user_response = UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            avatar=user.avatar,
            email_verified=user.email_verified,
            email_verified_at=user.email_verified_at,
            language=user.language,
            timezone=user.timezone,
            notification_preferences=user.notification_preferences,
            privacy_settings=user.privacy_settings,
            created_at=user.created_at,
            updated_at=user.updated_at,
            last_login_at=user.last_login_at
        )
        
        return LoginResponse(
            success=True,
            message="Login successful",
            user=user_response,
            tokens=tokens,
            session_id=session.id
        )
    
    async def refresh_token(self, refresh_token: str, ip_address: str = None) -> TokenResponse:
        """Refresh access token using refresh token"""
        
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        session_id = payload.get("session_id")
        if not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        # Find active session
        result = await self.db.execute(
            select(UserSession).where(
                and_(
                    UserSession.id == session_id,
                    UserSession.is_active == True,
                    UserSession.expires_at > datetime.utcnow()
                )
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found or expired"
            )
        
        # Generate new tokens
        user_id = session.user_id
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        access_token, new_refresh_token = generate_tokens(
            user_id=user_id,
            session_id=session.id,
            access_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_expire_days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        
        # Update session
        session.refresh_token_hash = hashlib.sha256(new_refresh_token.encode()).hexdigest()
        session.last_used_at = datetime.utcnow()
        if ip_address:
            session.ip_address = ip_address
        
        await self.db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=expires_in,
            expires_at=expires_at
        )
    
    async def logout_user(self, session_id: uuid.UUID) -> bool:
        """Logout user by deactivating session"""
        
        result = await self.db.execute(
            select(UserSession).where(UserSession.id == session_id)
        )
        session = result.scalar_one_or_none()
        
        if session:
            session.is_active = False
            await self.db.commit()
            return True
        
        return False
    
    async def logout_all_sessions(self, user_id: uuid.UUID) -> int:
        """Logout user from all sessions"""
        
        result = await self.db.execute(
            select(UserSession).where(
                and_(
                    UserSession.user_id == user_id,
                    UserSession.is_active == True
                )
            )
        )
        sessions = result.scalars().all()
        
        for session in sessions:
            session.is_active = False
        
        await self.db.commit()
        return len(sessions)
    
    async def validate_session(self, session_id: uuid.UUID) -> Optional[UserSession]:
        """Validate and return active session"""
        
        result = await self.db.execute(
            select(UserSession).where(
                and_(
                    UserSession.id == session_id,
                    UserSession.is_active == True,
                    UserSession.expires_at > datetime.utcnow()
                )
            )
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def _create_user_session(
        self, 
        user: User, 
        ip_address: str = None, 
        user_agent: str = None, 
        remember_me: bool = False
    ) -> Tuple[TokenResponse, UserSession]:
        """Create user session and generate tokens"""
        
        # Calculate expiration times
        refresh_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
        if remember_me:
            refresh_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS_EXTENDED
        
        expires_at = datetime.utcnow() + timedelta(days=refresh_expire_days)
        
        # Create session with placeholder token hash
        session = UserSession(
            user_id=user.id,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
            device_info=self._parse_device_info(user_agent) if user_agent else None,
            token_hash="placeholder"  # Temporary value to satisfy constraint
        )
        
        self.db.add(session)
        await self.db.flush()  # Get session ID
        
        # Generate tokens
        access_token, refresh_token = generate_tokens(
            user_id=user.id,
            session_id=session.id,
            access_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_expire_days=refresh_expire_days
        )
        
        # Store actual token hashes
        session.token_hash = hashlib.sha256(access_token.encode()).hexdigest()
        session.refresh_token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        
        # Create token response
        expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        token_expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        
        tokens = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=expires_in,
            expires_at=token_expires_at
        )
        
        return tokens, session
    
    def _parse_device_info(self, user_agent: str) -> Dict[str, Any]:
        """Parse device information from user agent"""
        # Simple device info parsing - could be enhanced with user-agents library
        device_info = {"user_agent": user_agent}
        
        if "Mobile" in user_agent:
            device_info["device_type"] = "mobile"
        elif "Tablet" in user_agent:
            device_info["device_type"] = "tablet"
        else:
            device_info["device_type"] = "desktop"
        
        if "Chrome" in user_agent:
            device_info["browser"] = "chrome"
        elif "Firefox" in user_agent:
            device_info["browser"] = "firefox"
        elif "Safari" in user_agent:
            device_info["browser"] = "safari"
        elif "Edge" in user_agent:
            device_info["browser"] = "edge"
        else:
            device_info["browser"] = "unknown"
        
        return device_info