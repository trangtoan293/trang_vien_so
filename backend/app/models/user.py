"""
User and UserSession models
Authentication and user management
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB, INET
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class User(Base):
    """User model matching PostgreSQL users table"""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Personal information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    avatar = Column(String(500))
    
    # Email verification
    email_verified = Column(Boolean, default=False)
    email_verified_at = Column(DateTime(timezone=False))
    
    # Localization
    language = Column(String(10), default='vi')
    timezone = Column(String(50), default='Asia/Ho_Chi_Minh')
    
    # Preferences (JSON)
    notification_preferences = Column(
        JSONB, 
        default={"push": True, "email": True}
    )
    privacy_settings = Column(
        JSONB,
        default={"profile_visibility": "family"}
    )
    
    # Timestamps
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    last_login_at = Column(DateTime(timezone=False))
    
    # Relationships
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    created_profiles = relationship("DeceasedProfile", foreign_keys="DeceasedProfile.created_by", back_populates="creator")
    family_memberships = relationship("FamilyMember", foreign_keys="FamilyMember.user_id", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.first_name} {self.last_name})>"
    
    @property
    def full_name(self):
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"


class UserSession(Base):
    """User session model for authentication tokens"""
    
    __tablename__ = "user_sessions"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign key
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Token information
    token_hash = Column(String(255), unique=True, nullable=False)
    refresh_token_hash = Column(String(255))
    
    # Session metadata
    ip_address = Column(INET)
    user_agent = Column(Text)
    device_info = Column(JSONB)
    
    # Session status
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    expires_at = Column(DateTime(timezone=False), nullable=False)
    last_used_at = Column(DateTime(timezone=False), server_default=func.now())
    is_active = Column(Boolean, default=True, index=True)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    
    def __repr__(self):
        return f"<UserSession(id={self.id}, user_id={self.user_id}, active={self.is_active})>"