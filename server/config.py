import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-key-12345")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configurações do Clerk
    CLERK_API_KEY = os.getenv("CLERK_API_KEY")
    CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")

    # Configurações do OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
