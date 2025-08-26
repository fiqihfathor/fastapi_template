@echo off
echo Installing FastAPI Template with UV...

REM Check if UV is installed
where uv >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo UV is not installed. Installing UV...
    pip install uv
)

REM Create a virtual environment with UV
echo Creating virtual environment with UV...
uv venv .venv

REM Activate the virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Install the package in development mode
echo Installing FastAPI Template in development mode...
uv pip install -e .

echo.
echo Installation completed successfully!
echo.
echo To create a new FastAPI project, run:
echo create-fastapi-project your_project_name [--use-uv]
echo.
echo To deactivate the virtual environment, run:
echo deactivate
