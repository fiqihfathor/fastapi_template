{% if cookiecutter.use_auth == "y" %}
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

{% if cookiecutter.use_sqlalchemy == "y" %}
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
{% endif %}
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.token import Token

router = APIRouter()
user_repository = UserRepository()


@router.post("/login", response_model=Token)
def login_for_access_token(
    {% if cookiecutter.use_sqlalchemy == "y" %}
    db: Session = Depends(get_db),
    {% endif %}
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Try to authenticate with username
    {% if cookiecutter.use_sqlalchemy == "y" %}
    user = user_repository.get_user_by_username(db, username=form_data.username)
    {% else %}
    user = user_repository.get_user_by_username(username=form_data.username)
    {% endif %}
    
    # If user not found by username, try with email
    if not user:
        {% if cookiecutter.use_sqlalchemy == "y" %}
        user = user_repository.get_user_by_email(db, email=form_data.username)
        {% else %}
        user = user_repository.get_user_by_email(email=form_data.username)
        {% endif %}
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
{% endif %}
