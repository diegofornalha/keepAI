from typing import List, Optional, Dict, Any
from models.note import Note
from config.database import SupabaseWrapper


class NoteService:
    def __init__(self) -> None:
        self.db = SupabaseWrapper[Note](Note, "notes")

    async def list_notes(self) -> List[Note]:
        return await self.db.select()

    async def get_note(self, note_id: str) -> Optional[Note]:
        return await self.db.get_by_id(note_id)

    async def create_note(self, note_data: Dict[str, Any]) -> Optional[Note]:
        return await self.db.insert(note_data)

    async def update_note(
        self, note_id: str, note_data: Dict[str, Any]
    ) -> Optional[Note]:
        return await self.db.update(note_id, note_data)

    async def delete_note(self, note_id: str) -> bool:
        return await self.db.delete(note_id)
