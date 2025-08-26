from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from app.models.base import SessionLocal
from app.models.user import User


class UserRepository:
    """Repository for user database operations."""
    
    def __init__(self):
        self.db: Session = SessionLocal()
    
    def get_users(self, limit: int, offset: int, email: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
        """
        Get users with pagination and optional filtering.
        
        Args:
            limit: Maximum number of users to return
            offset: Number of users to skip
            email: Filter by email (optional)
            
        Returns:
            Tuple containing list of users and total count
        """
        query = self.db.query(User)
        
        # Apply filters if provided
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        users = query.order_by(User.id).offset(offset).limit(limit).all()
        
        # Convert to dict
        users_dict = [self._user_to_dict(user) for user in users]
        
        return users_dict, total
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific user by ID.
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            User data or None if not found
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None
        
        return self._user_to_dict(user)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific user by email.
        
        Args:
            email: Email of the user to retrieve
            
        Returns:
            User data or None if not found
        """
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        return self._user_to_dict(user)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            user_data: User data for creation
            
        Returns:
            Created user data
        """
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return self._user_to_dict(user)
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing user.
        
        Args:
            user_id: ID of the user to update
            user_data: User data for update
            
        Returns:
            Updated user data
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        
        # Update only provided fields
        for key, value in user_data.items():
            setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        
        return self._user_to_dict(user)
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            True if deleted
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        self.db.delete(user)
        self.db.commit()
        
        return True
    
    def _user_to_dict(self, user: User) -> Dict[str, Any]:
        """Convert a User model to a dictionary."""
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
