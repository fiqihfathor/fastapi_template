from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "FastAPI Template")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "A FastAPI project template with best practices")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [origin.strip() for origin in 
                           os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").replace('[', '').replace(']', '').replace('"', '').split(',')]
    
    # Database Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # Security Settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7))  # Default: 7 days
    
    # Pagination Settings
    DEFAULT_LIMIT: int = int(os.getenv("DEFAULT_LIMIT", 10))
    MAX_LIMIT: int = int(os.getenv("MAX_LIMIT", 100))

    class Config:
        case_sensitive = True


# Create settings instance
settings = Settings()
