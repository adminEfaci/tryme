"""
Enums package for the Waste Management Intelligence System.

ALL ENUMS ARE DEFINED HERE - SEPARATE FROM MODELS
Following Single Responsibility Principle: Enums have one responsibility - defining constants.
"""

from .user_enums import *
from .contract_enums import *
from .schedule_enums import *
from .timesheet_enums import *
from .forecast_enums import *
from .system_enums import *

__all__ = [
    # User Enums
    "UserRole",
    "UserStatus", 
    "PermissionType",
    "AuthenticationMethod",
    
    # Contract Enums
    "ContractStatus",
    "ServiceType",
    "BillingFrequency",
    "ContractType",
    "PaymentTerms",
    
    # Schedule Enums
    "ScheduleStatus",
    "AssignmentStatus",
    "EventType",
    "VehicleType",
    "RouteStatus",
    "WeekDay",
    
    # Timesheet Enums
    "TimesheetStatus",
    "WorkType",
    "ClockEventType",
    "PayrollPeriodType",
    "ApprovalLevel",
    "TimeEntrySource",
    
    # Forecast Enums
    "ForecastType",
    "ForecastStatus",
    "ForecastAccuracy",
    "ForecastHorizon",
    "SeasonalPattern",
    "RiskFactor",
    
    # System Enums
    "AuditAction",
    "NotificationType",
    "NotificationPriority",
    "SystemStatus",
    "DataRetentionPolicy",
    "ExportFormat",
    "IntegrationStatus",
    "EmployeeStatus",
    "OrganizationType",
    "ComplianceStatus",
]