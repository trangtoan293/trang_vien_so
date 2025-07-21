"""
Family and invitation models
Family management and member relationships
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Family(Base):
    """Family model for grouping deceased profiles and members"""
    
    __tablename__ = "families"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information
    family_name = Column(String(200), nullable=False)
    description = Column(Text)
    
    # Audit fields
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", foreign_keys=[created_by])
    members = relationship("FamilyMember", back_populates="family", cascade="all, delete-orphan")
    deceased_profiles = relationship("DeceasedProfile", back_populates="family")
    invitations = relationship("Invitation", back_populates="family", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Family(id={self.id}, name={self.family_name})>"


class FamilyMember(Base):
    """Family member model for user-family relationships"""
    
    __tablename__ = "family_members"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    invited_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # Member status and role
    role = Column(String(20), nullable=False)  # admin, editor, viewer
    status = Column(String(20), nullable=False, default='pending', index=True)  # pending, active, inactive
    
    # Timestamps
    invited_at = Column(DateTime(timezone=False), server_default=func.now())
    joined_at = Column(DateTime(timezone=False))
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('family_id', 'user_id', name='family_members_family_id_user_id_key'),
        CheckConstraint(
            "role IN ('admin', 'editor', 'viewer')",
            name="family_members_role_check"
        ),
        CheckConstraint(
            "status IN ('pending', 'active', 'inactive')",
            name="family_members_status_check"
        ),
    )
    
    # Relationships
    family = relationship("Family", back_populates="members")
    user = relationship("User", foreign_keys=[user_id], back_populates="family_memberships")
    inviter = relationship("User", foreign_keys=[invited_by])
    
    def __repr__(self):
        return f"<FamilyMember(family_id={self.family_id}, user_id={self.user_id}, role={self.role}, status={self.status})>"


class Invitation(Base):
    """Invitation model for family member invitations"""
    
    __tablename__ = "invitations"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id", ondelete="CASCADE"), nullable=False, index=True)
    invited_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    invited_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Invitation details
    email = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # admin, editor, viewer
    status = Column(String(20), nullable=False, default='pending')  # pending, accepted, declined, expired
    
    # Optional message
    message = Column(Text)
    invitation_token = Column(String(255), unique=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    expires_at = Column(DateTime(timezone=False), nullable=False)
    responded_at = Column(DateTime(timezone=False))
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'editor', 'viewer')",
            name="invitations_role_check"
        ),
        CheckConstraint(
            "status IN ('pending', 'accepted', 'declined', 'expired')",
            name="invitations_status_check"
        ),
    )
    
    # Relationships
    family = relationship("Family", back_populates="invitations")
    inviter = relationship("User", foreign_keys=[invited_by])
    invited_user = relationship("User", foreign_keys=[invited_user_id])
    
    def __repr__(self):
        return f"<Invitation(id={self.id}, email={self.email}, family_id={self.family_id}, status={self.status})>"