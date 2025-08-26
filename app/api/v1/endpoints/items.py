from fastapi import APIRouter, Depends, Path, Body
from typing import List, Optional
from app.api.dependencies import get_pagination_params
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService
from app.core.exceptions import NotFoundException
from app.utils.response import success_response, pagination_response

router = APIRouter()
item_service = ItemService()


@router.get("/", response_model_exclude_none=True)
async def get_items(
    pagination: tuple[int, int] = Depends(get_pagination_params),
    name: Optional[str] = None
):
    """
    Get all items with pagination.
    
    - **limit**: Maximum number of items to return
    - **offset**: Number of items to skip
    - **name**: Filter by name (optional)
    """
    limit, offset = pagination
    items, total = item_service.get_items(limit=limit, offset=offset, name=name)
    
    return pagination_response(
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )


@router.get("/{item_id}", response_model_exclude_none=True)
async def get_item(
    item_id: int = Path(..., description="The ID of the item to get")
):
    """
    Get a specific item by ID.
    """
    item = item_service.get_item(item_id)
    if not item:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    return success_response(item)


@router.post("/", status_code=201, response_model_exclude_none=True)
async def create_item(
    item_data: ItemCreate = Body(...)
):
    """
    Create a new item.
    """
    item = item_service.create_item(item_data)
    return success_response(item)


@router.put("/{item_id}", response_model_exclude_none=True)
async def update_item(
    item_id: int = Path(..., description="The ID of the item to update"),
    item_data: ItemUpdate = Body(...)
):
    """
    Update an existing item.
    """
    item = item_service.update_item(item_id, item_data)
    if not item:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    return success_response(item)


@router.delete("/{item_id}", response_model_exclude_none=True)
async def delete_item(
    item_id: int = Path(..., description="The ID of the item to delete")
):
    """
    Delete an item.
    """
    success = item_service.delete_item(item_id)
    if not success:
        raise NotFoundException(f"Item with ID {item_id} not found")
    
    return success_response({"message": f"Item with ID {item_id} deleted successfully"})
