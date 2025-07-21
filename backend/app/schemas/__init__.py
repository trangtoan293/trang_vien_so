"""
Pydantic schemas for request/response validation
Data transfer objects for API endpoints
"""

from .user import (
    UserRegisterRequest, UserLoginRequest, UserResponse, UserProfileUpdate,
    UserSessionResponse, PasswordChangeRequest
)
from .auth import (
    LoginResponse, TokenResponse, RefreshTokenRequest
)
from .deceased import (
    DeceasedProfileCreate, DeceasedProfileUpdate, DeceasedProfileResponse,
    DeceasedProfileList, DeceasedProfileSearch
)
from .family import (
    FamilyCreate, FamilyUpdate, FamilyResponse, FamilyMemberResponse,
    InvitationCreate, InvitationResponse
)
from .media import (
    MediaFileResponse, MediaFileUpload, MediaFileUpdate
)

__all__ = [
    # User schemas
    "UserRegisterRequest",
    "UserLoginRequest", 
    "UserResponse",
    "UserProfileUpdate",
    "UserSessionResponse",
    "PasswordChangeRequest",
    
    # Auth schemas
    "LoginResponse",
    "TokenResponse",
    "RefreshTokenRequest",
    
    # Deceased profile schemas
    "DeceasedProfileCreate",
    "DeceasedProfileUpdate", 
    "DeceasedProfileResponse",
    "DeceasedProfileList",
    "DeceasedProfileSearch",
    
    # Family schemas
    "FamilyCreate",
    "FamilyUpdate",
    "FamilyResponse",
    "FamilyMemberResponse",
    "InvitationCreate",
    "InvitationResponse",
    
    # Media schemas
    "MediaFileResponse",
    "MediaFileUpload",
    "MediaFileUpdate"
]