{% if cookiecutter.use_sqlalchemy == "y" %}
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository:
    """Repository for Item model"""
    
    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get all items"""
        return db.query(Item).offset(skip).limit(limit).all()
    
    def get_item(self, db: Session, item_id: int) -> Optional[Item]:
        """Get item by id"""
        return db.query(Item).filter(Item.id == item_id).first()
    
    def create_item(self, db: Session, item_create: ItemCreate, owner_id: Optional[int] = None) -> Item:
        """Create new item"""
        db_item = Item(
            title=item_create.title,
            description=item_create.description,
            is_active=item_create.is_active,
            owner_id=owner_id
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def update_item(self, db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
        """Update item"""
        db_item = self.get_item(db, item_id)
        if not db_item:
            return None
        
        update_data = item_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_item, key, value)
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def delete_item(self, db: Session, item_id: int) -> bool:
        """Delete item"""
        db_item = self.get_item(db, item_id)
        if not db_item:
            return False
        
        db.delete(db_item)
        db.commit()
        return True
{% else %}
from typing import List, Optional, Dict
import json
import os

from app.schemas.item import ItemCreate, ItemUpdate


class ItemRepository:
    """Repository for Item model"""
    
    def __init__(self):
        """Initialize with in-memory storage"""
        self.items = {}
        self.counter = 0
    
    def get_items(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all items"""
        items = list(self.items.values())
        return items[skip:skip + limit]
    
    def get_item(self, item_id: int) -> Optional[Dict]:
        """Get item by id"""
        return self.items.get(item_id)
    
    def create_item(self, item_create: ItemCreate, owner_id: Optional[int] = None) -> Dict:
        """Create new item"""
        self.counter += 1
        item = {
            "id": self.counter,
            "title": item_create.title,
            "description": item_create.description,
            "is_active": item_create.is_active,
            "owner_id": owner_id
        }
        self.items[self.counter] = item
        return item
    
    def update_item(self, item_id: int, item_update: ItemUpdate) -> Optional[Dict]:
        """Update item"""
        if item_id not in self.items:
            return None
        
        item = self.items[item_id]
        update_data = item_update.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            if value is not None:
                item[key] = value
        
        return item
    
    def delete_item(self, item_id: int) -> bool:
        """Delete item"""
        if item_id not in self.items:
            return False
        
        del self.items[item_id]
        return True
{% endif %}
