from typing import List, Optional, Dict, Any
from models.task import Task
from config.database import SupabaseWrapper


class TaskService:
    def __init__(self) -> None:
        self.db = SupabaseWrapper[Task](Task, "tasks")

    async def list_tasks(self) -> List[Task]:
        return await self.db.select()

    async def get_task(self, task_id: str) -> Optional[Task]:
        return await self.db.get_by_id(task_id)

    async def create_task(self, task_data: Dict[str, Any]) -> Optional[Task]:
        return await self.db.insert(task_data)

    async def update_task(
        self, task_id: str, task_data: Dict[str, Any]
    ) -> Optional[Task]:
        return await self.db.update(task_id, task_data)

    async def delete_task(self, task_id: str) -> bool:
        return await self.db.delete(task_id)
