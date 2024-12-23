from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Roles possíveis para mensagens"""

    user = "user"
    assistant = "assistant"
    system = "system"


class MessageStatus(str, Enum):
    """Status possíveis para mensagens"""

    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class MessageBase(BaseModel):
    """Schema base para mensagens"""

    content: str = Field(..., min_length=1)
    role: MessageRole
    chat_id: str = Field(..., description="ID único da conversa")
    user_id: str = Field(..., description="ID do usuário que enviou a mensagem")
    status: MessageStatus = Field(default=MessageStatus.pending)
    metadata: Optional[Dict[str, Any]] = Field(default={})


class MessageCreate(MessageBase):
    """Schema para criação de mensagens"""

    pass


class MessageUpdate(BaseModel):
    """Schema para atualização de mensagens"""

    content: Optional[str] = Field(None, min_length=1)
    status: Optional[MessageStatus] = None
    metadata: Optional[Dict[str, Any]] = None


class MessageInDB(MessageBase):
    """Schema para mensagens no banco de dados"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(MessageInDB):
    """Schema para resposta da API"""

    pass


class ChatSession(BaseModel):
    """Schema para sessão de chat"""

    id: str
    title: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    metadata: Optional[Dict[str, Any]] = Field(default={})


class ChatList(BaseModel):
    """Schema para lista de chats"""

    chats: List[ChatSession]
    total: int
    page: int = 1
    per_page: int = 10


class ChatMessages(BaseModel):
    """Schema para mensagens de um chat"""

    messages: List[MessageResponse]
    total: int
    chat_id: str
    page: int = 1
    per_page: int = 50
