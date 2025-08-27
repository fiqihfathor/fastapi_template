{% if cookiecutter.use_sqlalchemy == "y" %}
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.models.base import Base


class Item(Base):
    """Item model"""
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    
    {% if cookiecutter.use_auth == "y" %}
    # Example of relationship with User model
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
    {% endif %}
{% else %}
# Item model placeholder for non-SQLAlchemy projects
class Item:
    """Item model"""
    
    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        is_active: bool = True,
        owner_id: int = None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.is_active = is_active
        self.owner_id = owner_id
{% endif %}
