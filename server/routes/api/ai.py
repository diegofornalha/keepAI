from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from models.conversation import Conversation, ConversationCreate
from services.ai_service import AIService
from config.logging_config import logger

router = APIRouter(prefix="/ai", tags=["ai"])
security = HTTPBearer()


@router.post("/chat", response_model=Conversation)
async def create_chat(
    conversation_data: ConversationCreate, user_id: UUID = Depends(security)
) -> Conversation:
    """Cria uma nova conversa com a IA."""
    try:
        conversation = await AIService.create_conversation(
            str(user_id), conversation_data
        )
        if not conversation:
            raise HTTPException(status_code=400, detail="Erro ao criar conversa")
        return conversation
    except HTTPException as e:
        logger.error(f"Erro ao criar conversa: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao criar conversa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/conversations", response_model=List[Conversation])
async def list_conversations(user_id: UUID = Depends(security)) -> List[Conversation]:
    """Lista todas as conversas do usuário."""
    try:
        return await AIService.list_conversations(str(user_id))
    except Exception as e:
        logger.error(f"Erro ao listar conversas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: UUID, user_id: UUID = Depends(security)
) -> Conversation:
    """Busca uma conversa específica."""
    try:
        conversation = await AIService.get_conversation(conversation_id, str(user_id))
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversa não encontrada")
        return conversation
    except HTTPException as e:
        logger.error(f"Erro ao buscar conversa: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar conversa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
