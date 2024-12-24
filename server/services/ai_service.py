from typing import Optional, List
from uuid import UUID

from models.conversation import Conversation, ConversationCreate
from config.database import supabase_client
from modules.agent import KeepAIAgent


class AIService:
    """Serviço para gerenciamento de conversas com IA."""

    def __init__(self) -> None:
        """Inicializa o serviço com uma instância do agente."""
        self.agent = KeepAIAgent()

    async def create_conversation(
        self, user_id: str, conversation_data: ConversationCreate
    ) -> Optional[Conversation]:
        """Cria uma nova conversa e processa a mensagem."""
        try:
            # Processa a mensagem com o agente
            response = self.process_message(conversation_data.message)

            # Prepara os dados para inserção
            data = conversation_data.model_dump()
            data.update(
                {
                    "user_id": user_id,
                    "response": response,
                    "model_used": conversation_data.model_used or "gemini-pro",
                }
            )

            # Insere no banco de dados
            db_response = (
                await supabase_client.table("conversations").insert(data).execute()
            )
            if db_response.data:
                return Conversation.model_validate(db_response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao criar conversa: {e}")
            return None

    async def get_conversation(
        self, conversation_id: UUID, user_id: str
    ) -> Optional[Conversation]:
        """Busca uma conversa específica."""
        try:
            response = (
                await supabase_client.table("conversations")
                .select("*")
                .eq("id", str(conversation_id))
                .eq("user_id", user_id)
                .single()
            )
            if response.data:
                return Conversation.model_validate(response.data)
            return None
        except Exception as e:
            print(f"Erro ao buscar conversa: {e}")
            return None

    async def list_conversations(self, user_id: str) -> List[Conversation]:
        """Lista todas as conversas de um usuário."""
        try:
            response = (
                await supabase_client.table("conversations")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            return [Conversation.model_validate(conv) for conv in response.data]
        except Exception as e:
            print(f"Erro ao listar conversas: {e}")
            return []

    def process_message(self, message: str) -> str:
        """Processa uma mensagem usando o agente."""
        try:
            response = self.agent.get_agent().invoke({"input": message})

            if not response or not isinstance(response, (str, dict)):
                raise ValueError("Resposta inválida do agente")

            if isinstance(response, dict):
                response = response.get("output", "")

            return str(response)

        except Exception as error:
            error_msg = str(error)
            if "safety" in error_msg.lower():
                return (
                    "Desculpe, não posso processar esse tipo de conteúdo "
                    "por questões de segurança. 🚫"
                )
            elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
                return (
                    "Desculpe, estou temporariamente indisponível. "
                    "Por favor, tente novamente em alguns minutos. ⏳"
                )
            else:
                return (
                    "Desculpe, ocorreu um erro ao processar sua mensagem. "
                    "Por favor, tente novamente. 🔄"
                )
