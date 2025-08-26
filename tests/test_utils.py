import pytest
from app.utils.response import success_response, error_response, validation_error_response, pagination_response


def test_success_response():
    """Test the success_response utility function."""
    # Test with simple data
    data = {"message": "Success"}
    response = success_response(data)
    
    assert response["responseCode"] == "200"
    assert response["responseStatus"] == "SUCCESS"
    assert response["data"] == data
    
    # Test with complex data
    data = {
        "id": 1,
        "name": "Test",
        "details": {
            "description": "Test description",
            "active": True
        }
    }
    response = success_response(data)
    
    assert response["responseCode"] == "200"
    assert response["responseStatus"] == "SUCCESS"
    assert response["data"] == data


def test_error_response():
    """Test the error_response utility function."""
    response = error_response("404", "NOT_FOUND", "Resource not found")
    
    assert response["responseCode"] == "404"
    assert response["responseStatus"] == "NOT_FOUND"
    assert response["data"]["message"] == "Resource not found"


def test_validation_error_response():
    """Test the validation_error_response utility function."""
    errors = [
        {"loc": ["body", "name"], "msg": "field required", "type": "value_error.missing"},
        {"loc": ["body", "price"], "msg": "must be greater than 0", "type": "value_error.number.not_gt"}
    ]
    
    response = validation_error_response(errors)
    
    assert response["responseCode"] == "422"
    assert response["responseStatus"] == "VALIDATION_ERROR"
    assert response["data"]["errors"] == errors


def test_pagination_response():
    """Test the pagination_response utility function."""
    # Test with has_more = False
    items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
    total = 2
    limit = 10
    offset = 0
    
    response = pagination_response(items, total, limit, offset)
    
    assert response["responseCode"] == "200"
    assert response["responseStatus"] == "SUCCESS"
    assert response["data"]["items"] == items
    assert response["data"]["pagination"]["total"] == total
    assert response["data"]["pagination"]["limit"] == limit
    assert response["data"]["pagination"]["offset"] == offset
    assert response["data"]["pagination"]["has_more"] is False
    
    # Test with has_more = True
    items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]
    total = 12
    limit = 2
    offset = 0
    
    response = pagination_response(items, total, limit, offset)
    
    assert response["responseCode"] == "200"
    assert response["responseStatus"] == "SUCCESS"
    assert response["data"]["items"] == items
    assert response["data"]["pagination"]["total"] == total
    assert response["data"]["pagination"]["limit"] == limit
    assert response["data"]["pagination"]["offset"] == offset
    assert response["data"]["pagination"]["has_more"] is True
