"""
Services package for the Waste Management Intelligence System.
Single Responsibility: Business logic layer.
"""

from .organization_service import OrganizationService

__all__ = [
    "OrganizationService",
]