"""
Trang Vien So - FastAPI Backend Application
Vietnamese Memorial App API Server
"""

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging
from datetime import datetime

from app.core.config import settings
from app.core.database import init_db
from app.routers import auth, users, health, deceased

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Trang Vien So API",
    description="🕯️ Vietnamese Memorial App - API for storing and sharing memories of loved ones",
    version="2.0.0",
    docs_url="/api/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT == "development" else None,
)

# Security middleware
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=["localhost", "127.0.0.1", "*.example.com"]
    )

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses"""
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-API-Version"] = "2.0.0"
    return response

# Request logging middleware  
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = time.perf_counter()
    
    # Log request
    logger.info(f"📥 {request.method} {request.url.path} - {request.client.host}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.perf_counter() - start_time
    logger.info(
        f"📤 {request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )
    
    return response

# Database initialization
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    logger.info("🚀 Starting Trang Vien So API Server...")
    logger.info(f"📚 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔗 Database URL: {settings.DATABASE_URL[:50]}...")
    
    # Initialize database (skip for testing if DB not available)
    try:
        await init_db()
        logger.info("✅ Database connection established")
    except Exception as e:
        logger.warning(f"⚠️ Database connection failed (testing mode): {e}")
        logger.info("🔄 Continuing without database for basic testing")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 Shutting down Trang Vien So API Server...")

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(deceased.router, prefix="/api/deceased", tags=["deceased-profiles"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Trang Vien So API",
        "description": "Vietnamese Memorial App - API for storing and sharing memories",
        "version": "2.0.0",
        "environment": settings.ENVIRONMENT,
        "docs_url": "/api/docs" if settings.ENVIRONMENT == "development" else None,
        "timestamp": datetime.utcnow().isoformat(),
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )