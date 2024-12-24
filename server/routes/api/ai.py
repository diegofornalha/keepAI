from typing import List
from fastapi import APIRouter, HTTPException
from models.conversation import Conversation, ConversationCreate
from services.ai_service import AIService

router = APIRouter()
service = AIService()


@router.get("/conversations", response_model=List[Conversation])
async def list_conversations() -> List[Conversation]:
    return await service.list_conversations()


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: str) -> Conversation:
    conversation = await service.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation


@router.post("/conversations", response_model=Conversation)
async def create_conversation(conversation: ConversationCreate) -> Conversation:
    result = await service.create_conversation(conversation.model_dump())
    if not result:
        raise HTTPException(status_code=400, detail="Could not create conversation")
    return result


@router.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: str, conversation: ConversationCreate
) -> Conversation:
    result = await service.update_conversation(
        conversation_id, conversation.model_dump()
    )
    if not result:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return result


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str) -> bool:
    if not await service.delete_conversation(conversation_id):
        raise HTTPException(status_code=404, detail="Conversation not found")
    return True
