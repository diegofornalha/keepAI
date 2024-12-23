from typing import Any, Dict, List, Optional

from ..config.supabase import get_supabase


class ChatRepository:
    def __init__(self):
        self.supabase = get_supabase()

    def create_session(self, user_id: str, title: str) -> Dict[str, Any]:
        """Cria uma nova sessão de chat"""
        result = (
            self.supabase.table("chat_sessions")
            .insert({"user_id": user_id, "title": title})
            .execute()
        )
        return result.data[0]

    def get_user_sessions(
        self, user_id: str, page: int = 1, per_page: int = 10
    ) -> List[Dict[str, Any]]:
        """Retorna todas as sessões de chat de um usuário"""
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
        """Retorna uma sessão específica"""
        result = (
            self.supabase.table("chat_sessions")
            .select("*")
            .eq("id", session_id)
            .limit(1)
            .execute()
        )
        return result.data[0] if result.data else None

    def update_session(self, session_id: str, **kwargs) -> Dict[str, Any]:
        """Atualiza uma sessão"""
        result = (
            self.supabase.table("chat_sessions")
            .update(kwargs)
            .eq("id", session_id)
            .execute()
        )
        return result.data[0]

    def delete_session(self, session_id: str) -> None:
        """Remove uma sessão e suas mensagens"""
        # Remover mensagens
        self.supabase.table("chat_messages").delete().eq(
            "chat_id", session_id
        ).execute()
        # Remover sessão
        self.supabase.table("chat_sessions").delete().eq("id", session_id).execute()

    def create_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova mensagem"""
        result = self.supabase.table("chat_messages").insert(message).execute()
        return result.data[0]

    def get_chat_messages(
        self, chat_id: str, page: int = 1, per_page: int = 50
    ) -> List[Dict[str, Any]]:
        """Retorna todas as mensagens de um chat"""
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
        """Atualiza uma mensagem"""
        result = (
            self.supabase.table("chat_messages")
            .update(data)
            .eq("id", message_id)
            .execute()
        )
        return result.data[0]

    def subscribe_to_messages(self, chat_id: str, callback) -> None:
        """Inscreve para receber novas mensagens em tempo real"""
        self.supabase.table("chat_messages").on("INSERT", callback).subscribe()

    def subscribe_to_updates(self, chat_id: str, callback) -> None:
        """Inscreve para receber atualizações de mensagens em tempo real"""
        self.supabase.table("chat_messages").on("UPDATE", callback).subscribe()
