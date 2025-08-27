{% if cookiecutter.use_pytest == "y" %}
import pytest
from fastapi.testclient import TestClient

{% if cookiecutter.use_auth == "y" %}
def test_read_items(client, token_headers):
    """Test reading items with authentication"""
    response = client.get("/api/v1/items/", headers=token_headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item(client, token_headers):
    """Test creating a new item with authentication"""
    item_data = {
        "title": "Test Item",
        "description": "This is a test item",
    }
    response = client.post("/api/v1/items/", json=item_data, headers=token_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert "id" in data
    
    # Test reading the created item
    item_id = data["id"]
    response = client.get(f"/api/v1/items/{item_id}", headers=token_headers)
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_update_item(client, token_headers):
    """Test updating an item with authentication"""
    # First create an item
    item_data = {
        "title": "Item to Update",
        "description": "This item will be updated",
    }
    response = client.post("/api/v1/items/", json=item_data, headers=token_headers)
    item_id = response.json()["id"]
    
    # Update the item
    update_data = {
        "title": "Updated Item",
        "description": "This item has been updated",
    }
    response = client.put(f"/api/v1/items/{item_id}", json=update_data, headers=token_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]

def test_delete_item(client, token_headers):
    """Test deleting an item with authentication"""
    # First create an item
    item_data = {
        "title": "Item to Delete",
        "description": "This item will be deleted",
    }
    response = client.post("/api/v1/items/", json=item_data, headers=token_headers)
    item_id = response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/api/v1/items/{item_id}", headers=token_headers)
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/api/v1/items/{item_id}", headers=token_headers)
    assert response.status_code == 404

def test_unauthorized_access(client):
    """Test that unauthorized access is rejected"""
    response = client.get("/api/v1/items/")
    assert response.status_code == 401
{% else %}
def test_read_items(client):
    """Test reading items without authentication"""
    response = client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_item(client):
    """Test creating a new item without authentication"""
    item_data = {
        "title": "Test Item",
        "description": "This is a test item",
    }
    response = client.post("/api/v1/items/", json=item_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == item_data["title"]
    assert data["description"] == item_data["description"]
    assert "id" in data
    
    # Test reading the created item
    item_id = data["id"]
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_update_item(client):
    """Test updating an item without authentication"""
    # First create an item
    item_data = {
        "title": "Item to Update",
        "description": "This item will be updated",
    }
    response = client.post("/api/v1/items/", json=item_data)
    item_id = response.json()["id"]
    
    # Update the item
    update_data = {
        "title": "Updated Item",
        "description": "This item has been updated",
    }
    response = client.put(f"/api/v1/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]

def test_delete_item(client):
    """Test deleting an item without authentication"""
    # First create an item
    item_data = {
        "title": "Item to Delete",
        "description": "This item will be deleted",
    }
    response = client.post("/api/v1/items/", json=item_data)
    item_id = response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/api/v1/items/{item_id}")
    assert response.status_code == 204
    
    # Verify it's gone
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 404
{% endif %}
{% endif %}
