"""
Security utilities for JWT tokens and password hashing
Compatible with existing Node.js implementation
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import hashlib
import secrets

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.core.config import settings


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    Compatible with Node.js bcryptjs implementation
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt
    Compatible with Node.js bcryptjs implementation
    """
    return pwd_context.hash(password, rounds=settings.BCRYPT_ROUNDS)


def hash_password(password: str) -> str:
    """
    Alias for get_password_hash for backward compatibility
    """
    return get_password_hash(password)


def hash_token(token: str) -> str:
    """
    Hash a token using SHA-256 for session storage
    Compatible with Node.js crypto.createHash implementation
    """
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token
    Compatible with Node.js jsonwebtoken implementation
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY, 
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token with longer expiration
    """
    to_encode = data.copy()
    to_encode.update({"type": "refresh"})
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token
    Returns the token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Check token type for refresh tokens
        if token_type == "refresh":
            if payload.get("type") != "refresh":
                return None
        
        # Check if token is expired
        exp = payload.get("exp")
        if exp is None:
            return None
            
        if datetime.utcnow().timestamp() > exp:
            return None
            
        return payload
        
    except JWTError:
        return None


def generate_tokens(
    user_id: str, 
    session_id: str, 
    access_expire_minutes: int = None, 
    refresh_expire_days: int = None
) -> Tuple[str, str]:
    """
    Generate both access and refresh tokens for a user session
    Returns tuple of (access_token, refresh_token)
    """
    # Use provided expiration times or defaults
    if access_expire_minutes is None:
        access_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    if refresh_expire_days is None:
        refresh_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    # Create access token
    access_token_expires = timedelta(minutes=access_expire_minutes)
    access_token = create_access_token(
        data={
            "user_id": str(user_id),
            "session_id": str(session_id),
            "type": "access"
        }, 
        expires_delta=access_token_expires
    )
    
    # Create refresh token
    refresh_token_expires = timedelta(days=refresh_expire_days)
    refresh_token = create_refresh_token(
        data={
            "user_id": str(user_id),
            "session_id": str(session_id),
            "type": "refresh"
        }, 
        expires_delta=refresh_token_expires
    )
    
    return access_token, refresh_token


def generate_secure_token() -> str:
    """Generate a cryptographically secure random token"""
    return secrets.token_urlsafe(32)