"""
Deceased profile models
Memorial and tribute management
"""

from sqlalchemy import Column, String, Text, Date, Integer, ForeignKey, CheckConstraint, ARRAY, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB, TSVECTOR
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class DeceasedProfile(Base):
    """Deceased profile model for memorial management"""
    
    __tablename__ = "deceased_profiles"
    
    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Basic information - Western style names
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100))
    nickname = Column(String(100))
    
    # Names for Vietnamese culture compatibility
    english_name = Column(String(200))
    common_name = Column(String(100))
    gender = Column(String(20))
    
    # Important dates - Solar calendar
    date_of_birth = Column(Date)
    date_of_death = Column(Date)
    birth_date = Column(Date)  # Schema compatibility
    death_date = Column(Date)  # Schema compatibility
    
    # Lunar calendar dates for Vietnamese culture
    birth_date_lunar = Column(String(50))
    death_date_lunar = Column(String(50))
    
    # Location information
    place_of_birth = Column(String(200))
    place_of_death = Column(String(200))
    birth_place = Column(String(300))  # Schema compatibility
    death_place = Column(String(300))  # Schema compatibility
    resting_place = Column(String(500))  # Cemetery/burial location
    cause_of_death = Column(String(500))
    
    # Personal information
    occupation = Column(String(200))
    education = Column(String(300))
    
    # Life information
    biography = Column(Text)
    life_achievements = Column(Text)
    memorable_quotes = Column(Text)
    special_dates = Column(JSONB, default={})
    
    # Vietnamese cultural fields
    vietnamese_name = Column(String(200))
    generation_name = Column(String(100))
    ancestral_title = Column(String(200))
    location_info = Column(JSONB, default={})
    cultural_info = Column(JSONB, default={})  # Additional cultural information
    
    # Family and access control
    family_id = Column(UUID(as_uuid=True), ForeignKey("families.id"))
    privacy_level = Column(String(20), default='family')
    allowed_users = Column(ARRAY(UUID(as_uuid=True)), default=[])
    
    # Media
    profile_photo = Column(String(500))
    cover_photo = Column(String(500))
    
    # Audit fields
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    last_modified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    
    # Statistics
    view_count = Column(Integer, default=0)
    search_vector = Column(TSVECTOR)
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "privacy_level IN ('public', 'family', 'private')",
            name="deceased_profiles_privacy_level_check"
        ),
        CheckConstraint(
            "vietnamese_name IS NOT NULL AND length(vietnamese_name) > 0",
            name="vietnamese_name_required"
        ),
        CheckConstraint(
            "date_of_death IS NULL OR date_of_birth IS NULL OR date_of_death >= date_of_birth",
            name="valid_dates"
        ),
        CheckConstraint(
            "death_date IS NULL OR birth_date IS NULL OR death_date >= birth_date",
            name="valid_schema_dates"
        ),
    )
    
    # Relationships
    family = relationship("Family", back_populates="deceased_profiles")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_profiles")
    last_modifier = relationship("User", foreign_keys=[last_modified_by])
    media_files = relationship("MediaFile", back_populates="profile", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<DeceasedProfile(id={self.id}, name={self.first_name} {self.last_name})>"
    
    @property
    def full_name(self):
        """Get deceased person's full name"""
        # Prefer English name if available
        if self.english_name:
            return self.english_name
        # Fall back to traditional first/last name
        if self.first_name and self.last_name:
            names = [self.first_name]
            if self.middle_name:
                names.append(self.middle_name)
            names.append(self.last_name)
            return " ".join(names)
        # Use Vietnamese name as last resort
        return self.vietnamese_name or "Unknown"
    
    @property
    def display_name(self):
        """Get display name with nickname if available"""
        if self.common_name:
            return f"{self.vietnamese_name} ({self.common_name})"
        elif self.nickname and self.first_name and self.last_name:
            return f"{self.first_name} '{self.nickname}' {self.last_name}"
        return self.full_name