from setuptools import setup, find_packages

setup(
    name="{{ cookiecutter.project_slug }}",
    version="{{ cookiecutter.version }}",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "pydantic>=2.0.0",
        "pydantic-settings>=2.0.0",
        {% if cookiecutter.use_sqlalchemy == "y" %}"sqlalchemy>=2.0.0",{% endif %}
        {% if cookiecutter.use_postgres == "y" %}"psycopg2-binary>=2.9.6",{% endif %}
        {% if cookiecutter.use_alembic == "y" %}"alembic>=1.11.1",{% endif %}
        {% if cookiecutter.use_auth == "y" %}"python-jose>=3.3.0",
        "passlib>=1.7.4",
        "python-multipart>=0.0.6",
        "bcrypt>=4.0.1",{% endif %}
        {% if cookiecutter.use_pytest == "y" %}"pytest>=7.3.1",
        "pytest-cov>=4.1.0",
        "httpx>=0.24.1",{% endif %}
    ],
    python_requires=">={{ cookiecutter.python_version }}",
    author="{{ cookiecutter.author_name }}",
    author_email="{{ cookiecutter.author_email }}",
    description="{{ cookiecutter.project_description }}",
    keywords="fastapi, api, rest, {{ cookiecutter.project_slug }}",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: {{ cookiecutter.python_version }}",
        "License :: OSI Approved :: {{ cookiecutter.open_source_license }}",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
    ],
)
