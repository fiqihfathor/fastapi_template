from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.exceptions import CustomException

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Exception handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "responseCode": str(exc.status_code),
            "responseStatus": exc.error_type,
            "data": {"message": exc.detail}
        }
    )

@app.get("/")
async def root():
    return {
        "responseCode": "200",
        "responseStatus": "SUCCESS",
        "data": {
            "message": f"Welcome to {settings.PROJECT_NAME} API",
            "version": settings.PROJECT_VERSION,
            "docs": f"{settings.API_V1_STR}/docs"
        }
    }
