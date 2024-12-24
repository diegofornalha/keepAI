from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Note(BaseModel):
    """Modelo para notas."""

    id: UUID
    user_id: str
    title: str = ""
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Configurações do modelo."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user_2xABCDEF",
                "title": "Minha Nota",
                "content": "Conteúdo da nota...",
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            }
        }


class NoteCreate(BaseModel):
    """Modelo para criação de notas."""

    title: str = ""
    content: str


class NoteUpdate(BaseModel):
    """Modelo para atualização de notas."""

    title: Optional[str] = None
    content: Optional[str] = None
