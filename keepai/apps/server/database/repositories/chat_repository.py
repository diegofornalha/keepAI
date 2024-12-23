from typing import Any, Dict, List, Optional, Callable

from keepai.apps.server.database.config.supabase import SupabaseClient


class ChatRepository:
    """Repositório para operações de banco de dados relacionadas ao chat"""

    def __init__(self, supabase: SupabaseClient):
        """Inicializa o repositório com uma conexão Supabase

        Args:
            supabase: Cliente Supabase
        """
        self.supabase = supabase

    def create_session(self, user_id: str, title: str) -> Dict[str, Any]:
        """Cria uma nova sessão de chat

        Args:
            user_id: ID do usuário
            title: Título da sessão

        Returns:
            Dict[str, Any]: Dados da sessão criada
        """
        result = (
            self.supabase.table("chat_sessions")
            .insert({"user_id": user_id, "title": title})
            .execute()
        )
        return result.data[0]

    def get_user_sessions(
        self, user_id: str, page: int = 1, per_page: int = 10
    ) -> List[Dict[str, Any]]:
        """Retorna todas as sessões de chat de um usuário

        Args:
            user_id: ID do usuário
            page: Número da página
            per_page: Itens por página

        Returns:
            List[Dict[str, Any]]: Lista de sessões
        """
        start = (page - 1) * per_page
        end = start + per_page

        result = (
            self.supabase.table("chat_sessions")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .range(start, end)
            .execute()
        )
        return result.data

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retorna uma sessão específica

        Args:
            session_id: ID da sessão

        Returns:
            Optional[Dict[str, Any]]: Dados da sessão ou None se não encontrada
        """
        result = (
            self.supabase.table("chat_sessions")
            .select("*")
            .eq("id", session_id)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    def update_session(self, session_id: str, **kwargs) -> Dict[str, Any]:
        """Atualiza uma sessão

        Args:
            session_id: ID da sessão
            **kwargs: Campos a serem atualizados

        Returns:
            Dict[str, Any]: Dados da sessão atualizada
        """
        result = (
            self.supabase.table("chat_sessions")
            .update(kwargs)
            .eq("id", session_id)
            .execute()
        )
        return result.data[0]

    def delete_session(self, session_id: str) -> None:
        """Remove uma sessão e suas mensagens

        Args:
            session_id: ID da sessão
        """
        # Remover mensagens
        self.supabase.table("chat_messages").delete().eq(
            "chat_id", session_id
        ).execute()
        # Remover sessão
        self.supabase.table("chat_sessions").delete().eq("id", session_id).execute()

    def create_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova mensagem

        Args:
            message: Dados da mensagem

        Returns:
            Dict[str, Any]: Dados da mensagem criada
        """
        result = self.supabase.table("chat_messages").insert(message).execute()
        return result.data[0]

    def get_chat_messages(
        self, chat_id: str, page: int = 1, per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """Retorna todas as mensagens de um chat

        Args:
            chat_id: ID do chat
            page: Número da página
            per_page: Itens por página

        Returns:
            List[Dict[str, Any]]: Lista de mensagens
        """
        start = (page - 1) * per_page
        end = start + per_page

        result = (
            self.supabase.table("chat_messages")
            .select("*")
            .eq("chat_id", chat_id)
            .order("created_at", desc=True)
            .range(start, end)
            .execute()
        )
        return result.data

    def update_message(self, message_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma mensagem

        Args:
            message_id: ID da mensagem
            data: Dados a serem atualizados

        Returns:
            Dict[str, Any]: Dados da mensagem atualizada
        """
        result = (
            self.supabase.table("chat_messages")
            .update(data)
            .eq("id", message_id)
            .execute()
        )
        return result.data[0]

    def subscribe_to_messages(self, chat_id: str, callback: Callable) -> None:
        """Inscreve para receber novas mensagens em tempo real

        Args:
            chat_id: ID do chat
            callback: Função de callback para novas mensagens
        """
        self.supabase.table("chat_messages").on("INSERT", callback).subscribe()

    def subscribe_to_updates(self, chat_id: str, callback: Callable) -> None:
        """Inscreve para receber atualizações de mensagens em tempo real

        Args:
            chat_id: ID do chat
            callback: Função de callback para atualizações
        """
        self.supabase.table("chat_messages").on("UPDATE", callback).subscribe()
