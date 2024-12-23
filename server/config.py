import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Clerk
    CLERK_API_KEY = os.getenv("CLERK_API_KEY")
    CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")
    CLERK_JWT_KEY = os.getenv("CLERK_JWT_KEY")

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Configurações de Sessão
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False  # A sessão expira quando o navegador é fechado
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos em segundos
