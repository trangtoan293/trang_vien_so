"""
Authentication-related Pydantic schemas
JWT tokens and authentication responses
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import uuid

from .user import UserResponse


class TokenResponse(BaseModel):
    """JWT token response schema"""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    expires_at: datetime = Field(..., description="Token expiration timestamp")


class RefreshTokenRequest(BaseModel):
    """Refresh token request schema"""
    refresh_token: str = Field(..., description="Valid refresh token")


class LoginResponse(BaseModel):
    """Login response schema"""
    success: bool = Field(True, description="Login success status")
    message: str = Field("Login successful", description="Response message")
    user: UserResponse = Field(..., description="User information")
    tokens: TokenResponse = Field(..., description="Authentication tokens")
    session_id: uuid.UUID = Field(..., description="Session identifier")
    
    class Config:
        from_attributes = True


class LogoutResponse(BaseModel):
    """Logout response schema"""
    success: bool = Field(True, description="Logout success status")
    message: str = Field("Logout successful", description="Response message")


class TokenValidationResponse(BaseModel):
    """Token validation response schema"""
    valid: bool = Field(..., description="Token validity status")
    user_id: Optional[uuid.UUID] = Field(None, description="User ID if token is valid")
    session_id: Optional[uuid.UUID] = Field(None, description="Session ID if token is valid")
    expires_at: Optional[datetime] = Field(None, description="Token expiration time")
    
    class Config:
        from_attributes = True