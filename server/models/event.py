from typing import Dict, Any


class Event:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.id = data.get("id")
        self.title = data.get("title")
        self.description = data.get("description")
        self.start_time = data.get("start_time")
        self.end_time = data.get("end_time")
        self.color = data.get("color", "#2563eb")  # Formato hex: #RRGGBB
        self.user_id = data.get("user_id")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "start": self.start_time,
            "end": self.end_time,
            "color": self.color,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self) -> str:
        return f"<Event {self.title}>"
