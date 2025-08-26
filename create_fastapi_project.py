#!/usr/bin/env python3
"""
FastAPI Project Generator

This script generates a new FastAPI project with a standardized structure
based on best practices.

Usage:
    python create_fastapi_project.py <project_name> [--path <output_path>]
"""

import os
import sys
import shutil
import argparse
import re
import subprocess


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate a new FastAPI project with standardized structure.")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--path", default=".", help="Output path for the project (default: current directory)")
    parser.add_argument("--use-uv", action="store_true", help="Use UV for package management instead of pip")
    parser.add_argument("--no-venv", action="store_true", help="Skip virtual environment creation")
    parser.add_argument("--install-as-package", action="store_true", help="Install the project as a package in development mode")
    return parser.parse_args()


def validate_project_name(name):
    """Validate project name."""
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', name):
        print(f"Error: Project name '{name}' is invalid. It should start with a letter and contain only letters, numbers, underscores, or hyphens.")
        sys.exit(1)
    return name


def create_directory_structure(project_path):
    """Create the directory structure for the project."""
    directories = [
        "app",
        "app/api",
        "app/api/v1",
        "app/api/v1/endpoints",
        "app/core",
        "app/models",
        "app/schemas",
        "app/services",
        "app/repositories",
        "app/utils",
        "tests",
        "alembic",
        "alembic/versions",
    ]
    
    for directory in directories:
        os.makedirs(os.path.join(project_path, directory), exist_ok=True)
        # Create __init__.py files
        if directory.startswith("app"):
            with open(os.path.join(project_path, directory, "__init__.py"), "w") as f:
                f.write('"""' + directory.replace("/", ".") + ' module."""\n')


def copy_template_files(template_dir, project_path, project_name):
    """Copy template files to the project directory."""
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Walk through the template directory and copy files
    for root, dirs, files in os.walk(script_dir):
        # Skip the .git directory and the script itself
        if ".git" in root or "create_fastapi_project.py" in files:
            continue
            
        for file in files:
            # Skip the generator script and any compiled Python files
            if file == "create_fastapi_project.py" or file.endswith(".pyc"):
                continue
                
            # Get the relative path from the script directory
            rel_path = os.path.relpath(os.path.join(root, file), script_dir)
            
            # Create the destination directory if it doesn't exist
            dest_dir = os.path.dirname(os.path.join(project_path, rel_path))
            os.makedirs(dest_dir, exist_ok=True)
            
            # Copy the file
            shutil.copy2(os.path.join(root, file), os.path.join(project_path, rel_path))
            
            # Replace template name with project name in file content if needed
            if file.endswith((".py", ".md", ".ini", ".txt")):
                replace_template_name(os.path.join(project_path, rel_path), "fastapi_template_new", project_name)


