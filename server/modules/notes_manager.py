"""Gerenciador de notas usando Supabase."""
from typing import Dict, Any, List, Optional
from supabase import Client
from server.config.supabase import get_supabase_client
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class NotesManager:
    """Gerencia operações de notas usando Supabase."""

    def __init__(self) -> None:
        """Inicializa o gerenciador de notas."""
        client = get_supabase_client()
        if not client:
            raise RuntimeError("Não foi possível inicializar o cliente Supabase")
        self.client: Client = client

    def create_note(self, title: str, content: str) -> Dict[str, Any]:
        """
        Cria uma nova nota.

        Args:
            title: Título da nota
            content: Conteúdo da nota

        Returns:
            Dict[str, Any]: Dados da nota criada ou erro
        """
        try:
            data = {"title": title, "content": content}
            response = self.client.table("notes").insert(data).execute()
            return {"success": True, "note": response.data[0]}
        except Exception as e:
            logger.error(f"Erro ao criar nota: {str(e)}")
            return {"success": False, "error": str(e)}

    def update_note(self, note_id: str, content: str) -> Dict[str, Any]:
        """
        Atualiza uma nota existente.

        Args:
            note_id: ID da nota
            content: Novo conteúdo

        Returns:
            Dict[str, Any]: Dados da nota atualizada ou erro
        """
        try:
            data = {"content": content, "updated_at": datetime.utcnow().isoformat()}
            response = (
                self.client.table("notes").update(data).eq("id", note_id).execute()
            )
            return {"success": True, "note": response.data[0]}
        except Exception as e:
            logger.error(f"Erro ao atualizar nota: {str(e)}")
            return {"success": False, "error": str(e)}

    def delete_note(self, note_id: str) -> Dict[str, Any]:
        """
        Deleta uma nota.

        Args:
            note_id: ID da nota

        Returns:
            Dict[str, Any]: Status da operação
        """
        try:
            self.client.table("notes").delete().eq("id", note_id).execute()
            return {"success": True, "message": "Nota deletada com sucesso"}
        except Exception as e:
            logger.error(f"Erro ao deletar nota: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_note(self, query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Busca notas por conteúdo.

        Args:
            query: Texto para buscar nas notas (opcional)

        Returns:
            List[Dict[str, Any]]: Lista de notas encontradas
        """
        try:
            if query:
                # Usando ilike para busca case-insensitive
                response = (
                    self.client.table("notes")
                    .select("*")
                    .ilike("content", f"%{query}%")
                    .execute()
                )
            else:
                response = self.client.table("notes").select("*").execute()

            return response.data
        except Exception as e:
            logger.error(f"Erro ao buscar notas: {str(e)}")
            return []
