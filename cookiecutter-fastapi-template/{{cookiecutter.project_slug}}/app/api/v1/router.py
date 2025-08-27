from fastapi import APIRouter

api_router = APIRouter()

# Import and include routers from endpoints
from app.api.v1.endpoints import items
api_router.include_router(items.router, prefix="/items", tags=["items"])

{% if cookiecutter.use_auth == "y" %}
from app.api.v1.endpoints import users, auth
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
{% endif %}
