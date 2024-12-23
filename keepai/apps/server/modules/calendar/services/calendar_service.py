from datetime import datetime
from typing import Any, Dict, List

from database.repositories.event_repository import EventRepository


class CalendarService:
    def __init__(self):
        self.event_repository = EventRepository()

    def get_all_events(self) -> List[Dict[str, Any]]:
        """Retorna todos os eventos"""
        return self.event_repository.find_all()

    def get_event_by_id(self, event_id: int) -> Dict[str, Any]:
        """Retorna um evento pelo ID"""
        return self.event_repository.find_by_id(event_id)

    def create_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria um novo evento"""
        return self.event_repository.create(event_data)

    def update_event(self, event_id: int, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza um evento existente"""
        return self.event_repository.update(event_id, event_data)

    def delete_event(self, event_id: int) -> None:
        """Remove um evento"""
        self.event_repository.delete(event_id)

    def get_events_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Retorna eventos em um intervalo de datas"""
        return self.event_repository.find_by_date_range(start_date, end_date)
