from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.base import SessionLocal
from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository:
    """Repository for item database operations."""
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def get_items(self, limit: int, offset: int, name: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get items with pagination and optional filtering.
        
        Args:
            limit: Maximum number of items to return
            offset: Number of items to skip
            name: Filter by name (optional)
            
        Returns:
            Tuple containing list of items and total count
        """
        query = self.db.query(Item)
        
        # Apply filters if provided
        if name:
            query = query.filter(Item.name.ilike(f"%{name}%"))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        items = query.order_by(Item.id).offset(offset).limit(limit).all()
        
        # Convert to dict
        items_dict = [self._item_to_dict(item) for item in items]
        
        return items_dict, total
    
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific item by ID.
        
        Args:
            item_id: ID of the item to retrieve
            
        Returns:
            Item data or None if not found
        """
        item = self.db.query(Item).filter(Item.id == item_id).first()
        if not item:
            return None
        
        return self._item_to_dict(item)
    
    def create_item(self, item_data: ItemCreate) -> Dict[str, Any]:
        """
        Create a new item.
        
        Args:
            item_data: Item data for creation
            
        Returns:
            Created item data
        """
        item = Item(**item_data.dict())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        
        return self._item_to_dict(item)
    
    def update_item(self, item_id: int, item_data: ItemUpdate) -> Dict[str, Any]:
        """
        Update an existing item.
        
        Args:
            item_id: ID of the item to update
            item_data: Item data for update
            
        Returns:
            Updated item data
        """
        item = self.db.query(Item).filter(Item.id == item_id).first()
        
        # Update only provided fields
        update_data = item_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        
        self.db.commit()
        self.db.refresh(item)
        
        return self._item_to_dict(item)
    
    def delete_item(self, item_id: int) -> bool:
        """
        Delete an item.
        
        Args:
            item_id: ID of the item to delete
            
        Returns:
            True if deleted
        """
        item = self.db.query(Item).filter(Item.id == item_id).first()
        self.db.delete(item)
        self.db.commit()
        
        return True
    
    def _item_to_dict(self, item: Item) -> Dict[str, Any]:
        """Convert an Item model to a dictionary."""
        return {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "is_active": item.is_active,
            "created_at": item.created_at,
            "updated_at": item.updated_at
        }
