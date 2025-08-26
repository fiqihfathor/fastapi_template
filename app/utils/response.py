from typing import Any, Dict, List, Optional


def success_response(data: Any) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: The data to include in the response
        
    Returns:
        Standardized response dictionary
    """
    return {
        "responseCode": "200",
        "responseStatus": "SUCCESS",
        "data": data
    }


def error_response(status_code: str, error_type: str, message: str) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        status_code: HTTP status code as string
        error_type: Type of error (e.g., "VALIDATION_ERROR", "NOT_FOUND")
        message: Error message
        
    Returns:
        Standardized error response dictionary
    """
    return {
        "responseCode": status_code,
        "responseStatus": error_type,
        "data": {"message": message}
    }


def validation_error_response(errors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a standardized validation error response.
    
    Args:
        errors: List of validation errors
        
    Returns:
        Standardized validation error response dictionary
    """
    return {
        "responseCode": "422",
        "responseStatus": "VALIDATION_ERROR",
        "data": {"errors": errors}
    }


def pagination_response(items: List[Any], total: int, limit: int, offset: int) -> Dict[str, Any]:
    """
    Create a standardized pagination response.
    
    Args:
        items: List of items for the current page
        total: Total number of items
        limit: Maximum number of items per page
        offset: Number of items skipped
        
    Returns:
        Standardized pagination response dictionary
    """
    has_more = offset + limit < total
    
    return {
        "responseCode": "200",
        "responseStatus": "SUCCESS",
        "data": {
            "items": items,
            "pagination": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "has_more": has_more
            }
        }
    }
