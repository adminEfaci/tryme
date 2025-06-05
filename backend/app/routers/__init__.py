"""
Routers package for the Waste Management Intelligence System.
Single Responsibility: API endpoint routing.
"""

from .organization_router import router as organization_router

__all__ = [
    "organization_router",
]