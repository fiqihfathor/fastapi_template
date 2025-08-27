# Cookiecutter FastAPI Template

A Cookiecutter template for creating FastAPI projects with best practices.

## Features

- **Modular Structure**: Well-organized project structure for scalability
- **FastAPI Best Practices**: Follows FastAPI recommended patterns
- **Database Integration**: SQLAlchemy ORM with migrations using Alembic
- **Docker Support**: Ready-to-use Docker and docker-compose configuration
- **UV Support**: Fast Python package installer and environment manager
- **Authentication**: JWT authentication ready to use
- **Testing**: Pytest configuration with fixtures
- **Documentation**: Auto-generated API documentation

## Requirements

- Python 3.8+
- Cookiecutter 2.1.1 or higher: `pip install cookiecutter`

## Usage

### Create a new project

```bash
cookiecutter https://github.com/yourusername/cookiecutter-fastapi-template
```

You'll be prompted to enter values for your project:

- `project_name`: Name of your project
- `project_slug`: Python package name (derived from project_name by default)
- `project_description`: Short description of your project
- `author_name`: Your name
- `author_email`: Your email
- `use_docker`: Include Docker configuration (y/n)
- `use_uv`: Include UV package manager support (y/n)
- `use_postgres`: Include PostgreSQL configuration (y/n)
- `use_sqlalchemy`: Include SQLAlchemy ORM (y/n)
- `use_alembic`: Include Alembic migrations (y/n)
- `use_pytest`: Include pytest configuration (y/n)
- `use_auth`: Include authentication (y/n)
- `python_version`: Python version to use
- `open_source_license`: License to use

### After generation

1. Navigate to your project directory:
   ```bash
   cd your-project-name
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```
your-project-name/
├── app/                    # FastAPI application
│   ├── api/                # API endpoints
│   │   ├── v1/             # API version 1
│   │   │   ├── endpoints/  # API endpoint modules
│   │   │   └── router.py   # API router
│   │   └── dependencies.py # API dependencies
│   ├── core/               # Core modules
│   │   ├── config.py       # Configuration settings
│   │   └── exceptions.py   # Custom exceptions
│   ├── models/             # Database models
│   ├── repositories/       # Database repositories
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   └── main.py             # FastAPI application
├── tests/                  # Tests
├── alembic/                # Database migrations
├── .env.example            # Environment variables example
├── requirements.txt        # Project dependencies
└── docker-compose.yml      # Docker Compose configuration
```

## License

MIT
