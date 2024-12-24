from typing import List, Dict, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import HTTPBearer

from models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from services.task_service import TaskService
from config.logging_config import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])
security = HTTPBearer()


@router.post("/", response_model=Task)
async def create_task(task_data: TaskCreate, user_id: UUID = Depends(security)) -> Task:
    """Cria uma nova tarefa."""
    try:
        task = await TaskService.create_task(str(user_id), task_data)
        if not task:
            raise HTTPException(status_code=400, detail="Erro ao criar tarefa")
        return task
    except HTTPException as e:
        logger.error(f"Erro ao criar tarefa: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao criar tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: UUID, user_id: UUID = Depends(security)) -> Task:
    """Busca uma tarefa específica."""
    try:
        task = await TaskService.get_task(task_id, str(user_id))
        if not task:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return task
    except HTTPException as e:
        logger.error(f"Erro ao buscar tarefa: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao buscar tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.get("/", response_model=List[Task])
async def list_tasks(
    status: Optional[TaskStatus] = Query(None, description="Filtrar por status"),
    user_id: UUID = Depends(security),
) -> List[Task]:
    """Lista todas as tarefas do usuário."""
    try:
        status_value = status.value if status else None
        return await TaskService.list_tasks(str(user_id), status_value)  # type: ignore
    except Exception as e:
        logger.error(f"Erro ao listar tarefas: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: UUID, task_data: TaskUpdate, user_id: UUID = Depends(security)
) -> Task:
    """Atualiza uma tarefa."""
    try:
        task = await TaskService.update_task(task_id, str(user_id), task_data)
        if not task:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return task
    except HTTPException as e:
        logger.error(f"Erro ao atualizar tarefa: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID, user_id: UUID = Depends(security)
) -> Dict[str, str]:
    """Deleta uma tarefa."""
    try:
        success = await TaskService.delete_task(task_id, str(user_id))
        if not success:
            raise HTTPException(status_code=404, detail="Tarefa não encontrada")
        return {"message": "Tarefa deletada com sucesso"}
    except HTTPException as e:
        logger.error(f"Erro ao deletar tarefa: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar tarefa: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")
