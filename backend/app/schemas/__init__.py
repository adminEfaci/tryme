"""
Schemas package for the Waste Management Intelligence System.
Single Responsibility: Pydantic DTOs for API serialization/deserialization.
"""

from .base_schemas import *
from .organization_schemas import *

__all__ = [
    # Base Schemas
    "BaseResponse",
    "PaginatedResponse",
    "ErrorResponse",
    
    # Organization Schemas
    "OrganizationBase",
    "OrganizationCreate",
    "OrganizationUpdate",
    "OrganizationResponse",
    "CapacityStatusResponse",
]