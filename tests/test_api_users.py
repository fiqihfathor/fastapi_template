import pytest
from fastapi.testclient import TestClient
from app.models.user import User


def test_create_user(client, db_session):
    """Test creating a new user."""
    # Test data
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "is_active": True,
        "is_superuser": False
    }
    
    # Make request
    response = client.post("/api/v1/users/", json=user_data)
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert data["data"]["email"] == user_data["email"]
    assert data["data"]["username"] == user_data["username"]
    assert data["data"]["is_active"] == user_data["is_active"]
    assert data["data"]["is_superuser"] == user_data["is_superuser"]
    assert "id" in data["data"]
    assert "hashed_password" not in data["data"]  # Password should not be returned
    
    # Check database
    db_user = db_session.query(User).filter(User.id == data["data"]["id"]).first()
    assert db_user is not None
    assert db_user.email == user_data["email"]
    assert db_user.username == user_data["username"]
    assert db_user.hashed_password is not None  # Password should be hashed
    assert db_user.hashed_password != user_data["password"]  # Password should not be stored in plain text


def test_get_users(client, db_session):
    """Test getting a list of users."""
    # Create test users with hashed passwords
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    users = [
        User(
            email="user1@example.com", 
            username="user1", 
            hashed_password=pwd_context.hash("password1")
        ),
        User(
            email="user2@example.com", 
            username="user2", 
            hashed_password=pwd_context.hash("password2")
        ),
        User(
            email="user3@example.com", 
            username="user3", 
            hashed_password=pwd_context.hash("password3")
        ),
    ]
    db_session.add_all(users)
    db_session.commit()
    
    # Make request
    response = client.get("/api/v1/users/")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert "items" in data["data"]
    assert "pagination" in data["data"]
    assert len(data["data"]["items"]) == 3
    assert data["data"]["pagination"]["total"] == 3
    assert data["data"]["pagination"]["has_more"] is False
    
    # Check that no passwords are returned
    for user in data["data"]["items"]:
        assert "hashed_password" not in user


def test_get_user(client, db_session):
    """Test getting a specific user."""
    # Create test user
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = User(
        email="test@example.com", 
        username="testuser", 
        hashed_password=pwd_context.hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Make request
    response = client.get(f"/api/v1/users/{user.id}")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert data["data"]["id"] == user.id
    assert data["data"]["email"] == user.email
    assert data["data"]["username"] == user.username
    assert "hashed_password" not in data["data"]  # Password should not be returned


def test_update_user(client, db_session):
    """Test updating a user."""
    # Create test user
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = User(
        email="original@example.com", 
        username="originaluser", 
        hashed_password=pwd_context.hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Update data
    update_data = {
        "email": "updated@example.com",
        "username": "updateduser",
        "password": "newpassword123"
    }
    
    # Make request
    response = client.put(f"/api/v1/users/{user.id}", json=update_data)
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert data["data"]["id"] == user.id
    assert data["data"]["email"] == update_data["email"]
    assert data["data"]["username"] == update_data["username"]
    
    # Check database
    db_user = db_session.query(User).filter(User.id == user.id).first()
    assert db_user.email == update_data["email"]
    assert db_user.username == update_data["username"]
    assert db_user.hashed_password != user.hashed_password  # Password should be updated


def test_delete_user(client, db_session):
    """Test deleting a user."""
    # Create test user
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    user = User(
        email="delete@example.com", 
        username="deleteuser", 
        hashed_password=pwd_context.hash("password123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    # Make request
    response = client.delete(f"/api/v1/users/{user.id}")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert "message" in data["data"]
    
    # Check database
    db_user = db_session.query(User).filter(User.id == user.id).first()
    assert db_user is None
