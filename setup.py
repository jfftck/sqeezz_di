
#!/usr/bin/env python3
"""Setup script for sqeezz package."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sqeezz",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A lightweight dependency injection and service configuration library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/sqeezz",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.910",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/sqeezz/issues",
        "Source": "https://github.com/yourusername/sqeezz",
        "Documentation": "https://github.com/yourusername/sqeezz#readme",
    },
    keywords="dependency injection, service locator, configuration, async, testing",
)
