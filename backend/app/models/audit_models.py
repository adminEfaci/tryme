"""
Audit-related models only.
Single Responsibility: Audit trail data models.
"""

import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from .base import BaseModel
from ..enums.system_enums import AuditAction


class AuditLogBase(SQLModel):
    """Base audit log model"""
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    
    # Action Details
    action: AuditAction
    resource_type: str = Field(max_length=100)
    resource_id: Optional[str] = Field(default=None, max_length=100)
    
    # Request Context
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=1000)
    endpoint: Optional[str] = Field(default=None, max_length=500)
    method: Optional[str] = Field(default=None, max_length=10)
    
    # Change Details
    old_values: Optional[str] = Field(default=None)  # JSON
    new_values: Optional[str] = Field(default=None)  # JSON
    
    # Additional Context
    description: Optional[str] = Field(default=None, max_length=1000)
    extra_metadata: Optional[str] = Field(default=None)  # JSON


class AuditLog(AuditLogBase, BaseModel, table=True):
    """
    Audit log model for compliance tracking.
    Single Responsibility: Audit trail data management.
    """
    __tablename__ = "audit_logs"
    
    # Relationships will be defined after all models are created