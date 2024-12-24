import os
import sys
from typing import List
from dotenv import load_dotenv
from supabase import create_client, Client

# Adicionar diretório raiz ao PATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Lista de arquivos de migração em ordem
MIGRATION_FILES: List[str] = [
    "00_create_schemas.sql",
    "01_create_notes_table.sql",
    "02_create_profiles_table.sql",
    "03_create_ai_tables.sql",
    "04_create_tasks_tables.sql",
]


def get_supabase_client() -> Client:
    """Retorna um cliente Supabase configurado"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def run_migrations() -> None:
    """Executa as migrações no Supabase"""
    print("Para executar as migrações, use uma das opções:")
    print("1. Dashboard do Supabase")
    print("2. Supabase CLI")
    print("3. Editor SQL do Supabase")
    print("\nArquivos de migração em ordem:")
    for file in MIGRATION_FILES:
        print(f"- {file}")


if __name__ == "__main__":
    run_migrations()
