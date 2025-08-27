{% if cookiecutter.use_pytest == "y" %}
# Tests Directory

This directory contains test files for the application.

## Structure

- `conftest.py`: Contains pytest fixtures and configuration
- `test_api_items.py`: Tests for the items API endpoints
{% if cookiecutter.use_auth == "y" %}
- `test_api_users.py`: Tests for the users API endpoints and authentication
{% endif %}

## Running Tests

You can run the tests using pytest directly:

```bash
pytest
```

Or using the provided script:

```bash
python scripts/run_tests.py
```

## Adding New Tests

When adding new tests, please follow these guidelines:

1. Name test files with the prefix `test_`
2. Group tests by functionality
3. Use descriptive test function names with the prefix `test_`
4. Use fixtures from `conftest.py` when possible
5. Add proper docstrings to test functions

## Test Coverage

To generate a test coverage report:

```bash
pytest --cov=app --cov-report=html
```

This will create an HTML report in the `htmlcov` directory.
{% endif %}
