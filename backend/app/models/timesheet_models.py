"""
Timesheet-related models only.
Single Responsibility: Timesheet domain data models.
"""

import uuid
from datetime import date, time, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from .base import BaseModel
from ..enums.timesheet_enums import TimesheetStatus, WorkType, ClockEventType


class TimesheetBase(SQLModel):
    """Base timesheet model"""
    employee_id: uuid.UUID = Field(foreign_key="employees.id")
    
    # Time Period
    pay_period_start: date
    pay_period_end: date
    
    # Status & Approval
    status: TimesheetStatus = Field(default=TimesheetStatus.DRAFT)
    submitted_at: Optional[datetime] = Field(default=None)
    approved_at: Optional[datetime] = Field(default=None)
    approved_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    rejected_at: Optional[datetime] = Field(default=None)
    rejection_reason: Optional[str] = Field(default=None, max_length=500)
    
    # Time Totals (calculated fields)
    total_regular_hours: float = Field(default=0.0, ge=0)
    total_overtime_hours: float = Field(default=0.0, ge=0)
    total_holiday_hours: float = Field(default=0.0, ge=0)
    total_sick_hours: float = Field(default=0.0, ge=0)
    total_vacation_hours: float = Field(default=0.0, ge=0)
    
    # Pay Calculations
    regular_pay: float = Field(default=0.0, ge=0)
    overtime_pay: float = Field(default=0.0, ge=0)
    holiday_pay: float = Field(default=0.0, ge=0)
    total_pay: float = Field(default=0.0, ge=0)
    
    # Additional
    notes: Optional[str] = Field(default=None, max_length=1000)


class Timesheet(TimesheetBase, BaseModel, table=True):
    """
    Timesheet model.
    Single Responsibility: Timesheet data management.
    """
    __tablename__ = "timesheets"
    
    # Relationships will be defined after all models are created


class TimeEntryBase(SQLModel):
    """Base time entry model"""
    timesheet_id: uuid.UUID = Field(foreign_key="timesheets.id")
    
    # Date & Time
    work_date: date
    start_time: Optional[time] = Field(default=None)
    end_time: Optional[time] = Field(default=None)
    break_duration_minutes: int = Field(default=0, ge=0)
    
    # Work Classification
    work_type: WorkType = Field(default=WorkType.REGULAR)
    hours_worked: float = Field(ge=0, le=24)
    
    # Location & Assignment
    work_location: Optional[str] = Field(default=None, max_length=255)
    
    # GPS Tracking (for verification)
    clock_in_latitude: Optional[float] = Field(default=None)
    clock_in_longitude: Optional[float] = Field(default=None)
    clock_out_latitude: Optional[float] = Field(default=None)
    clock_out_longitude: Optional[float] = Field(default=None)
    
    # Additional Details
    description: Optional[str] = Field(default=None, max_length=500)
    notes: Optional[str] = Field(default=None, max_length=500)


class TimeEntry(TimeEntryBase, BaseModel, table=True):
    """
    Time entry model.
    Single Responsibility: Time entry data management.
    """
    __tablename__ = "time_entries"
    
    # Relationships will be defined after all models are created


class TimeClockBase(SQLModel):
    """Base time clock model"""
    employee_id: uuid.UUID = Field(foreign_key="employees.id")
    
    # Clock Event
    clock_type: ClockEventType
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Location
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    location_accuracy: Optional[float] = Field(default=None)
    
    # Device Info
    device_id: Optional[str] = Field(default=None, max_length=255)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    
    # Context
    notes: Optional[str] = Field(default=None, max_length=500)


class TimeClock(TimeClockBase, BaseModel, table=True):
    """
    Time clock model for real-time tracking.
    Single Responsibility: Time clock data management.
    """
    __tablename__ = "time_clock"
    
    # Relationships will be defined after all models are created