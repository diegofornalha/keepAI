from fastapi import APIRouter

from .users import router as users_router
from .notes import router as notes_router
from .tasks import router as tasks_router
from .ai import router as ai_router

# Cria o router principal da API
api_router = APIRouter(prefix="/api")

# Inclui todos os routers
api_router.include_router(users_router)
api_router.include_router(notes_router)
api_router.include_router(tasks_router)
api_router.include_router(ai_router)

__all__ = ["api_router"]
