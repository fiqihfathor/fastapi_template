{% if cookiecutter.use_pytest == "y" %}
import os
import pytest
from fastapi.testclient import TestClient

{% if cookiecutter.use_sqlalchemy == "y" %}
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
{% endif %}
from app.main import app

# Set test environment
os.environ["ENVIRONMENT"] = "test"

# Create test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

{% if cookiecutter.use_sqlalchemy == "y" %}
# Create test database
@pytest.fixture(scope="module")
def test_db():
    # Use in-memory SQLite for tests
    SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Override dependency
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    # Return session for test usage
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
    # Clean up
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides = {}
{% endif %}

{% if cookiecutter.use_auth == "y" %}
# Authentication helpers
@pytest.fixture(scope="module")
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
    }

@pytest.fixture(scope="module")
def test_superuser():
    return {
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin",
        "is_superuser": True,
    }

@pytest.fixture(scope="module")
def token_headers(client, test_user{% if cookiecutter.use_sqlalchemy == "y" %}, test_db{% endif %}):
    {% if cookiecutter.use_sqlalchemy == "y" %}
    # Create test user in DB
    from app.repositories.user_repository import UserRepository
    from app.schemas.user import UserCreate
    from app.core.security import get_password_hash
    
    user_repo = UserRepository()
    user_in = UserCreate(**test_user)
    hashed_password = get_password_hash(user_in.password)
    user = user_repo.create_user(test_db, user_create=user_in, hashed_password=hashed_password)
    test_db.commit()
    {% endif %}
    
    # Get token
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Return headers with token
    return {"Authorization": f"Bearer {token}"}
{% endif %}
{% endif %}
