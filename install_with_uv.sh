#!/bin/bash
echo "Installing FastAPI Template with UV..."

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo "UV is not installed. Installing UV..."
    pip install uv
fi

# Create a virtual environment with UV
echo "Creating virtual environment with UV..."
uv venv .venv

# Activate the virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install the package in development mode
echo "Installing FastAPI Template in development mode..."
uv pip install -e .

echo ""
echo "Installation completed successfully!"
echo ""
echo "To create a new FastAPI project, run:"
echo "create-fastapi-project your_project_name [--use-uv]"
echo ""
echo "To deactivate the virtual environment, run:"
echo "deactivate"
