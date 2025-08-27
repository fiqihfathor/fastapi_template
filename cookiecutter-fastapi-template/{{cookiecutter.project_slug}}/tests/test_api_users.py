{% if cookiecutter.use_pytest == "y" and cookiecutter.use_auth == "y" %}
import pytest
from fastapi.testclient import TestClient

def test_create_user(client{% if cookiecutter.use_sqlalchemy == "y" %}, test_db{% endif %}):
    """Test creating a new user"""
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword",
    }
    response = client.post("/api/v1/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data

def test_read_users_me(client, token_headers):
    """Test reading current user info"""
    response = client.get("/api/v1/users/me", headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data

def test_update_user_me(client, token_headers):
    """Test updating current user info"""
    update_data = {
        "username": "updateduser",
        "email": "updated@example.com",
    }
    response = client.put("/api/v1/users/me", json=update_data, headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == update_data["username"]
    assert data["email"] == update_data["email"]
    assert "hashed_password" not in data

def test_update_user_password(client, token_headers):
    """Test updating user password"""
    update_data = {
        "current_password": "testpassword",
        "new_password": "newtestpassword",
    }
    response = client.put("/api/v1/users/me/password", json=update_data, headers=token_headers)
    assert response.status_code == 200
    
    # Test login with new password
    login_data = {
        "username": "updated@example.com",  # From previous test
        "password": "newtestpassword",
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_with_email(client, test_user{% if cookiecutter.use_sqlalchemy == "y" %}, test_db{% endif %}):
    """Test login with email"""
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_with_username(client, test_user{% if cookiecutter.use_sqlalchemy == "y" %}, test_db{% endif %}):
    """Test login with username"""
    login_data = {
        "username": test_user["username"],
        "password": test_user["password"],
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_incorrect_password(client, test_user):
    """Test login with incorrect password"""
    login_data = {
        "username": test_user["email"],
        "password": "wrongpassword",
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
{% endif %}
