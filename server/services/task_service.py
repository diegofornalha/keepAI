from typing import Optional, List
from uuid import UUID

from models.task import Task, TaskCreate, TaskUpdate, TaskStatus
from config.database import supabase_client


class TaskService:
    """Serviço para gerenciamento de tarefas."""

    @staticmethod
    async def create_task(user_id: str, task_data: TaskCreate) -> Optional[Task]:
        """Cria uma nova tarefa."""
        try:
            data = {
                "user_id": user_id,
                "title": task_data.title,
                "description": task_data.description,
                "priority": task_data.priority.value,
                "status": TaskStatus.PENDING.value,
                "due_date": task_data.due_date.isoformat()
                if task_data.due_date
                else None,
            }
            response = await supabase_client.table("tasks").insert(data).execute()
            if response.data:
                return Task.model_validate(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao criar tarefa: {e}")
            return None

    @staticmethod
    async def get_task(task_id: UUID, user_id: str) -> Optional[Task]:
        """Busca uma tarefa específica."""
        try:
            response = (
                await supabase_client.table("tasks")
                .select("*")
                .eq("id", str(task_id))
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            if response.data:
                return Task.model_validate(response.data)
            return None
        except Exception as e:
            print(f"Erro ao buscar tarefa: {e}")
            return None

    @staticmethod
    async def list_tasks(user_id: str, status: Optional[str] = None) -> List[Task]:
        """Lista todas as tarefas do usuário."""
        try:
            query = supabase_client.table("tasks").select("*").eq("user_id", user_id)
            if status:
                query = query.eq("status", status)
            response = await query.execute()
            return [Task.model_validate(task) for task in response.data]
        except Exception as e:
            print(f"Erro ao listar tarefas: {e}")
            return []

    @staticmethod
    async def update_task(
        task_id: UUID, user_id: str, task_data: TaskUpdate
    ) -> Optional[Task]:
        """Atualiza uma tarefa."""
        try:
            data = task_data.model_dump(exclude_unset=True)
            if task_data.due_date:
                data["due_date"] = task_data.due_date.isoformat()
            response = (
                await supabase_client.table("tasks")
                .update(data)
                .eq("id", str(task_id))
                .eq("user_id", user_id)
                .execute()
            )
            if response.data:
                return Task.model_validate(response.data[0])
            return None
        except Exception as e:
            print(f"Erro ao atualizar tarefa: {e}")
            return None

    @staticmethod
    async def delete_task(task_id: UUID, user_id: str) -> bool:
        """Deleta uma tarefa."""
        try:
            response = (
                await supabase_client.table("tasks")
                .delete()
                .eq("id", str(task_id))
                .eq("user_id", user_id)
                .execute()
            )
            return bool(response.data)
        except Exception as e:
            print(f"Erro ao deletar tarefa: {e}")
            return False
