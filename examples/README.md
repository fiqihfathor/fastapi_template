# FastAPI Template Examples

This directory contains example scripts to help you get started with the FastAPI template.

## Create Example Project

The `create_example_project.py` script demonstrates how to create a sample FastAPI project with pre-configured endpoints for items and users.

### Usage

```bash
# Create an example project with default settings
python create_example_project.py

# Create a project with a custom name
python create_example_project.py --name my_api

# Create a project in a specific directory
python create_example_project.py --path /path/to/directory

# Create a project using UV for package management
python create_example_project.py --use-uv
```

### What the Example Project Includes

The example project includes:

1. **Items API**: CRUD operations for managing items
   - Create, read, update, delete endpoints
   - Filtering and pagination

2. **Users API**: CRUD operations for managing users
   - Create, read, update, delete endpoints
   - Filtering and pagination

3. **Schemas**:
   - Item schemas (create, update, response)
   - User schemas (create, update, response)

### Next Steps After Creating the Example Project

1. Navigate to the project directory: `cd example_api` (or your custom name)
2. Copy `.env.example` to `.env` and update the values
3. Run the application: `python run.py`
4. Access the API documentation at http://localhost:8000/api/v1/docs
5. Explore and modify the code to fit your needs
