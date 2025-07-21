"""
Deceased profile management router
CRUD operations for deceased profiles with Vietnamese cultural features
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import List, Optional
import uuid
import logging

logger = logging.getLogger(__name__)

from app.core.database import get_db
from app.core.auth import get_current_user
from app.models.user import User
from app.models.deceased import DeceasedProfile
from app.schemas.deceased import (
    DeceasedProfileCreate,
    DeceasedProfileUpdate,
    DeceasedProfileResponse,
    DeceasedProfileList
)


router = APIRouter()


@router.post("/", response_model=DeceasedProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_deceased_profile(
    profile_data: DeceasedProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new deceased profile
    
    Creates a deceased profile with Vietnamese cultural information
    """
    try:
        logger.info(f"Creating deceased profile for user {current_user.id}")
        # Create deceased profile
        deceased_profile = DeceasedProfile(
        created_by=current_user.id,
        family_id=profile_data.family_id,
        # Basic information
        vietnamese_name=profile_data.vietnamese_name,
        english_name=profile_data.english_name,
        common_name=profile_data.common_name,
        generation_name=profile_data.generation_name,
        ancestral_title=profile_data.ancestral_title,
        gender=profile_data.gender,
        # Dates
        birth_date=profile_data.birth_date,
        death_date=profile_data.death_date,
        birth_date_lunar=profile_data.birth_date_lunar,
        death_date_lunar=profile_data.death_date_lunar,
        # Places
        birth_place=profile_data.birth_place,
        death_place=profile_data.death_place,
        resting_place=profile_data.resting_place,
        # Personal information
        occupation=profile_data.occupation,
        education=profile_data.education,
        biography=profile_data.biography,
        # Special dates and cultural info
        special_dates=profile_data.special_dates or {},
        cultural_info=profile_data.cultural_info or {},
        # Privacy
        privacy_level=profile_data.privacy_level
        )
        
        db.add(deceased_profile)
        await db.commit()
        await db.refresh(deceased_profile)
        
        return DeceasedProfileResponse(
        id=deceased_profile.id,
        family_id=deceased_profile.family_id,
        created_by=deceased_profile.created_by,
        vietnamese_name=deceased_profile.vietnamese_name,
        english_name=deceased_profile.english_name,
        common_name=deceased_profile.common_name,
        generation_name=deceased_profile.generation_name,
        ancestral_title=deceased_profile.ancestral_title,
        gender=deceased_profile.gender,
        birth_date=deceased_profile.birth_date,
        death_date=deceased_profile.death_date,
        birth_date_lunar=deceased_profile.birth_date_lunar,
        death_date_lunar=deceased_profile.death_date_lunar,
        birth_place=deceased_profile.birth_place,
        death_place=deceased_profile.death_place,
        resting_place=deceased_profile.resting_place,
        occupation=deceased_profile.occupation,
        education=deceased_profile.education,
        biography=deceased_profile.biography,
        special_dates=deceased_profile.special_dates,
        cultural_info=deceased_profile.cultural_info,
        privacy_level=deceased_profile.privacy_level,
            created_at=deceased_profile.created_at,
            updated_at=deceased_profile.updated_at
        )
    except Exception as e:
        logger.error(f"Error creating deceased profile: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create deceased profile: {str(e)}"
        )


