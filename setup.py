#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="FastAPI Template",
    version="0.1.0",
    author="Fiqih Fathor Rachim",
    author_email="fiqih.fathor.rachim@gmail.com",
    description="A FastAPI project template with best practices for building scalable APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fiqihfathor/fastapi_template",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "create-fastapi-project=create_fastapi_project:main",
        ],
    },
    include_package_data=True,
)
