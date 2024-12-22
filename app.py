import flet as ft
from datetime import datetime, UTC
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from ui import NotasUI

# Carrega as variáveis de ambiente
load_dotenv()

# Configuração do Supabase
supabase: Client = create_client(
    os.getenv('SUPABASE_URL'),
    os.getenv('SUPABASE_KEY')
)

class DatabaseController:
    def __init__(self):
        self.supabase = supabase

    def get_all_notes(self):
        response = self.supabase.table('notas').select("*").order('data_criacao', desc=True).execute()
        return response.data

    def add_note(self, titulo, conteudo):
        data = {
            'titulo': titulo,
            'conteudo': conteudo,
            'data_criacao': datetime.now(UTC).isoformat()
        }
        self.supabase.table('notas').insert(data).execute()

    def delete_note(self, nota_id):
        try:
            self.supabase.table('notas').delete().eq('id', nota_id).execute()
            return True
        except Exception:
            return False

def init_db():
    # Não precisamos criar tabelas manualmente no Supabase
    pass

def main(page: ft.Page):
    db_controller = DatabaseController()
    NotasUI(page, db_controller)

if __name__ == '__main__':
    init_db()
    ft.app(target=main)
