import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from server.services.note_service import NoteService
from server.models.note import Note, NoteCreate
from server.models.user import UserProfile


@pytest.mark.asyncio
async def test_create_note_success(
    client: TestClient,
    test_user: UserProfile,
    test_note: Note,
    test_note_create: NoteCreate,
) -> None:
    """Testa criação de nota com sucesso."""
    with patch.object(
        NoteService, "create_note", new_callable=AsyncMock
    ) as mock_create_note:
        mock_create_note.return_value = test_note
        response = client.post(
            "/api/notes/",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=test_note_create.model_dump(),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == test_note.title
        assert data["content"] == test_note.content


@pytest.mark.asyncio
async def test_create_note_failure(
    client: TestClient, test_user: UserProfile, test_note_create: NoteCreate
) -> None:
    """Testa falha na criação de nota."""
    with patch.object(
        NoteService, "create_note", new_callable=AsyncMock
    ) as mock_create_note:
        mock_create_note.return_value = None
        response = client.post(
            "/api/notes/",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=test_note_create.model_dump(),
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_note_success(
    client: TestClient, test_user: UserProfile, test_note: Note
) -> None:
    """Testa busca de nota com sucesso."""
    with patch.object(NoteService, "get_note", new_callable=AsyncMock) as mock_get_note:
        mock_get_note.return_value = test_note
        response = client.get(
            f"/api/notes/{test_note.id}",
            headers={"Authorization": f"Bearer {test_user.id}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_note.id)
        assert data["title"] == test_note.title


@pytest.mark.asyncio
async def test_get_note_not_found(
    client: TestClient, test_user: UserProfile, test_note: Note
) -> None:
    """Testa busca de nota não encontrada."""
    with patch.object(NoteService, "get_note", new_callable=AsyncMock) as mock_get_note:
        mock_get_note.return_value = None
        response = client.get(
            f"/api/notes/{test_note.id}",
            headers={"Authorization": f"Bearer {test_user.id}"},
        )
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_notes_success(
    client: TestClient, test_user: UserProfile, test_note: Note
) -> None:
    """Testa listagem de notas com sucesso."""
    with patch.object(
        NoteService, "list_notes", new_callable=AsyncMock
    ) as mock_list_notes:
        mock_list_notes.return_value = [test_note]
        response = client.get(
            "/api/notes/", headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == str(test_note.id)


@pytest.mark.asyncio
async def test_update_note_success(
    client: TestClient, test_user: UserProfile, test_note: Note
) -> None:
    """Testa atualização de nota com sucesso."""
    update_data = {"title": "Updated Title"}
    with patch.object(
        NoteService, "update_note", new_callable=AsyncMock
    ) as mock_update_note:
        updated_note = test_note.model_copy(update=update_data)
        mock_update_note.return_value = updated_note
        response = client.put(
            f"/api/notes/{test_note.id}",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=update_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_note_success(
    client: TestClient, test_user: UserProfile, test_note: Note
) -> None:
    """Testa deleção de nota com sucesso."""
    with patch.object(
        NoteService, "delete_note", new_callable=AsyncMock
    ) as mock_delete_note:
        mock_delete_note.return_value = True
        response = client.delete(
            f"/api/notes/{test_note.id}",
            headers={"Authorization": f"Bearer {test_user.id}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Nota deletada com sucesso"
