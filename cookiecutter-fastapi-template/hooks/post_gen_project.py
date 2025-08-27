#!/usr/bin/env python
import os
import shutil
import subprocess
import sys

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)

def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))

def remove_dir(dirpath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, dirpath))

def execute_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        sys.exit(1)

if __name__ == '__main__':
    if '{{ cookiecutter.use_docker }}' == 'n':
        if os.path.exists('Dockerfile'):
            remove_file('Dockerfile')
        if os.path.exists('docker-compose.yml'):
            remove_file('docker-compose.yml')
        if os.path.exists('docker-compose-prod.yml'):
            remove_file('docker-compose-prod.yml')
        if os.path.exists('.dockerignore'):
            remove_file('.dockerignore')
        if os.path.exists('docker-build.bat'):
            remove_file('docker-build.bat')
        if os.path.exists('docker-build.sh'):
            remove_file('docker-build.sh')

    if '{{ cookiecutter.use_uv }}' == 'n':
        if os.path.exists('UV_INSTALL.md'):
            remove_file('UV_INSTALL.md')
        if os.path.exists('install_with_uv.bat'):
            remove_file('install_with_uv.bat')
        if os.path.exists('install_with_uv.sh'):
            remove_file('install_with_uv.sh')

    if '{{ cookiecutter.use_alembic }}' == 'n':
        if os.path.exists('alembic'):
            remove_dir('alembic')
        if os.path.exists('alembic.ini'):
            remove_file('alembic.ini')

    if '{{ cookiecutter.use_pytest }}' == 'n':
        if os.path.exists('tests'):
            remove_dir('tests')
        if os.path.exists('pytest.ini'):
            remove_file('pytest.ini')

    # Create .env file from .env.example
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("Created .env file from .env.example")

    print("Project setup complete!")
    print(f"Your FastAPI project '{PROJECT_DIRECTORY}' has been created successfully!")
    print("\nNext steps:")
    print("1. Review the README.md file for usage instructions")
    print("2. Update the .env file with your configuration")
    print("3. Run the application with 'uvicorn app.main:app --reload'")
    
    if '{{ cookiecutter.use_docker }}' == 'y':
        print("   Or with Docker: 'docker-compose up -d'")
