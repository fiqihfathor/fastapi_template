import os
import sys
import uvicorn
from pathlib import Path

# Add parent directory to path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent))

from app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.ENVIRONMENT == "development",
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower(),
    )
