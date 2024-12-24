from setuptools import setup, find_packages

setup(
    name="keepai",
    version="0.1",
    package_dir={"": "03_server"},
    packages=find_packages(where="03_server"),
    install_requires=[
        "flask",
        "flask-cors",
        "python-dotenv",
        "supabase",
        "python-jose[cryptography]",  # Para JWT
        "requests",  # Para chamadas HTTP
        "langchain",  # Para funcionalidades de IA
        "google-generativeai",  # Para integração com Gemini
        "pyjwt",  # Para validação de tokens JWT do Clerk
        "jupyter",  # Para notebooks
        "pandas",  # Para análise de dados
        "notebook",  # Para Jupyter Notebook
        "jupyterlab",  # Para ambiente JupyterLab
    ],
)
