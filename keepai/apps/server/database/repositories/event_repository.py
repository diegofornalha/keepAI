from datetime import datetime
from typing import Any, Dict, List

from ..config.supabase import get_supabase


class EventRepository:
    def __init__(self):
        self.supabase = get_supabase()
        self.table = "events"

    def find_all(self) -> List[Dict[str, Any]]:
        """Retorna todos os eventos"""
        response = self.supabase.table(self.table).select("*").execute()
        return response.data

    def find_by_id(self, event_id: int) -> Dict[str, Any]:
        """Retorna um evento pelo ID"""
        response = (
            self.supabase.table(self.table)
            .select("*")
            .eq("id", event_id)
            .single()
            .execute()
        )
        return response.data

    def find_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Retorna eventos em um intervalo de datas"""
        response = (
            self.supabase.table(self.table)
            .select("*")
            .gte("start", start_date.isoformat())
            .lte("start", end_date.isoformat())
            .execute()
        )
        return response.data

    def create(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo evento"""
        response = self.supabase.table(self.table).insert(event_data).execute()
        return response.data[0]

    def update(self, event_id: int, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um evento existente"""
        response = (
            self.supabase.table(self.table)
            .update(event_data)
            .eq("id", event_id)
            .execute()
        )
        return response.data[0] if response.data else None

    def delete(self, event_id: int) -> None:
        """Remove um evento"""
        self.supabase.table(self.table).delete().eq("id", event_id).execute()
