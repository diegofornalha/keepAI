from typing import Optional, List
from uuid import UUID

from models.conversation import Conversation, ConversationCreate
from config.database import supabase_client


class AIService:
    """Serviço para gerenciamento de conversas com IA."""

    @staticmethod
    async def create_conversation(
        user_id: str, conversation_data: ConversationCreate
    ) -> Optional[Conversation]:
        """Cria uma nova conversa."""
        try:
            data = {
                "user_id": user_id,
                "message": conversation_data.message,
                "model_used": conversation_data.model_used,
                "metadata": conversation_data.metadata,
            }
            response = (
                await supabase_client.table("conversations").insert(data).execute()
            )
            if response.data:
                return Conversation.model_validate(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao criar conversa: {e}")
            return None

    @staticmethod
    async def get_conversation(
        conversation_id: UUID, user_id: str
    ) -> Optional[Conversation]:
        """Busca uma conversa específica."""
        try:
            response = (
                await supabase_client.table("conversations")
                .select("*")
                .eq("id", str(conversation_id))
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            if response.data:
                return Conversation.model_validate(response.data)
            return None
        except Exception as e:
            print(f"Erro ao buscar conversa: {e}")
            return None

    @staticmethod
    async def list_conversations(user_id: str) -> List[Conversation]:
        """Lista todas as conversas do usuário."""
        try:
            response = (
                await supabase_client.table("conversations")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            return [Conversation.model_validate(conv) for conv in response.data]
        except Exception as e:
            print(f"Erro ao listar conversas: {e}")
            return []

    @staticmethod
    async def delete_conversation(conversation_id: UUID, user_id: str) -> bool:
        """Deleta uma conversa."""
        try:
            response = (
                await supabase_client.table("conversations")
                .delete()
                .eq("id", str(conversation_id))
                .eq("user_id", user_id)
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            print(f"Erro ao deletar conversa: {e}")
            return False
