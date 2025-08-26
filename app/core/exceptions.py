from fastapi import HTTPException
from typing import Any, Dict, Optional


class CustomException(HTTPException):
    """
    Custom exception class that extends FastAPI's HTTPException
    with additional fields for standardized error responses.
    """
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None,
        error_type: str = "ERROR"
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_type = error_type


class NotFoundException(CustomException):
    """Exception raised when a resource is not found."""
    def __init__(
        self,
        detail: str = "Resource not found",
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            status_code=404,
            detail=detail,
            headers=headers,
            error_type="NOT_FOUND"
        )


class ValidationException(CustomException):
    """Exception raised for validation errors."""
    def __init__(
        self,
        detail: Any = "Validation error",
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            status_code=422,
            detail=detail,
            headers=headers,
            error_type="VALIDATION_ERROR"
        )


class UnauthorizedException(CustomException):
    """Exception raised for authentication errors."""
    def __init__(
        self,
        detail: str = "Not authenticated",
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            status_code=401,
            detail=detail,
            headers=headers,
            error_type="UNAUTHORIZED"
        )


class ForbiddenException(CustomException):
    """Exception raised for authorization errors."""
    def __init__(
        self,
        detail: str = "Not authorized to perform this action",
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            status_code=403,
            detail=detail,
            headers=headers,
            error_type="FORBIDDEN"
        )


class DatabaseException(CustomException):
    """Exception raised for database errors."""
    def __init__(
        self,
        detail: str = "Database error",
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            status_code=500,
            detail=detail,
            headers=headers,
            error_type="DATABASE_ERROR"
        )
