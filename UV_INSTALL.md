# Installing with UV

[UV](https://github.com/astral-sh/uv) is a fast Python package installer and resolver written in Rust. This guide explains how to use UV with this FastAPI template.

## Prerequisites

1. Install UV:

```bash
pip install uv
```

Or install it using pipx for isolated installation:

```bash
pipx install uv
```

## Installation Options

### Option 1: Create a new environment and install the project

```bash
# Create a new virtual environment and install the project
uv venv
uv pip install -e .
```

### Option 2: Install dependencies directly

```bash
# Install dependencies from requirements.txt
uv pip install -r requirements.txt
```

### Option 3: Install in development mode with all dependencies

```bash
# Install the project in development mode
uv pip install -e ".[dev]"
```

## Using UV with this template

UV is significantly faster than pip for installing packages and resolving dependencies. Here are some common commands:

```bash
# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On Unix/MacOS:
source .venv/bin/activate

# Install a new package
uv pip install package-name

# Update a package
uv pip install --upgrade package-name

# Generate a lockfile (requirements.lock)
uv pip freeze > requirements.lock

# Install from lockfile
uv pip install -r requirements.lock
```

## Benefits of UV

1. **Speed**: UV is significantly faster than pip for installing packages
2. **Reliability**: Better dependency resolution
3. **Reproducibility**: Consistent installations across environments
4. **Compatibility**: Works with existing Python projects

For more information, visit the [UV documentation](https://github.com/astral-sh/uv)

## Testing the Installation

This template includes a test script to verify that the installation works correctly. The script creates a temporary environment, installs the package, and tests creating a new project.

### Using the Test Script

```bash
# Test with standard pip installation
python test_install.py

# Test with UV installation
python test_install.py --use-uv

# Skip cleanup of temporary files (for debugging)
python test_install.py --skip-cleanup
```

### Automated Installation Scripts

For convenience, this template includes automated installation scripts:

- Windows: `install_with_uv.bat`
- Unix/Linux/Mac: `install_with_uv.sh`

These scripts will:
1. Check if UV is installed and install it if needed
2. Create a virtual environment using UV
3. Install the package in development mode
4. Provide instructions for next steps.
