{% if cookiecutter.use_sqlalchemy == "y" and cookiecutter.use_auth == "y" %}
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """Repository for User model"""
    
    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users"""
        return db.query(User).offset(skip).limit(limit).all()
    
    def get_user(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by id"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    def create_user(self, db: Session, user_create: UserCreate, hashed_password: str) -> User:
        """Create new user"""
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            is_active=user_create.is_active,
            is_superuser=user_create.is_superuser
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update_user(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user"""
        db_user = self.get_user(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete user"""
        db_user = self.get_user(db, user_id)
        if not db_user:
            return False
        
        db.delete(db_user)
        db.commit()
        return True
{% elif cookiecutter.use_auth == "y" %}
from typing import List, Optional, Dict
import json
import os

from app.schemas.user import UserCreate, UserUpdate


class UserRepository:
    """Repository for User model"""
    
    def __init__(self):
        """Initialize with in-memory storage"""
        self.users = {}
        self.counter = 0
    
    def get_users(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all users"""
        users = list(self.users.values())
        return users[skip:skip + limit]
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user by id"""
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        for user in self.users.values():
            if user["username"] == username:
                return user
        return None
    
    def create_user(self, user_create: UserCreate, hashed_password: str) -> Dict:
        """Create new user"""
        self.counter += 1
        user = {
            "id": self.counter,
            "email": user_create.email,
            "username": user_create.username,
            "hashed_password": hashed_password,
            "is_active": user_create.is_active,
            "is_superuser": user_create.is_superuser
        }
        self.users[self.counter] = user
        return user
    
    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[Dict]:
        """Update user"""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        update_data = user_update.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            if value is not None:
                user[key] = value
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user"""
        if user_id not in self.users:
            return False
        
        del self.users[user_id]
        return True
{% endif %}
