{% if cookiecutter.use_auth == "y" %}
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

{% if cookiecutter.use_sqlalchemy == "y" %}
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
{% endif %}
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserWithItems
from app.api.dependencies import get_current_user
from app.core.security import get_password_hash

router = APIRouter()
user_repository = UserRepository()


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get all users
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    users = user_repository.get_users(db, skip=skip, limit=limit)
    {% else %}
    users = user_repository.get_users(skip=skip, limit=limit)
    {% endif %}
    return users


@router.get("/me", response_model=UserResponse)
def get_user_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Get current user
    """
    return current_user


@router.get("/me/items", response_model=UserWithItems)
def get_user_items(
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get items for current user
    """
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.get_user(db, user_id=current_user.id)
    {% else %}
    user = user_repository.get_user(user_id=current_user.id)
    {% endif %}
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Get user by ID
    """
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.get_user(db, user_id=user_id)
    {% else %}
    user = user_repository.get_user(user_id=user_id)
    {% endif %}
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Create new user
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.get_user_by_email(db, email=user_create.email)
    {% else %}
    user = user_repository.get_user_by_email(email=user_create.email)
    {% endif %}
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.get_user_by_username(db, username=user_create.username)
    {% else %}
    user = user_repository.get_user_by_username(username=user_create.username)
    {% endif %}
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user_create.password)
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.create_user(db, user_create=user_create, hashed_password=hashed_password)
    {% else %}
    user = user_repository.create_user(user_create=user_create, hashed_password=hashed_password)
    {% endif %}
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Update user
    """
    if not current_user.is_superuser and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.get_user(db, user_id=user_id)
    {% else %}
    user = user_repository.get_user(user_id=user_id)
    {% endif %}
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user_update.password:
        hashed_password = get_password_hash(user_update.password)
        user_update.password = hashed_password
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    updated_user = user_repository.update_user(db, user_id=user_id, user_update=user_update)
    {% else %}
    updated_user = user_repository.update_user(user_id=user_id, user_update=user_update)
    {% endif %}
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    current_user: UserResponse = Depends(get_current_user)
):
    """
    Delete user
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.get_user(db, user_id=user_id)
    {% else %}
    user = user_repository.get_user(user_id=user_id)
    {% endif %}
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user_repository.delete_user(db, user_id=user_id)
    {% else %}
    user_repository.delete_user(user_id=user_id)
    {% endif %}
{% endif %}
