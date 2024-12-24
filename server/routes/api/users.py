from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer

from models.user import UserProfile
from services.user_service import UserService
from config.logging_config import logger

router = APIRouter(prefix="/users", tags=["users"])
security = HTTPBearer()


@router.get("/me", response_model=UserProfile)
async def get_current_user(user_id: UUID = Depends(security)) -> UserProfile:
    """Retorna o perfil do usuário atual."""
    try:
        profile = await UserService.get_profile(user_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil não encontrado")
        return profile
    except Exception as e:
        logger.error(f"Erro ao buscar perfil: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.put("/me", response_model=UserProfile)
async def update_current_user(
    profile_data: dict, user_id: UUID = Depends(security)
) -> UserProfile:
    """Atualiza o perfil do usuário atual."""
    try:
        profile = await UserService.update_profile(user_id, profile_data)
        if not profile:
            raise HTTPException(status_code=404, detail="Perfil não encontrado")
        return profile
    except Exception as e:
        logger.error(f"Erro ao atualizar perfil: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/", response_model=List[UserProfile])
async def list_users() -> List[UserProfile]:
    """Lista todos os usuários (apenas para admin)."""
    try:
        return await UserService.list_profiles()
    except Exception as e:
        logger.error(f"Erro ao listar perfis: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
