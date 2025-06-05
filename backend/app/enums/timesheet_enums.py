"""
Timesheet-related enums only.
Single Responsibility: Timesheet domain constants.
"""

from enum import Enum


class TimesheetStatus(str, Enum):
    """Timesheet workflow status"""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    REQUIRES_REVISION = "requires_revision"
    PAID = "paid"
    ARCHIVED = "archived"


class WorkType(str, Enum):
    """Work classification types"""
    REGULAR = "regular"
    OVERTIME = "overtime"
    DOUBLE_TIME = "double_time"
    HOLIDAY = "holiday"
    SICK_LEAVE = "sick_leave"
    VACATION = "vacation"
    PERSONAL_LEAVE = "personal_leave"
    TRAINING = "training"
    MEETING = "meeting"
    TRAVEL_TIME = "travel_time"
    ON_CALL = "on_call"
    STANDBY = "standby"


class ClockEventType(str, Enum):
    """Time clock event types"""
    CLOCK_IN = "clock_in"
    CLOCK_OUT = "clock_out"
    BREAK_START = "break_start"
    BREAK_END = "break_end"
    LUNCH_START = "lunch_start"
    LUNCH_END = "lunch_end"
    OVERTIME_START = "overtime_start"
    OVERTIME_END = "overtime_end"


class PayrollPeriodType(str, Enum):
    """Payroll period types"""
    WEEKLY = "weekly"
    BI_WEEKLY = "bi_weekly"
    SEMI_MONTHLY = "semi_monthly"
    MONTHLY = "monthly"


class ApprovalLevel(str, Enum):
    """Timesheet approval hierarchy"""
    SUPERVISOR = "supervisor"
    MANAGER = "manager"
    HR = "hr"
    PAYROLL = "payroll"
    FINAL = "final"


class TimeEntrySource(str, Enum):
    """Source of time entry"""
    MANUAL = "manual"
    MOBILE_APP = "mobile_app"
    WEB_PORTAL = "web_portal"
    TIME_CLOCK = "time_clock"
    GPS_TRACKING = "gps_tracking"
    SYSTEM_GENERATED = "system_generated"
    IMPORTED = "imported"