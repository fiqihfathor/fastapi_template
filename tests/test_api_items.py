import pytest
from fastapi.testclient import TestClient
from app.models.item import Item


def test_create_item(client, db_session):
    """Test creating a new item."""
    # Test data
    item_data = {
        "name": "Test Item",
        "description": "This is a test item",
        "price": 1000,
        "is_active": True
    }
    
    # Make request
    response = client.post("/api/v1/items/", json=item_data)
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert data["data"]["name"] == item_data["name"]
    assert data["data"]["description"] == item_data["description"]
    assert data["data"]["price"] == item_data["price"]
    assert data["data"]["is_active"] == item_data["is_active"]
    assert "id" in data["data"]
    
    # Check database
    db_item = db_session.query(Item).filter(Item.id == data["data"]["id"]).first()
    assert db_item is not None
    assert db_item.name == item_data["name"]


def test_get_items(client, db_session):
    """Test getting a list of items."""
    # Create test items
    items = [
        Item(name="Item 1", description="Description 1", price=1000),
        Item(name="Item 2", description="Description 2", price=2000),
        Item(name="Item 3", description="Description 3", price=3000),
    ]
    db_session.add_all(items)
    db_session.commit()
    
    # Make request
    response = client.get("/api/v1/items/")
    
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


def test_get_item(client, db_session):
    """Test getting a specific item."""
    # Create test item
    item = Item(name="Test Item", description="Test Description", price=1000)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    # Make request
    response = client.get(f"/api/v1/items/{item.id}")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert data["data"]["id"] == item.id
    assert data["data"]["name"] == item.name
    assert data["data"]["description"] == item.description
    assert data["data"]["price"] == item.price


def test_update_item(client, db_session):
    """Test updating an item."""
    # Create test item
    item = Item(name="Original Name", description="Original Description", price=1000)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    # Update data
    update_data = {
        "name": "Updated Name",
        "price": 1500
    }
    
    # Make request
    response = client.put(f"/api/v1/items/{item.id}", json=update_data)
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert data["data"]["id"] == item.id
    assert data["data"]["name"] == update_data["name"]
    assert data["data"]["description"] == item.description  # Unchanged
    assert data["data"]["price"] == update_data["price"]
    
    # Check database
    db_item = db_session.query(Item).filter(Item.id == item.id).first()
    assert db_item.name == update_data["name"]
    assert db_item.price == update_data["price"]


def test_delete_item(client, db_session):
    """Test deleting an item."""
    # Create test item
    item = Item(name="Test Item", description="Test Description", price=1000)
    db_session.add(item)
    db_session.commit()
    db_session.refresh(item)
    
    # Make request
    response = client.delete(f"/api/v1/items/{item.id}")
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert "message" in data["data"]
    
    # Check database
    db_item = db_session.query(Item).filter(Item.id == item.id).first()
    assert db_item is None


def test_get_nonexistent_item(client):
    """Test getting an item that doesn't exist."""
    # Make request with non-existent ID
    response = client.get("/api/v1/items/999")
    
    # Check response
    assert response.status_code == 404
    data = response.json()
    assert data["responseCode"] == "404"
    assert data["responseStatus"] == "NOT_FOUND"
    assert "message" in data["data"]
