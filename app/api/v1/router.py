from fastapi import APIRouter
from app.api.v1.endpoints import items, users

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
