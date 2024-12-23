from setuptools import setup, find_packages

setup(
    name="server",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "flask",
        "flask-cors",
        "flask-sqlalchemy",
        "python-dotenv",
        # Adicione outras dependências aqui
    ],
)