@router.get("/", response_model=DeceasedProfileList)
async def get_deceased_profiles(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    family_id: Optional[uuid.UUID] = Query(None, description="Filter by family ID"),
    search: Optional[str] = Query(None, description="Search in names and biography"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get deceased profiles list
    
    Returns paginated list of deceased profiles accessible by the user
    """
    # Base query for profiles user can access
    query = select(DeceasedProfile).where(
        or_(
            DeceasedProfile.created_by == current_user.id,
            DeceasedProfile.privacy_level == "public"
        )
    )
    
    # Apply filters
    if family_id:
        query = query.where(DeceasedProfile.family_id == family_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                DeceasedProfile.vietnamese_name.ilike(search_term),
                DeceasedProfile.english_name.ilike(search_term),
                DeceasedProfile.common_name.ilike(search_term),
                DeceasedProfile.biography.ilike(search_term)
            )
        )
    
    # Get total count
    count_result = await db.execute(
        select(DeceasedProfile).where(query.whereclause)
    )
    total = len(count_result.scalars().all())
    
    # Get paginated results
    query = query.offset(skip).limit(limit).order_by(DeceasedProfile.created_at.desc())
    result = await db.execute(query)
    profiles = result.scalars().all()
    
    # Convert to response format
    profile_responses = []
    for profile in profiles:
        profile_responses.append(DeceasedProfileResponse(
            id=profile.id,
            family_id=profile.family_id,
            created_by=profile.created_by,
            vietnamese_name=profile.vietnamese_name,
            english_name=profile.english_name,
            common_name=profile.common_name,
            generation_name=profile.generation_name,
            ancestral_title=profile.ancestral_title,
            gender=profile.gender,
            birth_date=profile.birth_date,
            death_date=profile.death_date,
            birth_date_lunar=profile.birth_date_lunar,
            death_date_lunar=profile.death_date_lunar,
            birth_place=profile.birth_place,
            death_place=profile.death_place,
            resting_place=profile.resting_place,
            occupation=profile.occupation,
            education=profile.education,
            biography=profile.biography,
            special_dates=profile.special_dates,
            cultural_info=profile.cultural_info,
            privacy_level=profile.privacy_level,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        ))
    
    return DeceasedProfileList(
        profiles=profile_responses,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{profile_id}", response_model=DeceasedProfileResponse)
async def get_deceased_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get specific deceased profile
    
    Returns detailed information about a deceased profile
    """
    result = await db.execute(
        select(DeceasedProfile).where(DeceasedProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deceased profile not found"
        )
    
    # Check access permissions
    if (profile.created_by != current_user.id and 
        profile.privacy_level == "private"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this profile"
        )
    
    return DeceasedProfileResponse(
        id=profile.id,
        family_id=profile.family_id,
        created_by=profile.created_by,
        vietnamese_name=profile.vietnamese_name,
        english_name=profile.english_name,
        common_name=profile.common_name,
        generation_name=profile.generation_name,
        ancestral_title=profile.ancestral_title,
        gender=profile.gender,
        birth_date=profile.birth_date,
        death_date=profile.death_date,
        birth_date_lunar=profile.birth_date_lunar,
        death_date_lunar=profile.death_date_lunar,
        birth_place=profile.birth_place,
        death_place=profile.death_place,
        resting_place=profile.resting_place,
        occupation=profile.occupation,
        education=profile.education,
        biography=profile.biography,
        special_dates=profile.special_dates,
        cultural_info=profile.cultural_info,
        privacy_level=profile.privacy_level,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.put("/{profile_id}", response_model=DeceasedProfileResponse)
async def update_deceased_profile(
    profile_id: uuid.UUID,
    profile_data: DeceasedProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update deceased profile
    
    Updates information for an existing deceased profile
    """
    result = await db.execute(
        select(DeceasedProfile).where(DeceasedProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deceased profile not found"
        )
    
    # Check edit permissions (only creator can edit)
    if profile.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the profile creator can edit this profile"
        )
    
    # Update fields that are provided
    update_data = profile_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return DeceasedProfileResponse(
        id=profile.id,
        family_id=profile.family_id,
        created_by=profile.created_by,
        vietnamese_name=profile.vietnamese_name,
        english_name=profile.english_name,
        common_name=profile.common_name,
        generation_name=profile.generation_name,
        ancestral_title=profile.ancestral_title,
        gender=profile.gender,
        birth_date=profile.birth_date,
        death_date=profile.death_date,
        birth_date_lunar=profile.birth_date_lunar,
        death_date_lunar=profile.death_date_lunar,
        birth_place=profile.birth_place,
        death_place=profile.death_place,
        resting_place=profile.resting_place,
        occupation=profile.occupation,
        education=profile.education,
        biography=profile.biography,
        special_dates=profile.special_dates,
        cultural_info=profile.cultural_info,
        privacy_level=profile.privacy_level,
        created_at=profile.created_at,
        updated_at=profile.updated_at
    )


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_deceased_profile(
    profile_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete deceased profile
    
    Permanently deletes a deceased profile (only creator can delete)
    """
    result = await db.execute(
        select(DeceasedProfile).where(DeceasedProfile.id == profile_id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Deceased profile not found"
        )
    
    # Check delete permissions (only creator can delete)
    if profile.created_by != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the profile creator can delete this profile"
        )
    
    await db.delete(profile)
    await db.commit()


@router.get("/status")
async def deceased_profiles_status():
    """Deceased profiles router status"""
    return {
        "message": "Deceased Profiles API is active",
        "version": "1.0.0",
        "endpoints": [
            "POST / - Create deceased profile",
            "GET / - List deceased profiles", 
            "GET /{profile_id} - Get specific profile",
            "PUT /{profile_id} - Update profile",
            "DELETE /{profile_id} - Delete profile"
        ]
    }