{% if cookiecutter.use_sqlalchemy == "y" %}
import logging
import sys
from pathlib import Path

# Add parent directory to path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.init_db import init_db


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Run database initialization script
    """
    logger.info("Creating initial data")
    db = SessionLocal()
    try:
        init_db(db)
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        db.close()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
{% endif %}
