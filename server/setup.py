from setuptools import setup, find_packages

setup(
    name="server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "supabase",
        "pydantic",
        "pydantic-settings",
    ],
)
