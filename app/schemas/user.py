from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base schema for User."""
    email: EmailStr = Field(..., description="User email", example="user@example.com")
    username: str = Field(..., description="Username", example="johndoe")
    is_active: bool = Field(True, description="Whether the user is active")
    is_superuser: bool = Field(False, description="Whether the user is a superuser")


class UserCreate(UserBase):
    """Schema for creating a new User."""
    password: str = Field(..., description="User password", example="strongpassword123")


class UserUpdate(BaseModel):
    """Schema for updating a User."""
    email: Optional[EmailStr] = Field(None, description="User email", example="newuser@example.com")
    username: Optional[str] = Field(None, description="Username", example="newjohndoe")
    password: Optional[str] = Field(None, description="User password", example="newstrongpassword123")
    is_active: Optional[bool] = Field(None, description="Whether the user is active")
    is_superuser: Optional[bool] = Field(None, description="Whether the user is a superuser")


class UserResponse(UserBase):
    """Schema for User response."""
    id: int = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
