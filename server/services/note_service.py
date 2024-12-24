from typing import Optional, List
from uuid import UUID

from models.note import Note, NoteCreate, NoteUpdate
from config.database import supabase_client


class NoteService:
    """Serviço para gerenciamento de notas."""

    @staticmethod
    async def create_note(user_id: str, note_data: NoteCreate) -> Optional[Note]:
        """Cria uma nova nota."""
        try:
            data = note_data.model_dump()
            data["user_id"] = user_id
            response = await supabase_client.table("notes").insert(data).execute()
            if response.data:
                return Note.model_validate(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao criar nota: {e}")
            return None

    @staticmethod
    async def get_note(note_id: UUID, user_id: str) -> Optional[Note]:
        """Busca uma nota específica."""
        try:
            response = (
                await supabase_client.table("notes")
                .select("*")
                .eq("id", str(note_id))
                .eq("user_id", user_id)
                .single()
            )
            if response.data:
                return Note.model_validate(response.data)
            return None
        except Exception as e:
            print(f"Erro ao buscar nota: {e}")
            return None

    @staticmethod
    async def list_notes(user_id: str) -> List[Note]:
        """Lista todas as notas de um usuário."""
        try:
            response = (
                await supabase_client.table("notes")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .execute()
            )
            return [Note.model_validate(note) for note in response.data]
        except Exception as e:
            print(f"Erro ao listar notas: {e}")
            return []

    @staticmethod
    async def update_note(
        note_id: UUID, user_id: str, note_data: NoteUpdate
    ) -> Optional[Note]:
        """Atualiza uma nota."""
        try:
            data = note_data.model_dump(exclude_unset=True)
            response = (
                await supabase_client.table("notes")
                .update(data)
                .eq("id", str(note_id))
                .eq("user_id", user_id)
                .execute()
            )
            if response.data:
                return Note.model_validate(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao atualizar nota: {e}")
            return None

    @staticmethod
    async def delete_note(note_id: UUID, user_id: str) -> bool:
        """Deleta uma nota."""
        try:
            response = (
                await supabase_client.table("notes")
                .delete()
                .eq("id", str(note_id))
                .eq("user_id", user_id)
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            print(f"Erro ao deletar nota: {e}")
            return False
