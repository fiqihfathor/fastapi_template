# FastAPI Template

A FastAPI project template with best practices for building scalable APIs.

## Features

- Modular project structure
- Standardized API responses
- Exception handling
- Database integration with SQLAlchemy
- Authentication ready
- Pagination support
- Comprehensive documentation

## Project Structure

```
fastapi_template_new/
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
├── setup.py                    # Package installation setup
├── pyproject.toml              # Modern Python packaging
├── docker-compose.yml          # Docker Compose configuration
└── UV_INSTALL.md              # UV installation guide
```

## Getting Started

### Using Docker (Recommended)

1. Clone the repository
2. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```
3. The API will be available at http://localhost:8000
4. PgAdmin will be available at http://localhost:5050 (email: admin@admin.com, password: admin)

### Standard Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and update the values
6. Run the application: `uvicorn app.main:app --reload`

### Using UV (Recommended)

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

### Package Installation

You can also install this template as a package:

```bash
# Using pip
pip install -e .

# Using UV
uv pip install -e .
```

This will also install the `create-fastapi-project` command-line tool.

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## Examples

The `examples` directory contains sample scripts to help you get started with the FastAPI template:

- `create_example_project.py`: Creates a sample FastAPI project with pre-configured endpoints for items and users

To create an example project:

```bash
python examples/create_example_project.py --name my_api [--use-uv]
```

See the [examples README](examples/README.md) for more details.

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

## Best Practices

- Keep routes thin, move business logic to services
- Use repositories for database operations
- Use standardized responses
- Handle exceptions properly
- Document your API endpoints
