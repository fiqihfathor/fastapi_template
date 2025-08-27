{% if cookiecutter.use_sqlalchemy == "y" %}
import logging
from sqlalchemy.orm import Session

from app.core.database import Base, engine
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """Initialize database with first superuser"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    {% if cookiecutter.use_auth == "y" %}
    # Create first superuser
    user_repository = UserRepository()
    user = user_repository.get_user_by_email(db, email="admin@example.com")
    
    if not user:
        user_in = UserCreate(
            email="admin@example.com",
            username="admin",
            password="admin",
            is_superuser=True,
        )
        hashed_password = get_password_hash(user_in.password)
        user_repository.create_user(db, user_create=user_in, hashed_password=hashed_password)
        logger.info("Superuser created")
    else:
        logger.info("Superuser already exists")
    {% endif %}
    
    logger.info("Database initialized")
{% endif %}
