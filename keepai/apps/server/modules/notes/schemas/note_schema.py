from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Schema base para notas"""

    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    tags: Optional[List[str]] = Field(default=[])


class NoteCreate(NoteBase):
    """Schema para criação de notas"""

    pass


class NoteUpdate(BaseModel):
    """Schema para atualização de notas"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    tags: Optional[List[str]] = None


class NoteInDB(NoteBase):
    """Schema para notas no banco de dados"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class NoteResponse(NoteInDB):
    """Schema para resposta da API"""

    pass


class NoteList(BaseModel):
    """Schema para lista de notas"""

    notes: List[NoteResponse]
    total: int
    page: int = 1
    per_page: int = 10


class TagList(BaseModel):
    """Schema para lista de tags"""

    tags: List[str]
