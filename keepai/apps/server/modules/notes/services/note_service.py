from datetime import datetime
from typing import Any, Dict, List

from database.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self):
        self.note_repository = NoteRepository()

    def get_all_notes(self) -> List[Dict[str, Any]]:
        """Retorna todas as notas"""
        return self.note_repository.find_all()

    def get_note_by_id(self, note_id: int) -> Dict[str, Any]:
        """Retorna uma nota pelo ID"""
        return self.note_repository.find_by_id(note_id)

    def get_notes_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """Retorna notas por tag"""
        return self.note_repository.find_by_tag(tag)

    def create_note(self, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova nota"""
        # Adicionar timestamps
        note_data["created_at"] = datetime.utcnow().isoformat()
        note_data["updated_at"] = note_data["created_at"]

        # Garantir que tags seja uma lista
        if "tags" in note_data and isinstance(note_data["tags"], str):
            note_data["tags"] = [tag.strip() for tag in note_data["tags"].split(",")]

        return self.note_repository.create(note_data)

    def update_note(self, note_id: int, note_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma nota existente"""
        # Atualizar timestamp
        note_data["updated_at"] = datetime.utcnow().isoformat()

        # Garantir que tags seja uma lista
        if "tags" in note_data and isinstance(note_data["tags"], str):
            note_data["tags"] = [tag.strip() for tag in note_data["tags"].split(",")]

        return self.note_repository.update(note_id, note_data)

    def delete_note(self, note_id: int) -> None:
        """Remove uma nota"""
        self.note_repository.delete(note_id)

    def search_notes(self, query: str) -> List[Dict[str, Any]]:
        """Pesquisa notas por título ou conteúdo"""
        return self.note_repository.search(query)

    def get_all_tags(self) -> List[str]:
        """Retorna todas as tags únicas"""
        notes = self.note_repository.find_all()
        tags = set()
        for note in notes:
            if note.get("tags"):
                tags.update(note["tags"])
        return sorted(list(tags))
