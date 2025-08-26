from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """Base schema for Item."""
    name: str = Field(..., description="Item name", example="Sample Item")
    description: Optional[str] = Field(None, description="Item description", example="This is a sample item")
    price: int = Field(..., description="Item price in cents", example=1000)
    is_active: bool = Field(True, description="Whether the item is active")


class ItemCreate(ItemBase):
    """Schema for creating a new Item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an Item."""
    name: Optional[str] = Field(None, description="Item name", example="Updated Item")
    description: Optional[str] = Field(None, description="Item description", example="This is an updated item")
    price: Optional[int] = Field(None, description="Item price in cents", example=1500)
    is_active: Optional[bool] = Field(None, description="Whether the item is active")


class ItemResponse(ItemBase):
    """Schema for Item response."""
    id: int = Field(..., description="Item ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True
