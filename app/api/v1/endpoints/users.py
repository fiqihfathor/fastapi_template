from fastapi import APIRouter, Depends, Path, Body
from typing import List, Optional
from app.api.dependencies import get_pagination_params
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.core.exceptions import NotFoundException
from app.utils.response import success_response, pagination_response

router = APIRouter()
user_service = UserService()


@router.get("/", response_model_exclude_none=True)
async def get_users(
    pagination: tuple[int, int] = Depends(get_pagination_params),
    email: Optional[str] = None
):
    """
    Get all users with pagination.
    
    - **limit**: Maximum number of users to return
    - **offset**: Number of users to skip
    - **email**: Filter by email (optional)
    """
    limit, offset = pagination
    users, total = user_service.get_users(limit=limit, offset=offset, email=email)
    
    return pagination_response(
        items=users,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{user_id}", response_model_exclude_none=True)
async def get_user(
    user_id: int = Path(..., description="The ID of the user to get")
):
    """
    Get a specific user by ID.
    """
    user = user_service.get_user(user_id)
    if not user:
        raise NotFoundException(f"User with ID {user_id} not found")
    
    return success_response(user)


@router.post("/", status_code=201, response_model_exclude_none=True)
async def create_user(
    user_data: UserCreate = Body(...)
):
    """
    Create a new user.
    """
    user = user_service.create_user(user_data)
    return success_response(user)


@router.put("/{user_id}", response_model_exclude_none=True)
async def update_user(
    user_id: int = Path(..., description="The ID of the user to update"),
    user_data: UserUpdate = Body(...)
):
    """
    Update an existing user.
    """
    user = user_service.update_user(user_id, user_data)
    if not user:
        raise NotFoundException(f"User with ID {user_id} not found")
    
    return success_response(user)


@router.delete("/{user_id}", response_model_exclude_none=True)
async def delete_user(
    user_id: int = Path(..., description="The ID of the user to delete")
):
    """
    Delete a user.
    """
    success = user_service.delete_user(user_id)
    if not success:
        raise NotFoundException(f"User with ID {user_id} not found")
    
    return success_response({"message": f"User with ID {user_id} deleted successfully"})
