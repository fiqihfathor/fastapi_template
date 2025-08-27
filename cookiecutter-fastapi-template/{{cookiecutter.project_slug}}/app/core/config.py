from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "{{ cookiecutter.project_name }}"
    APP_VERSION: str = "{{ cookiecutter.version }}"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-here"
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = "{% if cookiecutter.use_postgres == 'y' %}postgresql://postgres:postgres@localhost:5432/{{ cookiecutter.project_slug }}{% else %}sqlite:///./{{ cookiecutter.project_slug }}.db{% endif %}"

    {% if cookiecutter.use_auth == "y" %}
    # JWT
    JWT_SECRET_KEY: str = "your-jwt-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    {% endif %}

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
