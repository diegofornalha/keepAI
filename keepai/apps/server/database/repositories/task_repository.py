from typing import Any, Dict, List

from ..config.database import db


class TaskRepository:
    """Repositório de tarefas usando Supabase"""

    def __init__(self):
        self.supabase = db.get_client()
        self.table = "tasks"

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova tarefa"""
        result = self.supabase.table(self.table).insert(data).execute()
        return result.data[0] if result.data else None

    def get_by_id(self, task_id: str) -> Dict[str, Any]:
        """Obtém uma tarefa pelo ID"""
        result = self.supabase.table(self.table).select("*").eq("id", task_id).execute()
        return result.data[0] if result.data else None

    def get_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Obtém tarefas por status"""
        result = (
            self.supabase.table(self.table).select("*").eq("status", status).execute()
        )
        return result.data if result.data else []
