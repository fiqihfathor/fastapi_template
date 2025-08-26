from fastapi import Depends, Query
from typing import Optional
from app.core.config import settings
from app.core.exceptions import ValidationException


def get_pagination_params(
    limit: int = Query(
        default=settings.DEFAULT_LIMIT,
        ge=1,
        le=settings.MAX_LIMIT,
        description="Number of items to return per page"
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of items to skip (offset)"
    )
) -> tuple[int, int]:
    """
    Dependency for pagination parameters.
    Returns a tuple of (limit, offset).
    """
    if limit > settings.MAX_LIMIT:
        raise ValidationException(f"Maximum limit is {settings.MAX_LIMIT}")
    
    return limit, offset
