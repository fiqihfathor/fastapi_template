{% if cookiecutter.use_auth == "y" %}
from typing import Optional, List
from pydantic import BaseModel, EmailStr

from app.schemas.item import ItemResponse


class UserBase(BaseModel):
    """Base schema for User"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserCreate(UserBase):
    """Schema for creating User"""
    email: EmailStr
    username: str
    password: str


class UserUpdate(UserBase):
    """Schema for updating User"""
    password: Optional[str] = None


class UserResponse(UserBase):
    """Schema for User response"""
    id: int
    email: EmailStr
    username: str

    class Config:
        {% if cookiecutter.use_sqlalchemy == "y" %}
        from_attributes = True
        {% else %}
        from_attributes = False
        {% endif %}


class UserWithItems(UserResponse):
    """Schema for User with Items"""
    items: List[ItemResponse] = []
{% endif %}
