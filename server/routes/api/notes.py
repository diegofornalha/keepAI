from typing import List
from fastapi import APIRouter, HTTPException
from models.note import Note, NoteCreate, NoteUpdate
from services.note_service import NoteService

router = APIRouter()
service = NoteService()


@router.get("/notes", response_model=List[Note])
async def list_notes() -> List[Note]:
    return await service.list_notes()


@router.get("/notes/{note_id}", response_model=Note)
async def get_note(note_id: str) -> Note:
    note = await service.get_note(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/notes", response_model=Note)
async def create_note(note: NoteCreate) -> Note:
    result = await service.create_note(note.model_dump())
    if not result:
        raise HTTPException(status_code=400, detail="Could not create note")
    return result


@router.put("/notes/{note_id}", response_model=Note)
async def update_note(note_id: str, note: NoteUpdate) -> Note:
    result = await service.update_note(note_id, note.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Note not found")
    return result


@router.delete("/notes/{note_id}")
async def delete_note(note_id: str) -> bool:
    if not await service.delete_note(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return True
