from fastapi import status

class CustomException(Exception):
    """Base class for custom exceptions"""
    
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        self.detail = detail
        self.status_code = status_code


class NotFoundException(CustomException):
    """Exception raised when a resource is not found"""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(CustomException):
    """Exception raised when authentication fails"""
    
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(CustomException):
    """Exception raised when user doesn't have permission"""
    
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)


class BadRequestException(CustomException):
    """Exception raised when request is invalid"""
    
    def __init__(self, detail: str = "Bad request"):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)


class DatabaseException(CustomException):
    """Exception raised when database operation fails"""
    
    def __init__(self, detail: str = "Database error"):
        super().__init__(detail=detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
