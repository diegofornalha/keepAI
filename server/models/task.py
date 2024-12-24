from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from enum import Enum


class TaskStatus(str, Enum):
    """Enum para status de tarefas."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(str, Enum):
    """Enum para prioridade de tarefas."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    """Modelo para tarefas."""

    id: UUID
    user_id: str
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Configurações do modelo."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user_2xABCDEF",
                "title": "Completar relatório",
                "description": "Finalizar relatório mensal de vendas",
                "status": "pending",
                "priority": "high",
                "due_date": "2023-12-31T23:59:59Z",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            }
        }


class TaskCreate(BaseModel):
    """Modelo para criação de tarefas."""

    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None


class TaskUpdate(BaseModel):
    """Modelo para atualização de tarefas."""

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
