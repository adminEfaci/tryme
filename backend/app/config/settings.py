"""
Application settings configuration only.
Single Responsibility: Environment configuration management.
"""

from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Waste Management Intelligence System"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "development"
    
    # API
    api_v1_prefix: str = "/api/v1"
    backend_cors_origins: List[str] = [
        "http://localhost:3000", 
        "http://localhost:8080",
        "https://work-1-bnwrqilcplnoxtbq.prod-runtime.all-hands.dev",
        "https://work-2-bnwrqilcplnoxtbq.prod-runtime.all-hands.dev"
    ]
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./waste_management.db"
    database_echo: bool = False
    
    # Security
    secret_key: str = "waste-management-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # External Services
    openai_api_key: Optional[str] = None
    sentry_dsn: Optional[str] = None
    
    # File Storage
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    
    # Email
    smtp_host: Optional[str] = None
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 9090
    
    # Performance
    max_concurrent_requests: int = 1000
    request_timeout_seconds: int = 30
    
    # Business Rules
    max_daily_hours: float = 16.0
    overtime_threshold_hours: float = 40.0
    max_forecast_horizon_months: int = 12
    
    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings"""
    return Settings()