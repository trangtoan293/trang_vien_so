"""
Authentication router
User registration, login, logout, and token management
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_session, get_client_ip, get_user_agent
from app.services.auth_service import AuthService
from app.schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse
from app.schemas.auth import LoginResponse, TokenResponse, RefreshTokenRequest, LogoutResponse
from app.models.user import User, UserSession


router = APIRouter()


@router.post("/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    request: Request,
    user_data: UserRegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user account
    
    Creates a new user account and returns authentication tokens.
    """
    auth_service = AuthService(db)
    
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    try:
        response = await auth_service.register_user(user_data, ip_address, user_agent)
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=LoginResponse)
async def login_user(
    request: Request,
    login_data: UserLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    User login
    
    Authenticate user credentials and return access tokens.
    """
    auth_service = AuthService(db)
    
    ip_address = get_client_ip(request)
    user_agent = get_user_agent(request)
    
    try:
        response = await auth_service.login_user(login_data, ip_address, user_agent)
        return response
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Refresh access token
    
    Use a valid refresh token to get a new access token.
    """
    auth_service = AuthService(db)
    
    ip_address = get_client_ip(request)
    
    try:
        response = await auth_service.refresh_token(refresh_data.refresh_token, ip_address)
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout", response_model=LogoutResponse)
async def logout_user(
    current_session: UserSession = Depends(get_current_session),
    db: AsyncSession = Depends(get_db)
):
    """
    User logout
    
    Invalidate the current session and logout the user.
    """
    auth_service = AuthService(db)
    
    try:
        success = await auth_service.logout_user(current_session.id)
        if success:
            return LogoutResponse(
                success=True,
                message="Logout successful"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Logout failed"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.post("/logout-all", response_model=Dict[str, Any])
async def logout_all_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Logout from all sessions
    
    Invalidate all active sessions for the current user.
    """
    auth_service = AuthService(db)
    
    try:
        count = await auth_service.logout_all_sessions(current_user.id)
        return {
            "success": True,
            "message": f"Logged out from {count} sessions",
            "sessions_count": count
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout all failed"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information
    
    Returns the profile information of the authenticated user.
    """
    return UserResponse.from_orm(current_user)


@router.get("/verify-token")
async def verify_token(
    current_user: User = Depends(get_current_user),
    current_session: UserSession = Depends(get_current_session)
):
    """
    Verify token validity
    
    Check if the current token is valid and active.
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "session_id": current_session.id,
        "expires_at": current_session.expires_at,
        "last_used_at": current_session.last_used_at
    }


@router.get("/sessions")
async def get_user_sessions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's active sessions
    
    Returns list of active sessions for the current user.
    """
    from sqlalchemy import select, and_
    from datetime import datetime
    
    result = await db.execute(
        select(UserSession).where(
            and_(
                UserSession.user_id == current_user.id,
                UserSession.is_active == True,
                UserSession.expires_at > datetime.utcnow()
            )
        ).order_by(UserSession.last_used_at.desc())
    )
    sessions = result.scalars().all()
    
    session_list = []
    for session in sessions:
        session_list.append({
            "id": session.id,
            "ip_address": session.ip_address,
            "user_agent": session.user_agent,
            "device_info": session.device_info,
            "created_at": session.created_at,
            "last_used_at": session.last_used_at,
            "expires_at": session.expires_at,
            "is_current": False  # Will be enhanced in future versions
        })
    
    return {
        "sessions": session_list,
        "total": len(session_list)
    }


@router.get("/")
async def auth_status():
    """Authentication router status"""
    return {
        "message": "Authentication API is active",
        "version": "2.0.0",
        "endpoints": [
            "POST /register - User registration",
            "POST /login - User login", 
            "POST /refresh - Refresh access token",
            "POST /logout - User logout",
            "POST /logout-all - Logout from all sessions",
            "GET /me - Get current user info",
            "GET /verify-token - Verify token validity",
            "GET /sessions - Get user sessions"
        ]
    }