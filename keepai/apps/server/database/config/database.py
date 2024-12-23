import os

from supabase import create_client


class Database:
    """Configuração do Supabase"""

    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = create_client(self.url, self.key)

    def get_client(self):
        """Retorna o cliente do Supabase"""
        return self.client


# Instância global do banco
db = Database()
