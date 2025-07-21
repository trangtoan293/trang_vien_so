"""
Media file models
Media upload and management for deceased profiles
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, CheckConstraint, ARRAY, BigInteger, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class MediaFile(Base):
    """Media file model for photos, videos, documents associated with deceased profiles"""
    
    __tablename__ = "media_files"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign keys
    profile_id = Column(UUID(as_uuid=True), ForeignKey("deceased_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    # File information
    original_filename = Column(String(255), nullable=False)
    stored_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_url = Column(String(500), nullable=False)
    thumbnail_url = Column(String(500))
    
    # File metadata
    file_type = Column(String(50), nullable=False, index=True)  # image, video, document, audio
    mime_type = Column(String(100), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    
    # Media dimensions (for images/videos)
    width = Column(Integer)
    height = Column(Integer)
    duration = Column(Integer)  # in seconds for videos/audio
    
    # Content information
    caption = Column(Text)
    description = Column(Text)
    tags = Column(ARRAY(String(500)))
    
    # Context information
    date_taken = Column(DateTime(timezone=False))
    location_taken = Column(String(200))
    
    # Display settings
    display_order = Column(Integer, default=0)
    is_featured = Column(Boolean, default=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=False), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "file_type IN ('image', 'video', 'document', 'audio')",
            name="media_files_file_type_check"
        ),
        CheckConstraint(
            "file_size > 0",
            name="media_files_file_size_check"
        ),
    )
    
    # Relationships
    profile = relationship("DeceasedProfile", back_populates="media_files")
    uploader = relationship("User", foreign_keys=[uploaded_by])
    
    def __repr__(self):
        return f"<MediaFile(id={self.id}, filename={self.original_filename}, type={self.file_type})>"
    
    @property
    def file_size_mb(self):
        """Get file size in megabytes"""
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def is_image(self):
        """Check if file is an image"""
        return self.file_type == 'image'
    
    @property
    def is_video(self):
        """Check if file is a video"""
        return self.file_type == 'video'