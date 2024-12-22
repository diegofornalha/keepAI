from dotenv import load_dotenv
import os
from supabase import create_client

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do projeto
PROJECT_NAME = "KeepAI"
DEBUG = True

# Configurações do Supabase
def get_supabase_client():
    return create_client(
        os.getenv('SUPABASE_URL'),
        os.getenv('SUPABASE_KEY')
    )

# Configurações do modelo
MODEL_CONFIG = {
    "model": "gemini-pro",
    "temperature": 0.7,
    "convert_system_message_to_human": True
} 