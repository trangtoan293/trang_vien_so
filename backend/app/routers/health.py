"""
Health check endpoints for monitoring and status
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import datetime
import sys
import platform

from app.core.database import get_db
from app.core.config import settings


router = APIRouter()


@router.get("/api/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Comprehensive health check endpoint
    Compatible with Node.js implementation
    """
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    return {
        "success": True,
        "message": "Trang Vien So API is healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "system": {
            "platform": platform.system(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "architecture": platform.machine()
        }
    }


@router.get("/api/health/simple")
async def simple_health_check():
    """
    Simple health check without database dependency
    """
    return {
        "success": True,
        "message": "Trang Vien So API is healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "system": {
            "platform": platform.system(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "architecture": platform.machine()
        }
    }


@router.get("/api/status")
async def status_check():
    """
    Simple status endpoint for load balancer health checks
    """
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "2.0.0"
    }