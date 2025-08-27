{% if cookiecutter.use_sqlalchemy == "y" and cookiecutter.use_auth == "y" %}
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    """User model"""
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Example of relationship with Item model
    items = relationship("Item", back_populates="owner")
{% elif cookiecutter.use_auth == "y" %}
# User model placeholder for non-SQLAlchemy projects
class User:
    """User model"""
    
    def __init__(
        self,
        id: int,
        email: str,
        username: str,
        hashed_password: str,
        is_active: bool = True,
        is_superuser: bool = False
    ):
        self.id = id
        self.email = email
        self.username = username
        self.hashed_password = hashed_password
        self.is_active = is_active
        self.is_superuser = is_superuser
{% endif %}
