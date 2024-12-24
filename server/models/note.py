from typing import Dict, Any


class Note:
    def __init__(self, data: Dict[str, Any]) -> None:
        self.id = data.get("id")
        self.title = data.get("title")
        self.content = data.get("content")
        self.user_id = data.get("user_id")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self) -> str:
        return f"<Note {self.title}>"
