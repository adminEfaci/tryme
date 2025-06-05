"""
Organization-related schemas only.
Single Responsibility: Organization domain DTOs.
"""

import uuid
from datetime import date
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, validator

from .base_schemas import BaseResponse
from ..enums.system_enums import OrganizationType, ComplianceStatus


class OrganizationBase(BaseModel):
    """
    Base organization schema.
    Single Responsibility: Common organization fields.
    """
    name: str = Field(..., min_length=1, max_length=255)
    legal_name: str = Field(..., min_length=1, max_length=255)
    business_number: Optional[str] = Field(None, max_length=50)
    tax_id: Optional[str] = Field(None, max_length=50)
    organization_type: OrganizationType
    
    # Contact Information
    primary_contact_name: str = Field(..., min_length=1, max_length=255)
    primary_contact_email: EmailStr
    primary_contact_phone: str = Field(..., min_length=10, max_length=20)
    
    # Address
    address_line1: str = Field(..., min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    province_state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(default="Canada", max_length=100)
    
    # Operational Details
    max_capacity_hours_per_day: int = Field(default=480, gt=0, le=1440)
    max_vehicles: int = Field(default=10, gt=0)
    max_employees: int = Field(default=50, gt=0)
    service_areas: Optional[str] = Field(None)  # JSON array
    
    # Compliance
    insurance_policy_number: Optional[str] = Field(None, max_length=100)
    insurance_expiry: Optional[date] = None
    license_number: Optional[str] = Field(None, max_length=100)
    license_expiry: Optional[date] = None
    
    # Financial
    hourly_rate: Optional[Decimal] = Field(None, ge=0)
    overtime_multiplier: Decimal = Field(default=Decimal("1.5"), ge=1.0)
    holiday_multiplier: Decimal = Field(default=Decimal("2.0"), ge=1.0)
    
    @validator('name')
    def validate_name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Organization name cannot be empty')
        return v.strip()
    
    @validator('primary_contact_phone')
    def validate_phone_format(cls, v):
        # Basic phone validation - can be enhanced
        if not v or len(v.replace('-', '').replace(' ', '').replace('(', '').replace(')', '').replace('+', '')) < 10:
            raise ValueError('Invalid phone number format')
        return v
    
    @validator('postal_code')
    def validate_postal_code(cls, v):
        if not v or not v.strip():
            raise ValueError('Postal code is required')
        return v.strip().upper()


class OrganizationCreate(OrganizationBase):
    """
    Organization creation schema.
    Single Responsibility: Organization creation validation.
    """
    parent_organization_id: Optional[uuid.UUID] = None
    
    @validator('parent_organization_id')
    def validate_subcontractor_has_parent(cls, v, values):
        org_type = values.get('organization_type')
        if org_type == OrganizationType.SUBCONTRACTOR and not v:
            raise ValueError('Subcontractor must have a parent organization')
        if org_type == OrganizationType.PRIME_CONTRACTOR and v:
            raise ValueError('Prime contractor cannot have a parent organization')
        return v


class OrganizationUpdate(BaseModel):
    """
    Organization update schema.
    Single Responsibility: Organization update validation.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    legal_name: Optional[str] = Field(None, min_length=1, max_length=255)
    business_number: Optional[str] = Field(None, max_length=50)
    tax_id: Optional[str] = Field(None, max_length=50)
    
    # Contact Information
    primary_contact_name: Optional[str] = Field(None, min_length=1, max_length=255)
    primary_contact_email: Optional[EmailStr] = None
    primary_contact_phone: Optional[str] = Field(None, min_length=10, max_length=20)
    
    # Address
    address_line1: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    province_state: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    
    # Operational Details
    max_capacity_hours_per_day: Optional[int] = Field(None, gt=0, le=1440)
    max_vehicles: Optional[int] = Field(None, gt=0)
    max_employees: Optional[int] = Field(None, gt=0)
    service_areas: Optional[str] = None
    
    # Compliance
    insurance_policy_number: Optional[str] = Field(None, max_length=100)
    insurance_expiry: Optional[date] = None
    license_number: Optional[str] = Field(None, max_length=100)
    license_expiry: Optional[date] = None
    
    # Financial
    hourly_rate: Optional[Decimal] = Field(None, ge=0)
    overtime_multiplier: Optional[Decimal] = Field(None, ge=1.0)
    holiday_multiplier: Optional[Decimal] = Field(None, ge=1.0)
    
    # Performance
    performance_score: Optional[float] = Field(None, ge=0, le=100)
    reliability_score: Optional[float] = Field(None, ge=0, le=100)
    safety_score: Optional[float] = Field(None, ge=0, le=100)


class OrganizationResponse(OrganizationBase, BaseResponse):
    """
    Organization response schema.
    Single Responsibility: Organization API response.
    """
    status: ComplianceStatus
    parent_organization_id: Optional[uuid.UUID] = None
    
    # Performance Metrics
    performance_score: float
    reliability_score: float
    safety_score: float
    
    # Relationships
    subcontractors_count: int = 0
    employees_count: int = 0
    active_contracts_count: int = 0


class CapacityStatusResponse(BaseModel):
    """
    Organization capacity status response.
    Single Responsibility: Capacity status information.
    """
    organization_id: uuid.UUID
    date: date
    max_capacity_hours_per_day: int
    current_workload_hours: float
    available_capacity_hours: float
    utilization_percentage: float
    is_over_capacity: bool
    
    class Config:
        from_attributes = True


class OrganizationListResponse(BaseModel):
    """
    Organization list response.
    Single Responsibility: Organization list structure.
    """
    organizations: List[OrganizationResponse]
    total_count: int
    
    class Config:
        from_attributes = True