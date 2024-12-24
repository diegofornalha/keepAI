from typing import List
from fastapi import APIRouter, HTTPException
from models.task import Task, TaskCreate, TaskUpdate
from services.task_service import TaskService

router = APIRouter()
service = TaskService()


@router.get("/tasks", response_model=List[Task])
async def list_tasks() -> List[Task]:
    return await service.list_tasks()


@router.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: str) -> Task:
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/tasks", response_model=Task)
async def create_task(task: TaskCreate) -> Task:
    result = await service.create_task(task.model_dump())
    if not result:
        raise HTTPException(status_code=400, detail="Could not create task")
    return result


@router.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: str, task: TaskUpdate) -> Task:
    result = await service.update_task(task_id, task.model_dump(exclude_unset=True))
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: str) -> bool:
    if not await service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return True
