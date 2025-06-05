"""
Custom exceptions for the Waste Management Intelligence System.
Single Responsibility: Error handling and business rule violations.
"""

from typing import Optional, Dict, Any


class WasteManagementError(Exception):
    """
    Base exception for all waste management system errors.
    Single Responsibility: Base error structure.
    """
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class BusinessRuleViolationError(WasteManagementError):
    """
    Raised when a business rule is violated.
    Single Responsibility: Business rule violation handling.
    """
    
    def __init__(
        self, 
        rule_code: str, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Business rule violation: {message}",
            error_code=rule_code,
            details=details
        )
        self.rule_code = rule_code


class NotFoundError(WasteManagementError):
    """
    Raised when a requested resource is not found.
    Single Responsibility: Resource not found handling.
    """
    
    def __init__(
        self, 
        resource_type: str, 
        resource_id: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"{resource_type} with ID {resource_id} not found",
            error_code="RESOURCE_NOT_FOUND",
            details=details
        )
        self.resource_type = resource_type
        self.resource_id = resource_id


class ValidationError(WasteManagementError):
    """
    Raised when data validation fails.
    Single Responsibility: Data validation error handling.
    """
    
    def __init__(
        self, 
        field: str, 
        value: Any, 
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Validation error for field '{field}': {message}",
            error_code="VALIDATION_ERROR",
            details=details
        )
        self.field = field
        self.value = value


class AuthenticationError(WasteManagementError):
    """
    Raised when authentication fails.
    Single Responsibility: Authentication error handling.
    """
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationError(WasteManagementError):
    """
    Raised when authorization fails.
    Single Responsibility: Authorization error handling.
    """
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR"
        )


class ConflictError(WasteManagementError):
    """
    Raised when a resource conflict occurs.
    Single Responsibility: Resource conflict handling.
    """
    
    def __init__(
        self, 
        resource_type: str, 
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=f"Conflict with {resource_type}: {message}",
            error_code="RESOURCE_CONFLICT",
            details=details
        )
        self.resource_type = resource_type


# Business Rule Specific Exceptions

class ContractorCapacityExceededError(BusinessRuleViolationError):
    """
    Raised when contractor capacity is exceeded.
    Single Responsibility: Contractor capacity rule violation.
    """
    
    def __init__(
        self, 
        contractor_id: str, 
        requested_hours: float, 
        available_hours: float
    ):
        super().__init__(
            rule_code="CONTRACTOR_CAPACITY_001",
            message=f"Contractor capacity exceeded. Requested: {requested_hours}h, Available: {available_hours}h",
            details={
                "contractor_id": contractor_id,
                "requested_hours": requested_hours,
                "available_hours": available_hours
            }
        )


class InvalidContractorHierarchyError(BusinessRuleViolationError):
    """
    Raised when contractor hierarchy rules are violated.
    Single Responsibility: Contractor hierarchy rule violation.
    """
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            rule_code="CONTRACTOR_HIERARCHY_001",
            message=message,
            details=details
        )


class ExpiredInsuranceError(BusinessRuleViolationError):
    """
    Raised when contractor has expired insurance.
    Single Responsibility: Insurance expiry rule violation.
    """
    
    def __init__(
        self, 
        contractor_id: str, 
        expiry_date: str
    ):
        super().__init__(
            rule_code="CONTRACTOR_INSURANCE_001",
            message=f"Contractor insurance expired on {expiry_date}",
            details={
                "contractor_id": contractor_id,
                "expiry_date": expiry_date
            }
        )