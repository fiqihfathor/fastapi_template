#!/usr/bin/env python3
"""
Test script to verify the installation of the FastAPI template package.
This script checks if the package can be installed and the CLI tool works.
"""

import os
import sys
import subprocess
import tempfile
import shutil
import argparse


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Test the installation of the FastAPI template package.")
    parser.add_argument("--use-uv", action="store_true", help="Use UV for package installation")
    parser.add_argument("--skip-cleanup", action="store_true", help="Skip cleanup of temporary files")
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


def test_installation(use_uv=False):
    """Test the installation of the package."""
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    print(f"Created temporary directory: {temp_dir}")
    
    try:
        # Create a virtual environment
        if use_uv:
            success, _ = run_command(["uv", "venv", os.path.join(temp_dir, ".venv")])
            if not success:
                print("Failed to create virtual environment with UV")
                return False
            
            # Install the package
            success, _ = run_command(
                ["uv", "pip", "install", "-e", os.path.abspath(".")], 
                cwd=temp_dir
            )
        else:
            success, _ = run_command([sys.executable, "-m", "venv", os.path.join(temp_dir, "venv")])
            if not success:
                print("Failed to create virtual environment")
                return False
            
            # Determine pip path
            if os.name == "nt":  # Windows
                pip_path = os.path.join(temp_dir, "venv", "Scripts", "pip")
            else:  # Unix/Linux/Mac
                pip_path = os.path.join(temp_dir, "venv", "bin", "pip")
            
            # Install the package
            success, _ = run_command([pip_path, "install", "-e", os.path.abspath(".")], cwd=temp_dir)
        
        if not success:
            print("Failed to install the package")
            return False
        
        # Test creating a new project
        project_name = "test_project"
        project_path = os.path.join(temp_dir, project_name)
        
        # Determine the create-fastapi-project command path
        if use_uv:
            if os.name == "nt":  # Windows
                cmd_path = os.path.join(temp_dir, ".venv", "Scripts", "create-fastapi-project")
            else:  # Unix/Linux/Mac
                cmd_path = os.path.join(temp_dir, ".venv", "bin", "create-fastapi-project")
        else:
            if os.name == "nt":  # Windows
                cmd_path = os.path.join(temp_dir, "venv", "Scripts", "create-fastapi-project")
            else:  # Unix/Linux/Mac
                cmd_path = os.path.join(temp_dir, "venv", "bin", "create-fastapi-project")
        
        # Run the command
        success, _ = run_command([cmd_path, project_name, "--no-venv"], cwd=temp_dir)
        if not success:
            print("Failed to create a new project")
            return False
        
        # Check if the project was created
        if not os.path.exists(project_path):
            print(f"Project directory {project_path} was not created")
            return False
        
        print("Installation test completed successfully!")
        return True
    
    finally:
        # Clean up
        if not args.skip_cleanup:
            print(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    args = parse_args()
    success = test_installation(args.use_uv)
    sys.exit(0 if success else 1)
