from typing import Dict, Any, Optional
from datetime import datetime
from server.config.settings import settings


class NotesManager:
    def __init__(self) -> None:
        self.supabase = settings.get_supabase_client()

    def create_note(self, user_id: str, content: str) -> Dict[str, Any]:
        """Cria uma nova nota"""
        try:
            data = {
                "user_id": user_id,
                "content": content,
                "created_at": datetime.now().isoformat(),
            }
            result = self.supabase.table("notes").insert(data).execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_note(self, note_id: str) -> Optional[Dict[str, Any]]:
        """Retorna uma nota específica"""
        try:
            result = (
                self.supabase.table("notes").select("*").eq("id", note_id).execute()
            )
            return result.data[0] if result.data else None
        except Exception:
            return None

    def update_note(self, note_id: str, content: str) -> Dict[str, Any]:
        """Atualiza uma nota existente"""
        try:
            data = {"content": content, "updated_at": datetime.now().isoformat()}
            result = (
                self.supabase.table("notes").update(data).eq("id", note_id).execute()
            )
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def delete_note(self, note_id: str) -> Dict[str, Any]:
        """Deleta uma nota"""
        try:
            result = self.supabase.table("notes").delete().eq("id", note_id).execute()
            return {"success": True, "data": result.data}
        except Exception as e:
            return {"success": False, "error": str(e)}
