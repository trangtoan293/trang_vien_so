"""
Authentication middleware and dependencies
JWT token validation and user authentication
"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from datetime import datetime
import uuid

from app.core.database import get_db
from app.core.security import verify_token
from app.models.user import User, UserSession
from app.services.auth_service import AuthService


# HTTP Bearer token scheme
security = HTTPBearer()


class AuthenticationError(HTTPException):
    """Custom authentication error"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    """
    token = credentials.credentials
    
    # Verify JWT token
    payload = verify_token(token, token_type="access")
    if not payload:
        raise AuthenticationError("Invalid or expired token")
    
    # Extract user and session IDs
    user_id = payload.get("user_id")
    session_id = payload.get("session_id")
    
    if not user_id or not session_id:
        raise AuthenticationError("Invalid token payload")
    
    # Create auth service
    auth_service = AuthService(db)
    
    # Validate session
    session = await auth_service.validate_session(uuid.UUID(session_id))
    if not session:
        raise AuthenticationError("Session not found or expired")
    
    # Get user
    user = await auth_service.get_user_by_id(uuid.UUID(user_id))
    if not user:
        raise AuthenticationError("User not found")
    
    # Update session last used time
    session.last_used_at = datetime.utcnow()
    
    # Store user and session in request state for later use
    request.state.current_user = user
    request.state.current_session = session
    
    await db.commit()
    
    return user


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user if authenticated, otherwise return None
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(request, credentials, db)
    except HTTPException:
        return None


async def get_current_session(request: Request) -> UserSession:
    """
    Get current user session from request state
    Must be used after get_current_user dependency
    """
    if not hasattr(request.state, 'current_session'):
        raise AuthenticationError("No active session found")
    
    return request.state.current_session


def require_permissions(permissions: list):
    """
    Decorator to require specific permissions
    """
    def permission_checker(current_user: User = Depends(get_current_user)):
        # For now, all authenticated users have basic permissions
        # This can be extended with role-based access control
        return current_user
    
    return permission_checker


def require_email_verified():
    """
    Require user to have verified email
    """
    def email_verification_checker(current_user: User = Depends(get_current_user)):
        if not current_user.email_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Email verification required"
            )
        return current_user
    
    return email_verification_checker


# Common dependencies
CurrentUser = Depends(get_current_user)
CurrentUserOptional = Depends(get_current_user_optional)
CurrentSession = Depends(get_current_session)
VerifiedUser = Depends(require_email_verified())


# Utility functions
def get_client_ip(request: Request) -> str:
    """Get client IP address from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    return request.client.host if request.client else "unknown"


def get_user_agent(request: Request) -> str:
    """Get user agent from request"""
    return request.headers.get("User-Agent", "unknown")