"""
Calendar-related models only.
Single Responsibility: Calendar domain data models.
"""

import uuid
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from .base import BaseModel
from ..enums.schedule_enums import EventType


class CalendarEventBase(SQLModel):
    """Base calendar event model"""
    name: str = Field(max_length=255, index=True)
    event_type: EventType
    
    # Date Range
    start_date: date
    end_date: date
    
    # Recurrence
    is_recurring: bool = Field(default=False)
    recurrence_pattern: Optional[str] = Field(default=None, max_length=100)
    recurrence_end_date: Optional[date] = Field(default=None)
    
    # Impact Factors
    capacity_multiplier: float = Field(default=1.0, ge=0.1, le=10.0)
    crew_multiplier: float = Field(default=1.0, ge=0.1, le=5.0)
    vehicle_requirements: Optional[str] = Field(default=None)  # JSON array
    
    # Service Changes
    affects_regular_service: bool = Field(default=False)
    service_modifications: Optional[str] = Field(default=None)  # JSON description
    
    # Planning
    advance_notice_days: int = Field(default=7, ge=0)
    requires_special_equipment: bool = Field(default=False)
    requires_additional_permits: bool = Field(default=False)
    
    # Financial Impact
    cost_multiplier: float = Field(default=1.0, ge=0.1, le=10.0)
    additional_fees: Optional[float] = Field(default=None, ge=0)
    
    description: Optional[str] = Field(default=None, max_length=1000)
    special_instructions: Optional[str] = Field(default=None, max_length=1000)


class CalendarEvent(CalendarEventBase, BaseModel, table=True):
    """
    Calendar event model.
    Single Responsibility: Calendar event data management.
    """
    __tablename__ = "calendar_events"
    
    # Relationships will be defined after all models are created


class ContractCalendarEventBase(SQLModel):
    """Base contract calendar event model"""
    contract_id: uuid.UUID = Field(foreign_key="contracts.id", primary_key=True)
    calendar_event_id: uuid.UUID = Field(foreign_key="calendar_events.id", primary_key=True)
    
    # Contract-specific overrides
    custom_multiplier: Optional[float] = Field(default=None, ge=0.1, le=10.0)
    custom_instructions: Optional[str] = Field(default=None, max_length=500)
    is_opted_out: bool = Field(default=False)


class ContractCalendarEvent(ContractCalendarEventBase, BaseModel, table=True):
    """
    Contract calendar event association.
    Single Responsibility: Contract-event relationship management.
    """
    __tablename__ = "contract_calendar_events"
    
    # Override the id field since this is a many-to-many table
    id: Optional[uuid.UUID] = Field(default=None, primary_key=False)
    
    # Relationships will be defined after all models are created