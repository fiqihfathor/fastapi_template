#!/usr/bin/env python3
"""
Example script to create a sample FastAPI project with some basic endpoints.
This demonstrates how to use the FastAPI template to quickly create a new project.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Create an example FastAPI project.")
    parser.add_argument("--name", default="example_api", help="Name of the project")
    parser.add_argument("--path", default=".", help="Output path for the project")
    parser.add_argument("--use-uv", action="store_true", help="Use UV for package management")
    return parser.parse_args()


def run_command(cmd, cwd=None):
    """Run a command and return the output."""
    print(f"Running: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        print(f"Success: {result.stdout}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return False, e.stderr


def create_example_project():
    """Create an example FastAPI project."""
    args = parse_args()
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    
    # Create the project using create-fastapi-project
    create_cmd = [sys.executable, os.path.join(parent_dir, "create_fastapi_project.py"), 
                  args.name, "--path", args.path]
    
    if args.use_uv:
        create_cmd.append("--use-uv")
    
    success, _ = run_command(create_cmd)
    if not success:
        print("Failed to create the project")
        return False
    
    # Path to the new project
    project_path = os.path.join(args.path, args.name)
    
    # Create example endpoints
    create_example_endpoints(project_path)
    
    print(f"\nExample project created at {project_path}")
    print("\nTo run the project:")
    print(f"1. cd {project_path}")
    print("2. Copy .env.example to .env and update the values")
    print("3. Run the application: python run.py")
    print("4. Access the API documentation at http://localhost:8000/api/v1/docs")
    
    return True


def create_example_endpoints(project_path):
    """Create example endpoints in the project."""
    # Create endpoints directory if it doesn't exist
    endpoints_dir = os.path.join(project_path, "app", "api", "v1", "endpoints")
    os.makedirs(endpoints_dir, exist_ok=True)
    
    # Create example endpoints
    create_example_items_endpoint(endpoints_dir)
    create_example_users_endpoint(endpoints_dir)
    
    # Update router.py to include the endpoints
    update_router(os.path.join(project_path, "app", "api", "v1", "router.py"))
    
    # Create example schemas
    create_example_schemas(os.path.join(project_path, "app", "schemas"))


def create_example_items_endpoint(endpoints_dir):
    """Create an example items endpoint."""
    items_file = os.path.join(endpoints_dir, "items.py")
    with open(items_file, "w") as f:
        f.write("""from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate
from app.services.item_service import ItemService
from app.api.dependencies import get_item_service

router = APIRouter()

@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    item_service: ItemService = Depends(get_item_service)
):
    """Create a new item."""
    return await item_service.create_item(item)

@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: Optional[str] = None,
    item_service: ItemService = Depends(get_item_service)
):
    """Get all items with optional filtering."""
    return await item_service.get_items(skip=skip, limit=limit, name=name)

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    item_service: ItemService = Depends(get_item_service)
):
    """Get an item by ID."""
    item = await item_service.get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    item_service: ItemService = Depends(get_item_service)
):
    """Update an item."""
    updated_item = await item_service.update_item(item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item

@router.delete("/{item_id}", response_model=ItemResponse)
async def delete_item(
    item_id: int,
    item_service: ItemService = Depends(get_item_service)
):
    """Delete an item."""
    deleted_item = await item_service.delete_item(item_id)
    if not deleted_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_item
""")


def create_example_users_endpoint(endpoints_dir):
    """Create an example users endpoint."""
    users_file = os.path.join(endpoints_dir, "users.py")
    with open(users_file, "w") as f:
        f.write("""from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService
from app.api.dependencies import get_user_service

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    user: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user."""
    return await user_service.create_user(user)

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    email: Optional[str] = None,
    user_service: UserService = Depends(get_user_service)
):
    """Get all users with optional filtering."""
    return await user_service.get_users(skip=skip, limit=limit, email=email)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Get a user by ID."""
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    """Update a user."""
    updated_user = await user_service.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=UserResponse)
async def delete_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    """Delete a user."""
    deleted_user = await user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user
""")


def update_router(router_file):
    """Update the router.py file to include the example endpoints."""
    # Create the router.py file if it doesn't exist
    os.makedirs(os.path.dirname(router_file), exist_ok=True)
    
    with open(router_file, "w") as f:
        f.write("""from fastapi import APIRouter
from app.api.v1.endpoints import items, users

api_router = APIRouter()

api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
""")


def create_example_schemas(schemas_dir):
    """Create example schemas."""
    os.makedirs(schemas_dir, exist_ok=True)
    
    # Create item schema
    item_schema_file = os.path.join(schemas_dir, "item.py")
    with open(item_schema_file, "w") as f:
        f.write("""from pydantic import BaseModel
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(ItemBase):
    id: int
    
    class Config:
        orm_mode = True
""")
    
    # Create user schema
    user_schema_file = os.path.join(schemas_dir, "user.py")
    with open(user_schema_file, "w") as f:
        f.write("""from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    
    class Config:
        orm_mode = True
""")


if __name__ == "__main__":
    create_example_project()
