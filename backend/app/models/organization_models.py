"""
Organization-related models only.
Single Responsibility: Organization domain data models.
"""

import uuid
from datetime import date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from .base import BaseModel
from ..enums.system_enums import OrganizationType, ComplianceStatus


class OrganizationBase(SQLModel):
    """Base organization model"""
    name: str = Field(max_length=255, index=True)
    legal_name: str = Field(max_length=255)
    business_number: Optional[str] = Field(default=None, max_length=50)
    tax_id: Optional[str] = Field(default=None, max_length=50)
    organization_type: OrganizationType
    status: ComplianceStatus = Field(default=ComplianceStatus.COMPLIANT)
    
    # Contact Information
    primary_contact_name: str = Field(max_length=255)
    primary_contact_email: str = Field(max_length=255)
    primary_contact_phone: str = Field(max_length=20)
    
    # Address
    address_line1: str = Field(max_length=255)
    address_line2: Optional[str] = Field(default=None, max_length=255)
    city: str = Field(max_length=100)
    province_state: str = Field(max_length=100)
    postal_code: str = Field(max_length=20)
    country: str = Field(default="Canada", max_length=100)
    
    # Operational Details
    max_capacity_hours_per_day: int = Field(default=480, gt=0)  # 8 hours default
    max_vehicles: int = Field(default=10, gt=0)
    max_employees: int = Field(default=50, gt=0)
    service_areas: Optional[str] = Field(default=None)  # JSON array of postal codes
    
    # Compliance
    insurance_policy_number: Optional[str] = Field(default=None, max_length=100)
    insurance_expiry: Optional[date] = Field(default=None)
    license_number: Optional[str] = Field(default=None, max_length=100)
    license_expiry: Optional[date] = Field(default=None)
    
    # Financial
    hourly_rate: Optional[float] = Field(default=None, ge=0)
    overtime_multiplier: float = Field(default=1.5, ge=1.0)
    holiday_multiplier: float = Field(default=2.0, ge=1.0)
    
    # Performance Metrics
    performance_score: float = Field(default=100.0, ge=0, le=100)
    reliability_score: float = Field(default=100.0, ge=0, le=100)
    safety_score: float = Field(default=100.0, ge=0, le=100)


class Organization(OrganizationBase, BaseModel, table=True):
    """
    Organization model for contractors and subcontractors.
    Single Responsibility: Organization data management.
    """
    __tablename__ = "organizations"
    
    # Parent-Child relationship for subcontractors
    parent_organization_id: Optional[uuid.UUID] = Field(
        default=None, 
        foreign_key="organizations.id"
    )
    
    # Relationships will be defined after all models are created