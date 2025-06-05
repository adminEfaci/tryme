"""
Models package for the Waste Management Intelligence System.
Single Responsibility: Database model definitions only (NO ENUMS).

All enums are in the separate /enums/ package following SRP.
"""

from .base import BaseModel, TimestampMixin, UUIDMixin
from .user_models import User, Role, Permission, UserRole, RolePermission, UserSession
from .organization_models import Organization
from .employee_models import Employee
from .timesheet_models import Timesheet, TimeEntry, TimeClock
from .schedule_models import Schedule, ScheduleAssignment, AssignmentUpdate
from .forecast_models import Forecast, ForecastItem
from .calendar_models import CalendarEvent, ContractCalendarEvent
from .audit_models import AuditLog

__all__ = [
    # Base Models
    "BaseModel",
    "TimestampMixin", 
    "UUIDMixin",
    
    # User Models
    "User",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission", 
    "UserSession",
    
    # Organization Models
    "Organization",
    
    # Employee Models
    "Employee",
    
    # Timesheet Models
    "Timesheet",
    "TimeEntry",
    "TimeClock",
    
    # Schedule Models
    "Schedule",
    "ScheduleAssignment",
    "AssignmentUpdate",
    
    # Forecast Models
    "Forecast",
    "ForecastItem",
    
    # Calendar Models
    "CalendarEvent",
    "ContractCalendarEvent",
    
    # Audit Models
    "AuditLog",
]