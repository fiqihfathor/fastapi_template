# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Features

- Modular project structure
- Standardized API responses
- Exception handling
- Pagination support
- Comprehensive documentation
{% if cookiecutter.use_sqlalchemy == "y" %}
- Database integration with SQLAlchemy ORM
{% endif %}
{% if cookiecutter.use_postgres == "y" %}
- PostgreSQL database support
{% endif %}
{% if cookiecutter.use_alembic == "y" %}
- Database migrations with Alembic
{% endif %}
{% if cookiecutter.use_pytest == "y" %}
- Testing with pytest
{% endif %}
{% if cookiecutter.use_auth == "y" %}
- JWT Authentication and user management
{% endif %}
{% if cookiecutter.use_docker == "y" %}
- Docker and Docker Compose support
{% endif %}
{% if cookiecutter.use_uv == "y" %}
- UV package manager support
{% endif %}

## Project Structure

```
{{ cookiecutter.project_slug }}/
├── app/                    # API endpoints
│   ├── api/                    # API endpoints
│   │   ├── v1/                 # API version 1
│   │   │   ├── endpoints/      # API endpoint modules
│   │   │   └── router.py       # API router
│   │   └── dependencies.py     # API dependencies
│   ├── core/                   # Core modules
│   │   ├── config.py           # Configuration settings
│   │   └── exceptions.py       # Custom exceptions
│   ├── models/                 # Database models
│   ├── repositories/           # Database repositories
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   ├── utils/                  # Utility functions
│   └── main.py                 # FastAPI application
├── .env.example                # Environment variables example
├── requirements.txt            # Project dependencies
{% if cookiecutter.use_docker == "y" %}
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker configuration
{% endif %}
{% if cookiecutter.use_uv == "y" %}
├── UV_INSTALL.md              # UV installation guide
{% endif %}
```

## Getting Started

{% if cookiecutter.use_docker == "y" %}
### Using Docker (Recommended)

1. Clone the repository
2. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```
3. The API will be available at http://localhost:8000
4. PgAdmin will be available at http://localhost:5050 (email: admin@admin.com, password: admin)
{% endif %}

### Standard Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and update the values
6. Run the application: `uvicorn app.main:app --reload`

{% if cookiecutter.use_uv == "y" %}
### Using UV

UV is a fast Python package installer and resolver written in Rust.

#### Option 1: Using the installation script

1. Clone the repository
2. Run the installation script:
   - Windows: `install_with_uv.bat`
   - Unix/MacOS: `bash install_with_uv.sh` (make it executable first with `chmod +x install_with_uv.sh`)
3. Copy `.env.example` to `.env` and update the values
4. Run the application: `uvicorn app.main:app --reload`

#### Option 2: Manual installation

1. Install UV: `pip install uv` or `pipx install uv`
2. Clone the repository
3. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   uv pip install -r requirements.txt
   ```
4. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Unix/MacOS: `source .venv/bin/activate`
5. Copy `.env.example` to `.env` and update the values
6. Run the application: `uvicorn app.main:app --reload`

See [UV_INSTALL.md](UV_INSTALL.md) for more detailed instructions on using UV.
{% endif %}

### Package Installation

You can also install this project as a package:

```bash
pip install -e .
```

This will also install the `create-fastapi-project` command-line tool.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## API Endpoints

### Items

- `GET /api/v1/items/` - List all items
- `POST /api/v1/items/` - Create a new item
- `GET /api/v1/items/{item_id}` - Get an item by ID
- `PUT /api/v1/items/{item_id}` - Update an item
- `DELETE /api/v1/items/{item_id}` - Delete an item

{% if cookiecutter.use_auth == "y" %}
### Authentication

- `POST /api/v1/auth/login` - Login and get access token

### Users

- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update current user info
- `PUT /api/v1/users/me/password` - Update current user password
{% endif %}

## Development

### Adding a New Endpoint

1. Create a new file in `app/api/v1/endpoints/`
2. Define your router and endpoints
3. Include your router in `app/api/v1/router.py`

### Adding a New Model

1. Create a new file in `app/models/`
2. Define your SQLAlchemy model
3. Create corresponding schemas in `app/schemas/`
4. Create a repository in `app/repositories/`
5. Create a service in `app/services/`

## Testing

Run tests with pytest:

```bash
pytest
```

## License

{{ cookiecutter.open_source_license }}
