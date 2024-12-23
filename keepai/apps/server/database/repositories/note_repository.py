from typing import Any, Dict, List, Optional

from ..config.database import db


class NoteRepository:
    """Repositório de notas usando Supabase"""

    def __init__(self):
        self.supabase = db.get_client()
        self.table = "notes"

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova nota"""
        result = self.supabase.table(self.table).insert(data).execute()
        return result.data[0] if result.data else None

    def get_by_id(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Obtém uma nota pelo ID"""
        result = self.supabase.table(self.table).select("*").eq("id", note_id).execute()
        return result.data[0] if result.data else None

    def get_all_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Obtém todas as notas de um usuário"""
        result = (
            self.supabase.table(self.table).select("*").eq("user_id", user_id).execute()
        )
        return result.data if result.data else []

    def update(self, note_id: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Atualiza uma nota"""
        result = (
            self.supabase.table(self.table).update(data).eq("id", note_id).execute()
        )
        return result.data[0] if result.data else None

    def delete(self, note_id: str) -> bool:
        """Remove uma nota"""
        result = self.supabase.table(self.table).delete().eq("id", note_id).execute()
        return bool(result.data)

    def search(self, user_id: str, query: str) -> List[Dict[str, Any]]:
        """Pesquisa notas por texto"""
        result = (
            self.supabase.table(self.table)
            .select("*")
            .eq("user_id", user_id)
            .ilike("content", f"%{query}%")
            .execute()
        )
        return result.data if result.data else []
