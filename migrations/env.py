from logging.config import fileConfig
import os
import sys
from dotenv import load_dotenv
from typing import Optional, Any, Dict
from supabase import create_client, Client

# Adicionar o diretório raiz ao PATH para importar os modelos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase_client() -> Client:
    """Retorna um cliente Supabase configurado"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def run_migrations() -> None:
    """Executa as migrações no Supabase

    Como o Supabase gerencia as migrações através do dashboard ou CLI,
    este arquivo serve apenas como referência para a configuração.
    Para executar migrações, use:
    1. Dashboard do Supabase
    2. Supabase CLI
    3. Migrations SQL direto no editor SQL
    """
    print(
        """
    O Supabase não usa o Alembic para migrações.
    Por favor, use uma das seguintes opções:
    1. Dashboard do Supabase
    2. Supabase CLI
    3. Migrations SQL direto no editor SQL
    """
    )


if __name__ == "__main__":
    run_migrations()
