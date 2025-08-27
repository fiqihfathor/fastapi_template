from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    """Base schema for Item"""
    title: str
    description: Optional[str] = None
    is_active: Optional[bool] = True


class ItemCreate(ItemBase):
    """Schema for creating Item"""
    pass


class ItemUpdate(ItemBase):
    """Schema for updating Item"""
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ItemResponse(ItemBase):
    """Schema for Item response"""
    id: int
    {% if cookiecutter.use_auth == "y" %}
    owner_id: Optional[int] = None
    {% endif %}

    class Config:
        {% if cookiecutter.use_sqlalchemy == "y" %}
        from_attributes = True
        {% else %}
        from_attributes = False
        {% endif %}
