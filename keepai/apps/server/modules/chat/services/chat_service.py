from datetime import datetime
from typing import Any, Dict, List, Optional

import google.generativeai as genai

from config.settings import GOOGLE_API_KEY
from database.repositories.chat_repository import ChatRepository

from ..schemas.chat_schema import ChatSession, MessageCreate, MessageRole, MessageStatus

# Configurar o Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-pro")


class ChatService:
    def __init__(self):
        self.chat_repository = ChatRepository()
        self.default_context = """Você é um assistente pessoal inteligente chamado Keep AI.
        Você ajuda os usuários com suas tarefas, notas e agenda.
        Seja sempre prestativo, profissional e conciso em suas respostas."""

    def create_session(self, user_id: str, title: str = None) -> ChatSession:
        """Cria uma nova sessão de chat"""
        if not title:
            title = f"Nova conversa - {datetime.utcnow().strftime('%d/%m/%Y %H:%M')}"

        session = self.chat_repository.create_session(user_id, title)

        # Adiciona a mensagem de sistema com o contexto
        self.chat_repository.create_message(
            {
                "content": self.default_context,
                "role": MessageRole.system,
                "chat_id": session["id"],
                "user_id": user_id,
                "status": MessageStatus.completed,
            }
        )

        return ChatSession(**session)

    def get_user_sessions(
        self, user_id: str, page: int = 1, per_page: int = 10
    ) -> List[ChatSession]:
        """Retorna todas as sessões de chat de um usuário"""
        sessions = self.chat_repository.get_user_sessions(user_id, page, per_page)
        return [ChatSession(**session) for session in sessions]

    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """Retorna uma sessão de chat específica"""
        session = self.chat_repository.get_session(session_id)
        return ChatSession(**session) if session else None

    def update_session(self, session_id: str, title: str) -> ChatSession:
        """Atualiza o título de uma sessão"""
        session = self.chat_repository.update_session(session_id, title=title)
        return ChatSession(**session)

    def delete_session(self, session_id: str) -> None:
        """Remove uma sessão de chat e suas mensagens"""
        self.chat_repository.delete_session(session_id)

    async def send_message(
        self, user_id: str, chat_id: str, content: str
    ) -> Dict[str, Any]:
        """Envia uma mensagem e processa a resposta do assistente"""
        # Criar mensagem do usuário
        user_message = self.chat_repository.create_message(
            {
                "content": content,
                "role": MessageRole.user,
                "chat_id": chat_id,
                "user_id": user_id,
                "status": MessageStatus.completed,
            }
        )

        # Criar mensagem do assistente (pendente)
        assistant_message = self.chat_repository.create_message(
            {
                "content": "",
                "role": MessageRole.assistant,
                "chat_id": chat_id,
                "user_id": user_id,
                "status": MessageStatus.processing,
            }
        )

        try:
            # Buscar histórico do chat
            history = self.chat_repository.get_chat_messages(chat_id)
            messages = []

            # Preparar mensagens para o Gemini
            for msg in history:
                if msg["role"] == MessageRole.system:
                    messages.append({"role": "system", "content": msg["content"]})
                elif msg["role"] == MessageRole.user:
                    messages.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == MessageRole.assistant:
                    messages.append({"role": "assistant", "content": msg["content"]})

            # Gerar resposta com o Gemini
            chat = model.start_chat(history=messages)
            response = await chat.send_message_async(content)

            # Atualizar mensagem do assistente
            self.chat_repository.update_message(
                assistant_message["id"],
                {
                    "content": response.text,
                    "status": MessageStatus.completed,
                    "metadata": {
                        "model": "gemini-pro",
                        "prompt_tokens": response.prompt_tokens,
                        "completion_tokens": response.completion_tokens,
                    },
                },
            )

            return {
                "user_message": user_message,
                "assistant_message": assistant_message,
            }

        except Exception as e:
            # Em caso de erro, atualizar status da mensagem
            self.chat_repository.update_message(
                assistant_message["id"],
                {
                    "content": str(e),
                    "status": MessageStatus.failed,
                    "metadata": {"error": str(e)},
                },
            )
            raise

    def get_chat_messages(
        self, chat_id: str, page: int = 1, per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """Retorna todas as mensagens de um chat"""
        return self.chat_repository.get_chat_messages(chat_id, page, per_page)

    def subscribe_to_updates(self, chat_id: str, callback) -> None:
        """Inscreve para receber atualizações em tempo real"""
        self.chat_repository.subscribe_to_messages(chat_id, callback)
        self.chat_repository.subscribe_to_updates(chat_id, callback)
