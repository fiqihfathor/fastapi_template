from typing import List, Optional, Tuple, Dict, Any
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundException, DatabaseException
from passlib.context import CryptContext


class UserService:
    """Service for user operations."""
    
    def __init__(self):
        self.repository = UserRepository()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
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
        try:
            return self.repository.get_users(limit, offset, email)
        except Exception as e:
            raise DatabaseException(f"Error retrieving users: {str(e)}")
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific user by ID.
        
        Args:
            user_id: ID of the user to retrieve
            
        Returns:
            User data or None if not found
        """
        try:
            return self.repository.get_user(user_id)
        except Exception as e:
            raise DatabaseException(f"Error retrieving user: {str(e)}")
    
    def create_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            user_data: User data for creation
            
        Returns:
            Created user data
        """
        try:
            # Hash the password
            hashed_password = self.pwd_context.hash(user_data.password)
            
            # Create user with hashed password
            user_dict = user_data.dict()
            user_dict.pop("password")
            user_dict["hashed_password"] = hashed_password
            
            return self.repository.create_user(user_dict)
        except Exception as e:
            raise DatabaseException(f"Error creating user: {str(e)}")
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[Dict[str, Any]]:
        """
        Update an existing user.
        
        Args:
            user_id: ID of the user to update
            user_data: User data for update
            
        Returns:
            Updated user data or None if not found
        """
        try:
            user = self.repository.get_user(user_id)
            if not user:
                return None
            
            # Handle password update if provided
            user_dict = user_data.dict(exclude_unset=True)
            if "password" in user_dict:
                user_dict["hashed_password"] = self.pwd_context.hash(user_dict.pop("password"))
            
            return self.repository.update_user(user_id, user_dict)
        except Exception as e:
            raise DatabaseException(f"Error updating user: {str(e)}")
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user.
        
        Args:
            user_id: ID of the user to delete
            
        Returns:
            True if deleted, False if not found
        """
        try:
            user = self.repository.get_user(user_id)
            if not user:
                return False
            
            return self.repository.delete_user(user_id)
        except Exception as e:
            raise DatabaseException(f"Error deleting user: {str(e)}")
            
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        return self.pwd_context.verify(plain_password, hashed_password)
