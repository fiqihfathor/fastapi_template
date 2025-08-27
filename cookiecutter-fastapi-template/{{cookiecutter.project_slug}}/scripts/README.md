# Scripts Directory

This directory contains utility scripts for managing and running the application.

## Available Scripts

### `run_app.py`

Runs the FastAPI application using Uvicorn.

```bash
python scripts/run_app.py
```

{% if cookiecutter.use_pytest == "y" %}
### `run_tests.py`

Runs the test suite with pytest and generates coverage report.

```bash
python scripts/run_tests.py
```
{% endif %}

{% if cookiecutter.use_sqlalchemy == "y" %}
### `init_db.py`

Initializes the database with initial data.

```bash
python scripts/init_db.py
```
{% endif %}

## Adding New Scripts

When adding new scripts to this directory, please follow these guidelines:

1. Use descriptive names for your scripts
2. Include proper documentation within the script
3. Add the script to this README.md file with usage instructions
4. Make sure the script can be run from the project root directory
