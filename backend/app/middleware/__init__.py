"""
Middleware package for the Waste Management Intelligence System.
Single Responsibility: Request/response processing middleware.
"""

from .error_middleware import ErrorHandlerMiddleware

__all__ = [
    "ErrorHandlerMiddleware",
]