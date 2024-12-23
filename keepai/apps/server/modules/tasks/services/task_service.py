from datetime import datetime
from typing import Any, Dict, List

from database.repositories.task_repository import TaskRepository

from ..schemas.task_schema import TaskStats, TaskStatus


class TaskService:
    def __init__(self):
        self.task_repository = TaskRepository()

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Retorna todas as tarefas"""
        return self.task_repository.find_all()

    def get_task_by_id(self, task_id: int) -> Dict[str, Any]:
        """Retorna uma tarefa pelo ID"""
        return self.task_repository.find_by_id(task_id)

    def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Retorna tarefas por status"""
        return self.task_repository.find_by_status(status)

    def get_tasks_by_priority(self, priority: int) -> List[Dict[str, Any]]:
        """Retorna tarefas por prioridade"""
        return self.task_repository.find_by_priority(priority)

    def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Cria uma nova tarefa"""
        # Adicionar timestamps
        task_data["created_at"] = datetime.utcnow().isoformat()
        task_data["updated_at"] = task_data["created_at"]

        # Garantir que tags seja uma lista
        if "tags" in task_data and isinstance(task_data["tags"], str):
            task_data["tags"] = [tag.strip() for tag in task_data["tags"].split(",")]

        return self.task_repository.create(task_data)

    def update_task(self, task_id: int, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Atualiza uma tarefa existente"""
        # Atualizar timestamp
        task_data["updated_at"] = datetime.utcnow().isoformat()

        # Se a tarefa foi completada, adicionar completed_at
        if task_data.get("status") == TaskStatus.completed:
            task_data["completed_at"] = datetime.utcnow().isoformat()

        # Garantir que tags seja uma lista
        if "tags" in task_data and isinstance(task_data["tags"], str):
            task_data["tags"] = [tag.strip() for tag in task_data["tags"].split(",")]

        return self.task_repository.update(task_id, task_data)

    def delete_task(self, task_id: int) -> None:
        """Remove uma tarefa"""
        self.task_repository.delete(task_id)

    def search_tasks(self, query: str) -> List[Dict[str, Any]]:
        """Pesquisa tarefas por título ou descrição"""
        return self.task_repository.search(query)

    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Retorna tarefas atrasadas"""
        return self.task_repository.find_overdue()

    def get_task_stats(self) -> Dict[str, int]:
        """Retorna estatísticas das tarefas"""
        all_tasks = self.task_repository.find_all()
        overdue = self.task_repository.find_overdue()

        stats = {
            "total": len(all_tasks),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "cancelled": 0,
            "overdue": len(overdue),
        }

        for task in all_tasks:
            status = task.get("status")
            if status in stats:
                stats[status] += 1

        return TaskStats(**stats).dict()
