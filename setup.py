"""
MongoDB Atlas MCP Server Setup

用于安装和分发MongoDB Atlas MCP服务器包
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mongo-atlas-mcp",
    version="1.0.0",
    author="MCP Developer",
    author_email="developer@example.com",
    description="MongoDB Atlas MCP服务器 - 基于FastMCP的MongoDB Atlas连接和操作服务器",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/mongo-atlas-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Database",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mongo-atlas-mcp=mongo_atlas_mcp.server:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="mcp mongodb atlas fastmcp database",
    project_urls={
        "Bug Reports": "https://github.com/your-username/mongo-atlas-mcp/issues",
        "Source": "https://github.com/your-username/mongo-atlas-mcp",
        "Documentation": "https://github.com/your-username/mongo-atlas-mcp/blob/main/README.md",
    },
) 