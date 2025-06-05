"""
User-related enums only.
Single Responsibility: User domain constants.
"""

from enum import Enum


class UserRole(str, Enum):
    """User roles with exact hierarchy levels"""
    SUPER_ADMIN = "super_admin"           # Level 10 - Highest
    ADMIN = "admin"                       # Level 9
    OPERATIONS_MANAGER = "operations_manager"  # Level 8
    SUPERVISOR = "supervisor"             # Level 7
    DISPATCHER = "dispatcher"             # Level 6
    DRIVER = "driver"                     # Level 5
    LOADER = "loader"                     # Level 4
    CLIENT_CONTACT = "client_contact"     # Level 3
    VIEW_ONLY = "view_only"              # Level 2
    GUEST = "guest"                      # Level 1 - Lowest


class UserStatus(str, Enum):
    """User account status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    LOCKED = "locked"
    PENDING_VERIFICATION = "pending_verification"
    PASSWORD_RESET_REQUIRED = "password_reset_required"


class PermissionType(str, Enum):
    """Granular permission types"""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    APPROVE = "approve"
    REJECT = "reject"
    OVERRIDE = "override"
    EXPORT = "export"
    AUDIT = "audit"
    BULK_EDIT = "bulk_edit"
    ADMIN_PANEL = "admin_panel"


class AuthenticationMethod(str, Enum):
    """Authentication methods"""
    PASSWORD = "password"
    MFA_TOTP = "mfa_totp"
    MFA_SMS = "mfa_sms"
    MFA_EMAIL = "mfa_email"
    MAGIC_LINK = "magic_link"
    SSO = "sso"
    API_KEY = "api_key"