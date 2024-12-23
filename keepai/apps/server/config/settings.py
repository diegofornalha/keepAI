import os

from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Flask
SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-key")
DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Clerk
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_PUBLISHABLE_KEY = os.getenv("CLERK_PUBLISHABLE_KEY")

# Google AI
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configurações de cache
CACHE_TYPE = "simple"
CACHE_DEFAULT_TIMEOUT = 300


class Settings:
    """Configurações da aplicação"""

    def __init__(self):
        self.SECRET_KEY = SECRET_KEY
        self.DEBUG = DEBUG
        self.SUPABASE_URL = SUPABASE_URL
        self.SUPABASE_KEY = SUPABASE_KEY
        self.CLERK_SECRET_KEY = CLERK_SECRET_KEY
        self.CLERK_PUBLISHABLE_KEY = CLERK_PUBLISHABLE_KEY
        self.GOOGLE_API_KEY = GOOGLE_API_KEY
        self.CACHE_TYPE = CACHE_TYPE
        self.CACHE_DEFAULT_TIMEOUT = CACHE_DEFAULT_TIMEOUT