def replace_template_name(file_path, template_name, project_name):
    """Replace template name with project name in file content."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Replace template name with project name
    content = content.replace(template_name, project_name)
    content = content.replace("FastAPI Template", project_name.replace("_", " ").replace("-", " ").title())
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def setup_virtual_environment(project_path, use_uv=False):
    """Set up a virtual environment for the project."""
    try:
        venv_dir = ".venv" if use_uv else "venv"
        venv_path = os.path.join(project_path, venv_dir)
        
        if use_uv:
            # Check if UV is installed
            try:
                subprocess.run(["uv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except (subprocess.CalledProcessError, FileNotFoundError):
                print("UV is not installed. Installing UV...")
                subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)
                
            # Create virtual environment using UV
            subprocess.run(["uv", "venv", venv_path], check=True)
            print(f"Virtual environment created at {venv_path} using UV")
            
            # Determine the pip and python commands based on the OS
            if os.name == "nt":  # Windows
                pip_cmd = "uv"
                pip_args = ["pip", "install"]
            else:  # Unix/Linux/Mac
                pip_cmd = "uv"
                pip_args = ["pip", "install"]
                
            # Install dependencies using UV
            subprocess.run([pip_cmd] + pip_args + ["-r", os.path.join(project_path, "requirements.txt")], check=True)
            print("Dependencies installed successfully using UV")
        else:
            # Create virtual environment using venv
            subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
            print(f"Virtual environment created at {venv_path}")
            
            # Determine the pip command based on the OS
            if os.name == "nt":  # Windows
                pip_cmd = os.path.join(venv_path, "Scripts", "pip")
            else:  # Unix/Linux/Mac
                pip_cmd = os.path.join(venv_path, "bin", "pip")
            
            # Install dependencies
            subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
            subprocess.run([pip_cmd, "install", "-r", os.path.join(project_path, "requirements.txt")], check=True)
            print("Dependencies installed successfully")
        
        return True, venv_dir
    except subprocess.CalledProcessError as e:
        print(f"Error setting up virtual environment: {e}")
        return False, venv_dir


def main():
    """Main function."""
    args = parse_arguments()
    project_name = validate_project_name(args.project_name)
    
    # Create project directory
    project_path = os.path.join(args.path, project_name)
    if os.path.exists(project_path):
        print(f"Error: Directory '{project_path}' already exists.")
        sys.exit(1)
    
    print(f"Creating FastAPI project '{project_name}' at '{project_path}'...")
    
    # Create directory structure
    create_directory_structure(project_path)
    
    # Copy template files
    copy_template_files(os.path.dirname(os.path.abspath(__file__)), project_path, project_name)
    
    # Create .env file from .env.example
    shutil.copy2(os.path.join(project_path, ".env.example"), os.path.join(project_path, ".env"))
    
    # Set up virtual environment if not skipped
    venv_success = False
    venv_dir = "venv"
    if not args.no_venv:
        venv_success, venv_dir = setup_virtual_environment(project_path, args.use_uv)
        
        # Install as package if requested
        if venv_success and args.install_as_package:
            try:
                if args.use_uv:
                    subprocess.run(["uv", "pip", "install", "-e", "."], 
                                  cwd=project_path, check=True)
                else:
                    pip_cmd = os.path.join(project_path, venv_dir, 
                                         "Scripts" if os.name == "nt" else "bin", "pip")
                    subprocess.run([pip_cmd, "install", "-e", "."], 
                                  cwd=project_path, check=True)
                print("Project installed as package in development mode")
            except subprocess.CalledProcessError as e:
                print(f"Error installing project as package: {e}")
    
    print("\n" + "=" * 80)
    print(f"FastAPI project '{project_name}' created successfully at '{project_path}'!")
    print("=" * 80)
    print("\nProject structure:")
    print(f"  {project_name}/")
    print("  ├── app/")
    print("  │   ├── api/")
    print("  │   ├── core/")
    print("  │   ├── models/")
    print("  │   ├── schemas/")
    print("  │   ├── services/")
    print("  │   ├── repositories/")
    print("  │   ├── utils/")
    print("  │   └── main.py")
    print("  ├── tests/")
    print("  ├── alembic/")
    print("  ├── .env")
    print("  ├── .env.example")
    print("  ├── requirements.txt")
    print("  ├── setup.py")
    print("  ├── pyproject.toml")
    print("  └── run.py")
    
    print("\nNext steps:")
    if venv_success:
        if os.name == "nt":  # Windows
            print("  1. Activate the virtual environment:")
            print(f"     > {project_path}\\{venv_dir}\\Scripts\\activate")
        else:  # Unix/Linux/Mac
            print("  1. Activate the virtual environment:")
            print(f"     $ source {project_path}/{venv_dir}/bin/activate")
    else:
        if args.use_uv:
            print("  1. Create and activate a virtual environment:")
            print(f"     $ uv venv {project_path}/.venv")
            if os.name == "nt":  # Windows
                print(f"     $ {project_path}\.venv\Scripts\activate")
            else:  # Unix/Linux/Mac
                print(f"     $ source {project_path}/.venv/bin/activate")
            print("  2. Install dependencies:")
            print(f"     $ uv pip install -r {project_path}/requirements.txt")
        else:
            print("  1. Create and activate a virtual environment:")
            print(f"     $ python -m venv {project_path}/venv")
            if os.name == "nt":  # Windows
                print(f"     $ {project_path}\\venv\\Scripts\\activate")
            else:  # Unix/Linux/Mac
                print(f"     $ source {project_path}/venv/bin/activate")
            print("  2. Install dependencies:")
            print(f"     $ pip install -r {project_path}/requirements.txt")
    
    print("  3. Update the .env file with your configuration")
    print("  4. Run the application:")
    print(f"     $ cd {project_path}")
    print("     $ python run.py")
    print("  5. Access the API documentation at http://localhost:8000/api/v1/docs")
    
    # Additional instructions for package installation
    print("\nAlternative installation methods:")
    print("  - Install as a package (development mode):")
    print("    $ pip install -e .")
    print("  - Install using UV:")
    print("    $ uv pip install -e .")
    print("\nThis will also make the 'create-fastapi-project' command available in your environment.")


if __name__ == "__main__":
    main()
