import pytest
from fastapi.testclient import TestClient
from app.main import app


def test_root_endpoint(client):
    """Test the root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == "200"
    assert data["responseStatus"] == "SUCCESS"
    assert "message" in data["data"]
    assert "version" in data["data"]
    assert "docs" in data["data"]


def test_docs_endpoint(client):
    """Test that the docs endpoint is accessible."""
    response = client.get("/api/v1/docs")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Swagger UI" in response.text


def test_redoc_endpoint(client):
    """Test that the redoc endpoint is accessible."""
    response = client.get("/api/v1/redoc")
    
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "ReDoc" in response.text


def test_openapi_json(client):
    """Test that the OpenAPI JSON is accessible."""
    response = client.get("/api/v1/openapi.json")
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
    assert "components" in data
