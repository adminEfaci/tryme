"""
Base schema classes only.
Single Responsibility: Common DTO functionality.
"""

import uuid
from datetime import datetime
from typing import Generic, TypeVar, List, Optional, Any
from pydantic import BaseModel, Field


T = TypeVar('T')


class BaseResponse(BaseModel):
    """
    Base response schema.
    Single Responsibility: Common response structure.
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Paginated response schema.
    Single Responsibility: Pagination structure.
    """
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    has_next: bool
    has_prev: bool
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """
    Error response schema.
    Single Responsibility: Error response structure.
    """
    error_code: str
    message: str
    details: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True


class SuccessResponse(BaseModel):
    """
    Success response schema.
    Single Responsibility: Success response structure.
    """
    message: str
    data: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        from_attributes = True