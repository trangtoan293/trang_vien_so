"""
Media Pydantic schemas - placeholder
"""

from pydantic import BaseModel
from typing import Optional
import uuid

class MediaFileResponse(BaseModel):
    """Media file response schema - placeholder"""
    id: uuid.UUID
    original_filename: str
    
    class Config:
        from_attributes = True

class MediaFileUpload(BaseModel):
    """Media file upload schema - placeholder"""
    filename: str

class MediaFileUpdate(BaseModel):
    """Media file update schema - placeholder"""
    caption: Optional[str] = None