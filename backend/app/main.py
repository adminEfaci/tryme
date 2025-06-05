"""
FastAPI application initialization only.
Single Responsibility: Application setup and configuration.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .config import get_settings, create_db_and_tables, close_db, setup_logging
from .routers.organization_router import router as organization_router
from .middleware.error_middleware import ErrorHandlerMiddleware

# Setup logging
setup_logging()
logger = logging.getLogger("app.main")

# Get settings
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Single Responsibility: Application startup/shutdown logic.
    """
    # Startup
    logger.info("Starting Waste Management Intelligence System...")
    await create_db_and_tables()
    logger.info("Database tables created/verified")
    logger.info("Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    await close_db()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Municipal-grade waste logistics platform with FastAPI + SQLModel + TDD",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.debug else ["localhost", "127.0.0.1"]
)

app.add_middleware(ErrorHandlerMiddleware)

# Include routers
app.include_router(
    organization_router,
    prefix=f"{settings.api_v1_prefix}/organizations",
    tags=["organizations"]
)


@app.get("/")
async def root():
    """
    Root endpoint.
    Single Responsibility: Basic API information.
    """
    return {
        "message": f"{settings.app_name} API",
        "version": settings.app_version,
        "docs_url": f"{settings.api_v1_prefix}/docs",
        "health_check": "/health"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    Single Responsibility: Application health status.
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment
    }