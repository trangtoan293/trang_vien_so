"""
Users router - placeholder for future implementation
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def users_status():
    """Placeholder users endpoint"""
    return {"message": "Users routes - coming soon"}