from setuptools import setup, find_packages

setup(
    name="server",
    version="0.1",
    packages=find_packages(),
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
        # Adicione outras dependências aqui
    ],
)
