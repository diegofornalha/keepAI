from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID
from pydantic import BaseModel, Field


class Conversation(BaseModel):
    """Modelo para conversas com IA."""

    id: UUID
    user_id: str
    message: str
    response: Optional[str] = None
    created_at: datetime
    model_used: str = "gemini-pro"
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Configurações do modelo."""

        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "user_id": "user_2xABCDEF",
                "message": "Como posso melhorar minha produtividade?",
                "response": "Aqui estão algumas dicas...",
                "created_at": "2023-01-01T00:00:00Z",
                "model_used": "gemini-pro",
                "metadata": {"tokens": 150, "context": "productivity"},
            }
        }


class ConversationCreate(BaseModel):
    """Modelo para criação de conversas."""

    message: str
    model_used: Optional[str] = "gemini-pro"
    metadata: Dict[str, Any] = Field(default_factory=dict)
