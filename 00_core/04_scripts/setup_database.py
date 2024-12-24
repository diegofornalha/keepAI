"""Script para configurar o banco de dados Supabase."""

import os
from supabase import create_client, Client


def setup_database() -> None:
    """Configura o banco de dados Supabase"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")

    client = create_client(supabase_url, supabase_key)

    # Criar tabelas
    create_tables(client)


def create_tables(client: Client) -> None:
    """Cria as tabelas necessárias"""
    try:
        # Criar tabela de notas
        client.table("notes").select("*").limit(1).execute()
        print("Tabela 'notes' já existe")
    except Exception:
        print("Criando tabela 'notes'...")
        client.rpc(
            "create_notes_table",
            {
                "table_name": "notes",
                "columns": {
                    "id": "uuid DEFAULT uuid_generate_v4() PRIMARY KEY",
                    "user_id": "text NOT NULL",
                    "title": "text",
                    "content": "text",
                    "created_at": "timestamp with time zone DEFAULT NOW()",
                    "updated_at": "timestamp with time zone DEFAULT NOW()",
                },
            },
        ).execute()
        print("Tabela 'notes' criada com sucesso")


if __name__ == "__main__":
    setup_database()
