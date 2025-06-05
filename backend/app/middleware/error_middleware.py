"""
Error handling middleware only.
Single Responsibility: Global error handling and response formatting.
"""

import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from ..exceptions import (
    WasteManagementError,
    BusinessRuleViolationError,
    NotFoundError,
    ValidationError,
    AuthenticationError,
    AuthorizationError
)
from ..schemas.base_schemas import ErrorResponse

logger = logging.getLogger("app.middleware.error")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.
    Single Responsibility: Convert exceptions to proper HTTP responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and handle any exceptions.
        Single Responsibility: Exception to HTTP response conversion.
        """
        try:
            response = await call_next(request)
            return response
        
        except BusinessRuleViolationError as e:
            logger.warning(f"Business rule violation: {e.message}", extra={
                "rule_code": e.rule_code,
                "details": e.details,
                "path": request.url.path
            })
            
            error_response = ErrorResponse(
                error_code=e.error_code,
                message=e.message,
                details=e.details
            )
            
            return JSONResponse(
                status_code=422,  # Unprocessable Entity
                content=error_response.dict()
            )
        
        except NotFoundError as e:
            logger.info(f"Resource not found: {e.message}", extra={
                "resource_type": e.resource_type,
                "resource_id": e.resource_id,
                "path": request.url.path
            })
            
            error_response = ErrorResponse(
                error_code=e.error_code,
                message=e.message,
                details=e.details
            )
            
            return JSONResponse(
                status_code=404,
                content=error_response.dict()
            )
        
        except ValidationError as e:
            logger.warning(f"Validation error: {e.message}", extra={
                "field": e.field,
                "value": e.value,
                "path": request.url.path
            })
            
            error_response = ErrorResponse(
                error_code=e.error_code,
                message=e.message,
                details=e.details
            )
            
            return JSONResponse(
                status_code=400,  # Bad Request
                content=error_response.dict()
            )
        
        except AuthenticationError as e:
            logger.warning(f"Authentication error: {e.message}", extra={
                "path": request.url.path,
                "user_agent": request.headers.get("user-agent")
            })
            
            error_response = ErrorResponse(
                error_code=e.error_code,
                message=e.message,
                details=e.details
            )
            
            return JSONResponse(
                status_code=401,  # Unauthorized
                content=error_response.dict()
            )
        
        except AuthorizationError as e:
            logger.warning(f"Authorization error: {e.message}", extra={
                "path": request.url.path
            })
            
            error_response = ErrorResponse(
                error_code=e.error_code,
                message=e.message,
                details=e.details
            )
            
            return JSONResponse(
                status_code=403,  # Forbidden
                content=error_response.dict()
            )
        
        except WasteManagementError as e:
            logger.error(f"Application error: {e.message}", extra={
                "error_code": e.error_code,
                "details": e.details,
                "path": request.url.path
            })
            
            error_response = ErrorResponse(
                error_code=e.error_code or "INTERNAL_ERROR",
                message=e.message,
                details=e.details
            )
            
            return JSONResponse(
                status_code=500,  # Internal Server Error
                content=error_response.dict()
            )
        
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", extra={
                "path": request.url.path,
                "exception_type": type(e).__name__
            }, exc_info=True)
            
            error_response = ErrorResponse(
                error_code="INTERNAL_ERROR",
                message="An unexpected error occurred",
                details={"exception_type": type(e).__name__}
            )
            
            return JSONResponse(
                status_code=500,
                content=error_response.dict()
            )