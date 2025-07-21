"""
Deceased profile Pydantic schemas
Vietnamese memorial app - deceased profile management
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import uuid


class DeceasedProfileCreate(BaseModel):
    """Deceased profile creation schema"""
    # Family relationship
    family_id: Optional[uuid.UUID] = Field(None, description="Family ID this profile belongs to")
    
    # Names in Vietnamese culture
    vietnamese_name: str = Field(..., min_length=1, max_length=200, description="Vietnamese name")
    english_name: Optional[str] = Field(None, max_length=200, description="English/Western name")
    common_name: Optional[str] = Field(None, max_length=100, description="Common name or nickname")
    generation_name: Optional[str] = Field(None, max_length=100, description="Generation name (tên thế hệ)")
    ancestral_title: Optional[str] = Field(None, max_length=200, description="Ancestral title or honorific")
    
    # Basic information
    gender: str = Field(..., description="Gender")
    
    # Dates (both solar and lunar calendar)
    birth_date: Optional[date] = Field(None, description="Birth date (solar calendar)")
    death_date: Optional[date] = Field(None, description="Death date (solar calendar)")
    birth_date_lunar: Optional[str] = Field(None, max_length=50, description="Birth date (lunar calendar)")
    death_date_lunar: Optional[str] = Field(None, max_length=50, description="Death date (lunar calendar)")
    
    # Places
    birth_place: Optional[str] = Field(None, max_length=300, description="Place of birth")
    death_place: Optional[str] = Field(None, max_length=300, description="Place of death")
    resting_place: Optional[str] = Field(None, max_length=500, description="Cemetery/burial location")
    
    # Personal information
    occupation: Optional[str] = Field(None, max_length=200, description="Occupation")
    education: Optional[str] = Field(None, max_length=300, description="Education background")
    biography: Optional[str] = Field(None, description="Life story and biography")
    
    # Vietnamese cultural specific
    special_dates: Optional[Dict[str, Any]] = Field(None, description="Special memorial dates")
    cultural_info: Optional[Dict[str, Any]] = Field(None, description="Cultural and religious information")
    
    # Privacy
    privacy_level: str = Field("family", description="Privacy level: public, family, private")
    
    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender values"""
        allowed_genders = ['male', 'female', 'other', 'nam', 'nữ', 'khác']
        if v.lower() not in allowed_genders:
            raise ValueError(f'Gender must be one of: {", ".join(allowed_genders)}')
        return v.lower()
    
    @validator('privacy_level')
    def validate_privacy_level(cls, v):
        """Validate privacy level"""
        allowed_levels = ['public', 'family', 'private']
        if v.lower() not in allowed_levels:
            raise ValueError(f'Privacy level must be one of: {", ".join(allowed_levels)}')
        return v.lower()


class DeceasedProfileUpdate(BaseModel):
    """Deceased profile update schema"""
    # Names
    vietnamese_name: Optional[str] = Field(None, min_length=1, max_length=200)
    english_name: Optional[str] = Field(None, max_length=200)
    common_name: Optional[str] = Field(None, max_length=100)
    generation_name: Optional[str] = Field(None, max_length=100)
    ancestral_title: Optional[str] = Field(None, max_length=200)
    
    # Basic information
    gender: Optional[str] = Field(None)
    
    # Dates
    birth_date: Optional[date] = Field(None)
    death_date: Optional[date] = Field(None)
    birth_date_lunar: Optional[str] = Field(None, max_length=50)
    death_date_lunar: Optional[str] = Field(None, max_length=50)
    
    # Places
    birth_place: Optional[str] = Field(None, max_length=300)
    death_place: Optional[str] = Field(None, max_length=300)
    resting_place: Optional[str] = Field(None, max_length=500)
    
    # Personal information
    occupation: Optional[str] = Field(None, max_length=200)
    education: Optional[str] = Field(None, max_length=300)
    biography: Optional[str] = Field(None)
    
    # Cultural information
    special_dates: Optional[Dict[str, Any]] = Field(None)
    cultural_info: Optional[Dict[str, Any]] = Field(None)
    
    # Privacy
    privacy_level: Optional[str] = Field(None)
    
    @validator('gender')
    def validate_gender(cls, v):
        """Validate gender values"""
        if v is None:
            return v
        allowed_genders = ['male', 'female', 'other', 'nam', 'nữ', 'khác']
        if v.lower() not in allowed_genders:
            raise ValueError(f'Gender must be one of: {", ".join(allowed_genders)}')
        return v.lower()
    
    @validator('privacy_level')
    def validate_privacy_level(cls, v):
        """Validate privacy level"""
        if v is None:
            return v
        allowed_levels = ['public', 'family', 'private']
        if v.lower() not in allowed_levels:
            raise ValueError(f'Privacy level must be one of: {", ".join(allowed_levels)}')
        return v.lower()


class DeceasedProfileResponse(BaseModel):
    """Deceased profile response schema"""
    id: uuid.UUID
    family_id: Optional[uuid.UUID]
    created_by: uuid.UUID
    
    # Names
    vietnamese_name: str
    english_name: Optional[str]
    common_name: Optional[str]
    generation_name: Optional[str]
    ancestral_title: Optional[str]
    
    # Basic information
    gender: str
    
    # Dates
    birth_date: Optional[date]
    death_date: Optional[date]
    birth_date_lunar: Optional[str]
    death_date_lunar: Optional[str]
    
    # Places
    birth_place: Optional[str]
    death_place: Optional[str]
    resting_place: Optional[str]
    
    # Personal information
    occupation: Optional[str]
    education: Optional[str]
    biography: Optional[str]
    
    # Cultural information
    special_dates: Optional[Dict[str, Any]]
    cultural_info: Optional[Dict[str, Any]]
    
    # Privacy
    privacy_level: str
    
    # Timestamps
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class DeceasedProfileList(BaseModel):
    """Deceased profile list schema"""
    profiles: List[DeceasedProfileResponse]
    total: int = Field(..., description="Total number of profiles")
    skip: int = Field(..., description="Number of records skipped")
    limit: int = Field(..., description="Number of records returned")


class DeceasedProfileSearch(BaseModel):
    """Deceased profile search schema"""
    query: str = Field(..., min_length=1, description="Search query")
    family_id: Optional[uuid.UUID] = Field(None, description="Filter by family ID")
    gender: Optional[str] = Field(None, description="Filter by gender")
    privacy_level: Optional[str] = Field(None, description="Filter by privacy level")