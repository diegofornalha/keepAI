from typing import List, Dict
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from models.note import Note, NoteCreate, NoteUpdate
from services.note_service import NoteService
from config.logging_config import logger

router = APIRouter(prefix="/notes", tags=["notes"])
security = HTTPBearer()


@router.post("/", response_model=Note)
async def create_note(note_data: NoteCreate, user_id: UUID = Depends(security)) -> Note:
    """Cria uma nova nota."""
    try:
        note = await NoteService.create_note(str(user_id), note_data)
        if not note:
            raise HTTPException(status_code=400, detail="Erro ao criar nota")
        return note
    except HTTPException as e:
        logger.error(f"Erro ao criar nota: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao criar nota: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/{note_id}", response_model=Note)
async def get_note(note_id: UUID, user_id: UUID = Depends(security)) -> Note:
    """Busca uma nota específica."""
    try:
        note = await NoteService.get_note(note_id, str(user_id))
        if not note:
            raise HTTPException(status_code=404, detail="Nota não encontrada")
        return note
    except HTTPException as e:
        logger.error(f"Erro ao buscar nota: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar nota: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/", response_model=List[Note])
async def list_notes(user_id: UUID = Depends(security)) -> List[Note]:
    """Lista todas as notas do usuário."""
    try:
        return await NoteService.list_notes(str(user_id))
    except Exception as e:
        logger.error(f"Erro ao listar notas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.put("/{note_id}", response_model=Note)
async def update_note(
    note_id: UUID, note_data: NoteUpdate, user_id: UUID = Depends(security)
) -> Note:
    """Atualiza uma nota."""
    try:
        note = await NoteService.update_note(note_id, str(user_id), note_data)
        if not note:
            raise HTTPException(status_code=404, detail="Nota não encontrada")
        return note
    except HTTPException as e:
        logger.error(f"Erro ao atualizar nota: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar nota: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.delete("/{note_id}")
async def delete_note(
    note_id: UUID, user_id: UUID = Depends(security)
) -> Dict[str, str]:
    """Deleta uma nota."""
    try:
        success = await NoteService.delete_note(note_id, str(user_id))
        if not success:
            raise HTTPException(status_code=404, detail="Nota não encontrada")
        return {"message": "Nota deletada com sucesso"}
    except HTTPException as e:
        logger.error(f"Erro ao deletar nota: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar nota: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
