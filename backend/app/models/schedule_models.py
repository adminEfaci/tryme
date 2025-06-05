"""
Schedule-related models only.
Single Responsibility: Schedule domain data models.
"""

import uuid
from datetime import date, time, datetime
from typing import Optional
from sqlmodel import SQLModel, Field

from .base import BaseModel
from ..enums.schedule_enums import ScheduleStatus, AssignmentStatus, EventType


class ScheduleBase(SQLModel):
    """Base schedule model"""
    route_id: uuid.UUID = Field(foreign_key="routes.id")
    vehicle_id: uuid.UUID = Field(foreign_key="vehicles.id")
    
    # Date & Timing
    scheduled_date: date
    scheduled_start_time: time = Field(default=time(8, 0))
    scheduled_end_time: time = Field(default=time(16, 0))
    
    # Event Type
    event_type: EventType = Field(default=EventType.REGULAR_WEEK)
    
    # Status
    status: ScheduleStatus = Field(default=ScheduleStatus.SCHEDULED)
    priority: int = Field(default=1, ge=1, le=5)
    
    # Operational Details
    estimated_duration_minutes: int = Field(gt=0)
    estimated_stops: int = Field(ge=0)
    estimated_distance_km: float = Field(ge=0)
    
    # Actual Performance
    actual_start_time: Optional[datetime] = Field(default=None)
    actual_end_time: Optional[datetime] = Field(default=None)
    actual_stops: Optional[int] = Field(default=None)
    actual_distance_km: Optional[float] = Field(default=None)
    
    # Administrative
    locked_at: Optional[datetime] = Field(default=None)
    locked_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    
    # Completion
    completion_notes: Optional[str] = Field(default=None, max_length=1000)


class Schedule(ScheduleBase, BaseModel, table=True):
    """
    Schedule model.
    Single Responsibility: Schedule data management.
    """
    __tablename__ = "schedules"
    
    # Relationships will be defined after all models are created


class ScheduleAssignmentBase(SQLModel):
    """Base schedule assignment model"""
    schedule_id: uuid.UUID = Field(foreign_key="schedules.id")
    employee_id: uuid.UUID = Field(foreign_key="employees.id")
    
    # Assignment Details
    role: str = Field(max_length=50)  # "driver", "loader", "supervisor"
    assignment_status: AssignmentStatus = Field(default=AssignmentStatus.PLANNED)
    
    # Timing
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: uuid.UUID = Field(foreign_key="users.id")
    
    # Schedule Times
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime] = Field(default=None)
    actual_end: Optional[datetime] = Field(default=None)
    
    # Real-time Updates
    last_location_update: Optional[datetime] = Field(default=None)
    current_latitude: Optional[float] = Field(default=None)
    current_longitude: Optional[float] = Field(default=None)
    current_status: Optional[str] = Field(default=None, max_length=100)
    
    notes: Optional[str] = Field(default=None, max_length=1000)


class ScheduleAssignment(ScheduleAssignmentBase, BaseModel, table=True):
    """
    Schedule assignment model.
    Single Responsibility: Assignment data management.
    """
    __tablename__ = "schedule_assignments"
    
    # Relationships will be defined after all models are created


class AssignmentUpdateBase(SQLModel):
    """Base assignment update model"""
    assignment_id: uuid.UUID = Field(foreign_key="schedule_assignments.id")
    update_type: str = Field(max_length=50)
    
    # Update Details
    old_value: Optional[str] = Field(default=None, max_length=500)
    new_value: Optional[str] = Field(default=None, max_length=500)
    
    # Context
    updated_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    update_source: str = Field(max_length=50)
    
    # Location (if applicable)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    
    notes: Optional[str] = Field(default=None, max_length=500)


class AssignmentUpdate(AssignmentUpdateBase, BaseModel, table=True):
    """
    Assignment update model for tracking changes.
    Single Responsibility: Assignment update data management.
    """
    __tablename__ = "assignment_updates"
    
    # Relationships will be defined after all models are created