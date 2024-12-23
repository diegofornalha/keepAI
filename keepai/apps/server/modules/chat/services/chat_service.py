from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol

import google.generativeai as genai
from flask import current_app

from keepai.apps.server.config.settings import GOOGLE_API_KEY
from keepai.apps.server.database.repositories.chat_repository import ChatRepository
from keepai.apps.server.modules.chat.schemas.chat_schema import (
    ChatSession,
    MessageCreate,
    MessageRole,
    MessageStatus,
)


class ChatRepositoryProtocol(Protocol):
    """Protocolo para o repositório de chat"""

    def create_session(self, user_id: str, title: str) -> Dict[str, Any]: ...
    def get_user_sessions(
        self, user_id: str, page: int, per_page: int
    ) -> List[Dict[str, Any]]: ...
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]: ...
    def update_session(self, session_id: str, **kwargs) -> Dict[str, Any]: ...
    def delete_session(self, session_id: str) -> None: ...
    def create_message(self, message: Dict[str, Any]) -> Dict[str, Any]: ...
    def get_chat_messages(
        self, chat_id: str, page: int, per_page: int
    ) -> List[Dict[str, Any]]: ...
    def update_message(
        self, message_id: str, data: Dict[str, Any]
    ) -> Dict[str, Any]: ...
    def subscribe_to_messages(self, chat_id: str, callback) -> None: ...
    def subscribe_to_updates(self, chat_id: str, callback) -> None: ...


class ChatService:
    """Serviço responsável pela lógica de negócio do chat"""

    def __init__(self, repository: Optional[ChatRepositoryProtocol] = None):
        """Inicializa o serviço de chat

        Args:
            repository: Repositório de chat opcional
        """
        self.chat_repository = repository or ChatRepository()
        self.default_context = """Você é um assistente pessoal inteligente chamado Keep AI.
        Você ajuda os usuários com suas tarefas, notas e agenda.
        Seja sempre prestativo, profissional e conciso em suas respostas."""

        # Configurar o Gemini
        genai.configure(api_key=GOOGLE_API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")

    def create_session(self, user_id: str, title: Optional[str] = None) -> ChatSession:
        """Cria uma nova sessão de chat

        Args:
            user_id: ID do usuário
            title: Título opcional da sessão

        Returns:
            ChatSession: Sessão criada
        """
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
        """Retorna todas as sessões de chat de um usuário

        Args:
            user_id: ID do usuário
            page: Número da página
            per_page: Itens por página

        Returns:
            List[ChatSession]: Lista de sessões
        """
        sessions = self.chat_repository.get_user_sessions(user_id, page, per_page)
        return [ChatSession(**session) for session in sessions]

    async def send_message(
        self, user_id: str, chat_id: str, content: str
    ) -> Dict[str, Any]:
        """Envia uma mensagem e processa a resposta do assistente

        Args:
            user_id: ID do usuário
            chat_id: ID do chat
            content: Conteúdo da mensagem

        Returns:
            Dict[str, Any]: Mensagens do usuário e do assistente

        Raises:
            Exception: Se houver erro ao processar a mensagem
        """
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
            messages = self._prepare_messages_for_model(history)

            # Gerar resposta com o Gemini
            chat = self.model.start_chat(history=messages)
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
            current_app.logger.error(f"Erro ao processar mensagem: {str(e)}")
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

    def _prepare_messages_for_model(
        self, history: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """Prepara as mensagens para o modelo

        Args:
            history: Histórico de mensagens

        Returns:
            List[Dict[str, str]]: Mensagens formatadas
        """
        messages = []
        for msg in history:
            if msg["role"] == MessageRole.system:
                messages.append({"role": "system", "content": msg["content"]})
            elif msg["role"] == MessageRole.user:
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == MessageRole.assistant:
                messages.append({"role": "assistant", "content": msg["content"]})
        return messages
