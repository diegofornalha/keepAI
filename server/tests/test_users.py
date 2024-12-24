import pytest
from unittest.mock import patch, AsyncMock
from fastapi import HTTPException

from server.services.user_service import UserService


@pytest.mark.asyncio
async def test_get_current_user_success(client, test_user):
    """Testa busca do usuário atual com sucesso."""
    with patch.object(
        UserService, "get_profile", new_callable=AsyncMock
    ) as mock_get_profile:
        mock_get_profile.return_value = test_user
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["email"] == test_user.email


@pytest.mark.asyncio
async def test_get_current_user_not_found(client, test_user):
    """Testa busca do usuário atual não encontrado."""
    with patch.object(
        UserService, "get_profile", new_callable=AsyncMock
    ) as mock_get_profile:
        mock_get_profile.return_value = None
        response = client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_current_user_success(client, test_user):
    """Testa atualização do usuário atual com sucesso."""
    update_data = {
        "first_name": "Updated",
        "last_name": "Name"
    }
    with patch.object(
        UserService, "update_profile", new_callable=AsyncMock
    ) as mock_update_profile:
        updated_user = test_user.model_copy(update=update_data)
        mock_update_profile.return_value = updated_user
        response = client.put(
            "/api/users/me",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Updated"
        assert data["last_name"] == "Name"


@pytest.mark.asyncio
async def test_update_current_user_not_found(client, test_user):
    """Testa atualização do usuário atual não encontrado."""
    with patch.object(
        UserService, "update_profile", new_callable=AsyncMock
    ) as mock_update_profile:
        mock_update_profile.return_value = None
        response = client.put(
            "/api/users/me",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json={"first_name": "Updated"}
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_users_success(client, test_user):
    """Testa listagem de usuários com sucesso."""
    with patch.object(
        UserService, "list_profiles", new_callable=AsyncMock
    ) as mock_list_profiles:
        mock_list_profiles.return_value = [test_user]
        response = client.get("/api/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["username"] == test_user.username


@pytest.mark.asyncio
async def test_list_users_empty(client):
    """Testa listagem de usuários vazia."""
    with patch.object(
        UserService, "list_profiles", new_callable=AsyncMock
    ) as mock_list_profiles:
        mock_list_profiles.return_value = []
        response = client.get("/api/users/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0 