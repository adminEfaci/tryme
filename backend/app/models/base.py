"""
Base model classes only.
Single Responsibility: Common model functionality.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class UUIDMixin(SQLModel):
    """
    UUID primary key mixin.
    Single Responsibility: Provide UUID primary key.
    """
    id: Optional[uuid.UUID] = Field(
        default_factory=uuid.uuid4, 
        primary_key=True,
        index=True
    )


class TimestampMixin(SQLModel):
    """
    Timestamp mixin for created/updated tracking.
    Single Responsibility: Provide timestamp fields.
    """
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )


class BaseModel(UUIDMixin, TimestampMixin):
    """
    Base model with UUID and timestamps.
    Single Responsibility: Provide common model structure.
    """
    pass