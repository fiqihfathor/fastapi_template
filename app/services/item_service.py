from typing import List, Optional, Tuple, Dict, Any
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate
from app.core.exceptions import NotFoundException, DatabaseException


class ItemService:
    """Service for item operations."""
    
    def __init__(self):
        self.repository = ItemRepository()
    
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
        try:
            return self.repository.get_items(limit, offset, name)
        except Exception as e:
            raise DatabaseException(f"Error retrieving items: {str(e)}")
    
    def get_item(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific item by ID.
        
        Args:
            item_id: ID of the item to retrieve
            
        Returns:
            Item data or None if not found
        """
        try:
            return self.repository.get_item(item_id)
        except Exception as e:
            raise DatabaseException(f"Error retrieving item: {str(e)}")
    
    def create_item(self, item_data: ItemCreate) -> Dict[str, Any]:
        """
        Create a new item.
        
        Args:
            item_data: Item data for creation
            
        Returns:
            Created item data
        """
        try:
            return self.repository.create_item(item_data)
        except Exception as e:
            raise DatabaseException(f"Error creating item: {str(e)}")
    
    def update_item(self, item_id: int, item_data: ItemUpdate) -> Optional[Dict[str, Any]]:
        """
        Update an existing item.
        
        Args:
            item_id: ID of the item to update
            item_data: Item data for update
            
        Returns:
            Updated item data or None if not found
        """
        try:
            item = self.repository.get_item(item_id)
            if not item:
                return None
            
            return self.repository.update_item(item_id, item_data)
        except Exception as e:
            raise DatabaseException(f"Error updating item: {str(e)}")
    
    def delete_item(self, item_id: int) -> bool:
        """
        Delete an item.
        
        Args:
            item_id: ID of the item to delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            item = self.repository.get_item(item_id)
            if not item:
                return False
            
            return self.repository.delete_item(item_id)
        except Exception as e:
            raise DatabaseException(f"Error deleting item: {str(e)}")
