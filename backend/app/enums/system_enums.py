"""
System-wide enums only.
Single Responsibility: System domain constants.
"""

from enum import Enum


class AuditAction(str, Enum):
    """System audit actions"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    LOGIN_FAILED = "login_failed"
    PASSWORD_CHANGE = "password_change"
    ROLE_CHANGE = "role_change"
    SCHEDULE_EDIT = "schedule_edit"
    CREW_ASSIGN = "crew_assign"
    REPORT_SUBMIT = "report_submit"
    SLA_BREACH = "sla_breach"
    EXPORT_GENERATE = "export_generate"
    BULK_OPERATION = "bulk_operation"
    SYSTEM_MAINTENANCE = "system_maintenance"


class NotificationType(str, Enum):
    """Notification delivery methods"""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    IN_APP = "in_app"
    WEBHOOK = "webhook"
    SLACK = "slack"
    TEAMS = "teams"


class NotificationPriority(str, Enum):
    """Notification priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class SystemStatus(str, Enum):
    """System health status"""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    MAINTENANCE = "maintenance"
    OUTAGE = "outage"
    CRITICAL = "critical"


class DataRetentionPolicy(str, Enum):
    """Data retention periods"""
    DAYS_30 = "days_30"
    DAYS_90 = "days_90"
    MONTHS_6 = "months_6"
    YEAR_1 = "year_1"
    YEARS_3 = "years_3"
    YEARS_7 = "years_7"
    INDEFINITE = "indefinite"


class ExportFormat(str, Enum):
    """Export file formats"""
    PDF = "pdf"
    CSV = "csv"
    XLSX = "xlsx"
    JSON = "json"
    XML = "xml"
    HTML = "html"


class IntegrationStatus(str, Enum):
    """External integration status"""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    ERROR = "error"
    SYNCING = "syncing"
    RATE_LIMITED = "rate_limited"
    UNAUTHORIZED = "unauthorized"


class EmployeeStatus(str, Enum):
    """Employee employment status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"
    PROBATIONARY = "probationary"
    SEASONAL = "seasonal"
    CONTRACTOR = "contractor"


class OrganizationType(str, Enum):
    """Organization classification"""
    PRIME_CONTRACTOR = "prime_contractor"
    SUBCONTRACTOR = "subcontractor"
    INDEPENDENT = "independent"
    MUNICIPAL_DIRECT = "municipal_direct"
    PARTNERSHIP = "partnership"
    JOINT_VENTURE = "joint_venture"


class ComplianceStatus(str, Enum):
    """Compliance verification status"""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    REQUIRES_ACTION = "requires_action"
    EXPIRED = "expired"
    NOT_APPLICABLE = "not_applicable"