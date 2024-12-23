from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Status possíveis para uma tarefa"""

    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class TaskPriority(int, Enum):
    """Níveis de prioridade para uma tarefa"""

    low = 1
    medium = 2
    high = 3
    urgent = 4


class TaskBase(BaseModel):
    """Schema base para tarefas"""

    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: TaskPriority = Field(default=TaskPriority.medium)
    status: TaskStatus = Field(default=TaskStatus.pending)
    tags: Optional[List[str]] = Field(default=[])


class TaskCreate(TaskBase):
    """Schema para criação de tarefas"""

    pass


class TaskUpdate(BaseModel):
    """Schema para atualização de tarefas"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    due_date: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    tags: Optional[List[str]] = None


class TaskInDB(TaskBase):
    """Schema para tarefas no banco de dados"""

    id: int
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TaskResponse(TaskInDB):
    """Schema para resposta da API"""

    pass


class TaskList(BaseModel):
    """Schema para lista de tarefas"""

    tasks: List[TaskResponse]
    total: int
    page: int = 1
    per_page: int = 10


class TaskStats(BaseModel):
    """Schema para estatísticas de tarefas"""

    total: int
    pending: int
    in_progress: int
    completed: int
    cancelled: int
    overdue: int
