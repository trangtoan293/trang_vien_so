"""
Family Pydantic schemas - placeholder
"""

from pydantic import BaseModel
from typing import Optional
import uuid

class FamilyCreate(BaseModel):
    """Family creation schema - placeholder"""
    family_name: str

class FamilyUpdate(BaseModel):
    """Family update schema - placeholder"""
    family_name: Optional[str] = None

class FamilyResponse(BaseModel):
    """Family response schema - placeholder"""
    id: uuid.UUID
    family_name: str
    
    class Config:
        from_attributes = True

class FamilyMemberResponse(BaseModel):
    """Family member response schema - placeholder"""
    id: uuid.UUID
    role: str
    
    class Config:
        from_attributes = True

class InvitationCreate(BaseModel):
    """Invitation creation schema - placeholder"""
    email: str

class InvitationResponse(BaseModel):
    """Invitation response schema - placeholder"""
    id: uuid.UUID
    email: str
    
    class Config:
        from_attributes = True