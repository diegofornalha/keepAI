import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Configurações da aplicação
APP_NAME = "KeepAI"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("A variável de ambiente SECRET_KEY deve estar definida")

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configurações do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Configurações CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
CORS_METHODS = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_HEADERS = ["*"]

# Configurações de cache
CACHE_TYPE = os.getenv("CACHE_TYPE", "simple")
CACHE_REDIS_URL = os.getenv("REDIS_URL")

# Configurações de rate limit
RATELIMIT_DEFAULT = "100/hour"
RATELIMIT_STORAGE_URL = CACHE_REDIS_URL

# Exporta todas as configurações
__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "DEBUG",
    "SECRET_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "GEMINI_API_KEY",
    "LOG_LEVEL",
    "LOG_FORMAT",
    "LOG_DIR",
    "CORS_ORIGINS",
    "CORS_METHODS",
    "CORS_HEADERS",
    "CACHE_TYPE",
    "CACHE_REDIS_URL",
    "RATELIMIT_DEFAULT",
    "RATELIMIT_STORAGE_URL",
]
