from typing import List, Optional, Dict, Any
from models.conversation import Conversation
from config.database import SupabaseWrapper


class AIService:
    def __init__(self) -> None:
        self.db = SupabaseWrapper[Conversation](Conversation, "conversations")

    async def list_conversations(self) -> List[Conversation]:
        return await self.db.select()

    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        return await self.db.get_by_id(conversation_id)

    async def create_conversation(
        self, conversation_data: Dict[str, Any]
    ) -> Optional[Conversation]:
        return await self.db.insert(conversation_data)

    async def update_conversation(
        self, conversation_id: str, conversation_data: Dict[str, Any]
    ) -> Optional[Conversation]:
        return await self.db.update(conversation_id, conversation_data)

    async def delete_conversation(self, conversation_id: str) -> bool:
        return await self.db.delete(conversation_id)
