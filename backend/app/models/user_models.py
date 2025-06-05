"""
User-related models only.
Single Responsibility: User domain data models.
"""

import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from .base import BaseModel
from ..enums.user_enums import UserRole as UserRoleEnum, UserStatus, PermissionType


class RoleBase(SQLModel):
    """Base role model"""
    name: str = Field(unique=True, max_length=100, index=True)
    display_name: str = Field(max_length=255)
    description: Optional[str] = Field(default=None, max_length=500)
    is_system_role: bool = Field(default=False)
    is_active: bool = Field(default=True)
    hierarchy_level: int = Field(default=1, ge=1, le=10)


class Role(RoleBase, BaseModel, table=True):
    """
    Role model for RBAC.
    Single Responsibility: Role definition and hierarchy.
    """
    __tablename__ = "roles"
    
    # Relationships will be defined after all models are created


class PermissionBase(SQLModel):
    """Base permission model"""
    name: str = Field(unique=True, max_length=100, index=True)
    resource: str = Field(max_length=100)
    action: PermissionType
    description: Optional[str] = Field(default=None, max_length=500)
    conditions: Optional[str] = Field(default=None)  # JSON conditions


class Permission(PermissionBase, BaseModel, table=True):
    """
    Permission model for RBAC.
    Single Responsibility: Permission definition.
    """
    __tablename__ = "permissions"
    
    # Relationships will be defined after all models are created


class RolePermission(SQLModel, table=True):
    """
    Role-Permission association.
    Single Responsibility: Link roles to permissions.
    """
    __tablename__ = "role_permissions"
    
    role_id: uuid.UUID = Field(foreign_key="roles.id", primary_key=True)
    permission_id: uuid.UUID = Field(foreign_key="permissions.id", primary_key=True)
    granted_at: datetime = Field(default_factory=datetime.utcnow)


class UserBase(SQLModel):
    """Base user model"""
    username: str = Field(unique=True, max_length=100, index=True)
    email: str = Field(unique=True, max_length=255, index=True)
    
    # Personal Information
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    phone: Optional[str] = Field(default=None, max_length=20)
    
    # Account Status
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
    status: UserStatus = Field(default=UserStatus.ACTIVE)
    
    # Authentication
    failed_login_attempts: int = Field(default=0, ge=0)
    locked_until: Optional[datetime] = Field(default=None)
    last_login: Optional[datetime] = Field(default=None)
    password_changed_at: Optional[datetime] = Field(default=None)
    must_change_password: bool = Field(default=False)
    
    # MFA
    mfa_enabled: bool = Field(default=False)
    mfa_secret: Optional[str] = Field(default=None)
    backup_codes: Optional[str] = Field(default=None)  # JSON array
    
    # Preferences
    timezone: str = Field(default="America/Toronto", max_length=50)
    language: str = Field(default="en", max_length=10)
    theme: str = Field(default="light", max_length=20)
    
    # Organization Association
    organization_id: Optional[uuid.UUID] = Field(default=None, foreign_key="organizations.id")
    employee_id: Optional[uuid.UUID] = Field(default=None, foreign_key="employees.id")


class User(UserBase, BaseModel, table=True):
    """
    User model for authentication and authorization.
    Single Responsibility: User account management.
    """
    __tablename__ = "users"
    
    hashed_password: str = Field(max_length=255)
    
    # Relationships will be defined after all models are created


class UserRole(SQLModel, table=True):
    """
    User-Role association.
    Single Responsibility: Link users to roles.
    """
    __tablename__ = "user_roles"
    
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    role_id: uuid.UUID = Field(foreign_key="roles.id", primary_key=True)
    assigned_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    expires_at: Optional[datetime] = Field(default=None)


class UserSessionBase(SQLModel):
    """Base user session model"""
    user_id: uuid.UUID = Field(foreign_key="users.id")
    token: str = Field(unique=True, max_length=255)
    device_info: Optional[str] = Field(default=None, max_length=500)
    ip_address: Optional[str] = Field(default=None, max_length=45)
    user_agent: Optional[str] = Field(default=None, max_length=1000)
    expires_at: datetime
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    is_revoked: bool = Field(default=False)


class UserSession(UserSessionBase, BaseModel, table=True):
    """
    User session tracking.
    Single Responsibility: Session management.
    """
    __tablename__ = "user_sessions"
    
    # Relationships will be defined after all models are created