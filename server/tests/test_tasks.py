import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException

from server.services.task_service import TaskService
from server.models.task import TaskStatus


@pytest.mark.asyncio
async def test_create_task_success(client, test_user, test_task, test_task_create):
    """Testa criação de tarefa com sucesso."""
    with patch.object(
        TaskService, "create_task", new_callable=AsyncMock
    ) as mock_create_task:
        mock_create_task.return_value = test_task
        response = client.post(
            "/api/tasks/",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=test_task_create.model_dump()
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_task.title
        assert data["description"] == test_task.description


@pytest.mark.asyncio
async def test_create_task_failure(client, test_user, test_task_create):
    """Testa falha na criação de tarefa."""
    with patch.object(
        TaskService, "create_task", new_callable=AsyncMock
    ) as mock_create_task:
        mock_create_task.return_value = None
        response = client.post(
            "/api/tasks/",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=test_task_create.model_dump()
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_task_success(client, test_user, test_task):
    """Testa busca de tarefa com sucesso."""
    with patch.object(
        TaskService, "get_task", new_callable=AsyncMock
    ) as mock_get_task:
        mock_get_task.return_value = test_task
        response = client.get(
            f"/api/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_task.id)
        assert data["title"] == test_task.title


@pytest.mark.asyncio
async def test_get_task_not_found(client, test_user, test_task):
    """Testa busca de tarefa não encontrada."""
    with patch.object(
        TaskService, "get_task", new_callable=AsyncMock
    ) as mock_get_task:
        mock_get_task.return_value = None
        response = client.get(
            f"/api/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_tasks_success(client, test_user, test_task):
    """Testa listagem de tarefas com sucesso."""
    with patch.object(
        TaskService, "list_tasks", new_callable=AsyncMock
    ) as mock_list_tasks:
        mock_list_tasks.return_value = [test_task]
        response = client.get(
            "/api/tasks/",
            headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == str(test_task.id)


@pytest.mark.asyncio
async def test_list_tasks_with_filter(client, test_user, test_task):
    """Testa listagem de tarefas com filtro de status."""
    with patch.object(
        TaskService, "list_tasks", new_callable=AsyncMock
    ) as mock_list_tasks:
        mock_list_tasks.return_value = [test_task]
        response = client.get(
            "/api/tasks/?status=pending",
            headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["status"] == TaskStatus.PENDING.value


@pytest.mark.asyncio
async def test_update_task_success(client, test_user, test_task):
    """Testa atualização de tarefa com sucesso."""
    update_data = {
        "title": "Updated Title",
        "status": TaskStatus.COMPLETED.value
    }
    with patch.object(
        TaskService, "update_task", new_callable=AsyncMock
    ) as mock_update_task:
        updated_task = test_task.model_copy(update=update_data)
        mock_update_task.return_value = updated_task
        response = client.put(
            f"/api/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == TaskStatus.COMPLETED.value


@pytest.mark.asyncio
async def test_delete_task_success(client, test_user, test_task):
    """Testa deleção de tarefa com sucesso."""
    with patch.object(
        TaskService, "delete_task", new_callable=AsyncMock
    ) as mock_delete_task:
        mock_delete_task.return_value = True
        response = client.delete(
            f"/api/tasks/{test_task.id}",
            headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Tarefa deletada com sucesso" 