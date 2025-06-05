"""
Employee-related models only.
Single Responsibility: Employee domain data models.
"""

import uuid
from datetime import date, time
from typing import Optional
from sqlmodel import SQLModel, Field

from .base import BaseModel
from ..enums.system_enums import EmployeeStatus


class EmployeeBase(SQLModel):
    """Base employee model"""
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    employee_number: str = Field(unique=True, max_length=20, index=True)
    
    # Personal Information
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    date_of_birth: Optional[date] = Field(default=None)
    
    # Contact
    phone: str = Field(max_length=20)
    email: Optional[str] = Field(default=None, max_length=255)
    emergency_contact_name: Optional[str] = Field(default=None, max_length=255)
    emergency_contact_phone: Optional[str] = Field(default=None, max_length=20)
    
    # Employment
    hire_date: date
    termination_date: Optional[date] = Field(default=None)
    employment_status: EmployeeStatus = Field(default=EmployeeStatus.ACTIVE)
    job_title: str = Field(max_length=100)
    department: Optional[str] = Field(default=None, max_length=100)
    
    # Driver-specific fields
    license_number: Optional[str] = Field(default=None, max_length=50)
    license_class: Optional[str] = Field(default=None, max_length=10)
    license_expiry: Optional[date] = Field(default=None)
    
    # Work Preferences
    preferred_start_time: Optional[time] = Field(default=None)
    max_daily_hours: int = Field(default=8, ge=4, le=16)
    can_work_overtime: bool = Field(default=True)
    can_work_holidays: bool = Field(default=False)
    can_work_weekends: bool = Field(default=False)
    
    # Financial
    hourly_rate: float = Field(gt=0)
    overtime_rate: Optional[float] = Field(default=None, gt=0)
    holiday_rate: Optional[float] = Field(default=None, gt=0)


class Employee(EmployeeBase, BaseModel, table=True):
    """
    Employee model.
    Single Responsibility: Employee data management.
    """
    __tablename__ = "employees"
    
    # Relationships will be defined after all models are created