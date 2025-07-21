"""
Configuration management for Trang Vien So API
Handles environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # API Configuration
    API_TITLE: str = "Trang Vien So API"
    API_DESCRIPTION: str = "Vietnamese Memorial App API"
    API_VERSION: str = "2.0.0"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Configuration
    DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5432/trang_vien_so"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_POOL_RECYCLE: int = 3600
    
    # Security Configuration
    SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_SECRET_KEY: str = secrets.token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    
    # Token expiration settings
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7  # 7 days
    REFRESH_TOKEN_EXPIRE_DAYS_EXTENDED: int = 30  # 30 days for "remember me"
    
    # Backward compatibility
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Password Security
    BCRYPT_ROUNDS: int = 12
    
    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001", 
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_WINDOW: int = 60  # seconds
    
    # Email Configuration (for future use)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    
    # File Upload Configuration
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif", "image/webp",
        "video/mp4", "video/webm", "video/ogg",
        "application/pdf"
    ]
    
    # Monitoring & Logging
    LOG_LEVEL: str = "INFO"
    ENABLE_ACCESS_LOG: bool = True
    ENABLE_METRICS: bool = True
    
    # Vietnamese Cultural Settings
    DEFAULT_LANGUAGE: str = "vi"
    DEFAULT_TIMEZONE: str = "Asia/Ho_Chi_Minh"
    SUPPORTED_LANGUAGES: List[str] = ["vi", "en"]
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
        # Allow validation of extra fields for flexibility
        extra = "allow"


# Create global settings instance
settings = Settings()


def get_database_url() -> str:
    """Get database URL with proper formatting"""
    return settings.DATABASE_URL


def get_cors_origins() -> List[str]:
    """Get CORS allowed origins"""
    if settings.ENVIRONMENT == "production":
        # In production, be more restrictive
        return [
            "https://trangvienso.com",
            "https://www.trangvienso.com",
            "https://api.trangvienso.com"
        ]
    return settings.ALLOWED_ORIGINS


def is_development() -> bool:
    """Check if running in development mode"""
    return settings.ENVIRONMENT == "development"


def is_production() -> bool:
    """Check if running in production mode"""
    return settings.ENVIRONMENT == "production"