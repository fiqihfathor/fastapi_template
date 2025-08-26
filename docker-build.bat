@echo off
echo Building Docker image for FastAPI application...
docker build -t fastapi-template .
echo Done! Image built successfully.
echo.
echo To run the application:
echo docker run -p 8000:8000 fastapi-template
