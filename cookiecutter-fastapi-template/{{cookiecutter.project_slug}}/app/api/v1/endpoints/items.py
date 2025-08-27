from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status

{% if cookiecutter.use_sqlalchemy == "y" %}
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
{% endif %}
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
{% if cookiecutter.use_auth == "y" %}
from app.api.dependencies import get_current_user
from app.schemas.user import UserResponse
{% endif %}

router = APIRouter()
item_repository = ItemRepository()


@router.get("/", response_model=List[ItemResponse])
def get_items(
    skip: int = 0,
    limit: int = 100,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db)
    {% endif %}
):
    """
    Get all items
    """
    {% if cookiecutter.use_sqlalchemy == "y" %}
    items = item_repository.get_items(db, skip=skip, limit=limit)
    {% else %}
    items = item_repository.get_items(skip=skip, limit=limit)
    {% endif %}
    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db)
    {% endif %}
):
    """
    Get item by ID
    """
    {% if cookiecutter.use_sqlalchemy == "y" %}
    item = item_repository.get_item(db, item_id=item_id)
    {% else %}
    item = item_repository.get_item(item_id=item_id)
    {% endif %}
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item_create: ItemCreate,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    {% if cookiecutter.use_auth == "y" %}
    current_user: UserResponse = Depends(get_current_user)
    {% endif %}
):
    """
    Create new item
    """
    {% if cookiecutter.use_sqlalchemy == "y" and cookiecutter.use_auth == "y" %}
    item = item_repository.create_item(db, item_create=item_create, owner_id=current_user.id)
    {% elif cookiecutter.use_sqlalchemy == "y" %}
    item = item_repository.create_item(db, item_create=item_create)
    {% elif cookiecutter.use_auth == "y" %}
    item = item_repository.create_item(item_create=item_create, owner_id=current_user.id)
    {% else %}
    item = item_repository.create_item(item_create=item_create)
    {% endif %}
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    {% if cookiecutter.use_auth == "y" %}
    current_user: UserResponse = Depends(get_current_user)
    {% endif %}
):
    """
    Update item
    """
    {% if cookiecutter.use_sqlalchemy == "y" %}
    item = item_repository.get_item(db, item_id=item_id)
    {% else %}
    item = item_repository.get_item(item_id=item_id)
    {% endif %}
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    {% if cookiecutter.use_auth == "y" %}
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    {% endif %}
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    updated_item = item_repository.update_item(db, item_id=item_id, item_update=item_update)
    {% else %}
    updated_item = item_repository.update_item(item_id=item_id, item_update=item_update)
    {% endif %}
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    {% if cookiecutter.use_auth == "y" %}
    current_user: UserResponse = Depends(get_current_user)
    {% endif %}
):
    """
    Delete item
    """
    {% if cookiecutter.use_sqlalchemy == "y" %}
    item = item_repository.get_item(db, item_id=item_id)
    {% else %}
    item = item_repository.get_item(item_id=item_id)
    {% endif %}
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    {% if cookiecutter.use_auth == "y" %}
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    {% endif %}
    
    {% if cookiecutter.use_sqlalchemy == "y" %}
    item_repository.delete_item(db, item_id=item_id)
    {% else %}
    item_repository.delete_item(item_id=item_id)
    {% endif %}
