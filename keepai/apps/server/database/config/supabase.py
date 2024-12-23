import os
import sys

# Adicionar o diretório raiz ao PYTHONPATH
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

from supabase import Client, create_client

from config.settings import Settings

settings = Settings()


def get_supabase() -> Client:
    """Retorna uma instância do cliente Supabase"""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY são obrigatórios")

    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
