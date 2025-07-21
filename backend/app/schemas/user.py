"""
User-related Pydantic schemas
Request/response models for user management
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime
import uuid


class UserRegisterRequest(BaseModel):
    """User registration request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="Password (8-128 characters)")
    first_name: str = Field(..., min_length=1, max_length=100, description="First name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Last name")
    phone_number: Optional[str] = Field(None, max_length=20, description="Phone number")
    language: Optional[str] = Field("vi", max_length=10, description="Preferred language")
    timezone: Optional[str] = Field("Asia/Ho_Chi_Minh", max_length=50, description="User timezone")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLoginRequest(BaseModel):
    """User login request schema"""
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")
    remember_me: Optional[bool] = Field(False, description="Extended session duration")


class UserProfileUpdate(BaseModel):
    """User profile update schema"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = Field(None, max_length=500)
    language: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=50)
    notification_preferences: Optional[Dict[str, Any]] = Field(None)
    privacy_settings: Optional[Dict[str, Any]] = Field(None)


class PasswordChangeRequest(BaseModel):
    """Password change request schema"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=128, description="New password")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserResponse(BaseModel):
    """User response schema"""
    id: uuid.UUID
    email: str
    first_name: str
    last_name: str
    phone_number: Optional[str]
    avatar: Optional[str]
    email_verified: bool
    email_verified_at: Optional[datetime]
    language: str
    timezone: str
    notification_preferences: Dict[str, Any]
    privacy_settings: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"


class UserSessionResponse(BaseModel):
    """User session response schema"""
    id: uuid.UUID
    user_id: uuid.UUID
    ip_address: Optional[str]
    user_agent: Optional[str]
    device_info: Optional[Dict[str, Any]]
    created_at: datetime
    expires_at: datetime
    last_used_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True