from typing import Dict, Any, Optional
from datetime import datetime


class Task:
    def __init__(
        self,
        title: str,
        description: str,
        due_date: Optional[datetime] = None,
        priority: str = "medium",
        status: str = "pending",
    ) -> None:
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    def update(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        due_date: Optional[datetime] = (
            datetime.fromisoformat(data["due_date"]) if data.get("due_date") else None
        )
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=due_date,
            priority=data.get("priority", "medium"),
            status=data.get("status", "pending"),
        )
