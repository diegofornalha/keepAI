import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from server.services.ai_service import AIService
from server.models.conversation import Conversation, ConversationCreate
from server.models.user import UserProfile


@pytest.mark.asyncio
async def test_create_chat_success(
    client: TestClient,
    test_user: UserProfile,
    test_conversation: Conversation,
    test_conversation_create: ConversationCreate,
) -> None:
    """Testa criação de conversa com sucesso."""
    with patch.object(
        AIService, "create_conversation", new_callable=AsyncMock
    ) as mock_create_conversation:
        mock_create_conversation.return_value = test_conversation
        response = client.post(
            "/api/ai/chat",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=test_conversation_create.model_dump(),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == test_conversation.message
        assert data["response"] == test_conversation.response


@pytest.mark.asyncio
async def test_create_chat_failure(
    client: TestClient,
    test_user: UserProfile,
    test_conversation_create: ConversationCreate,
) -> None:
    """Testa falha na criação de conversa."""
    with patch.object(
        AIService, "create_conversation", new_callable=AsyncMock
    ) as mock_create_conversation:
        mock_create_conversation.return_value = None
        response = client.post(
            "/api/ai/chat",
            headers={"Authorization": f"Bearer {test_user.id}"},
            json=test_conversation_create.model_dump(),
        )
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_list_conversations_success(
    client: TestClient, test_user: UserProfile, test_conversation: Conversation
) -> None:
    """Testa listagem de conversas com sucesso."""
    with patch.object(
        AIService, "list_conversations", new_callable=AsyncMock
    ) as mock_list_conversations:
        mock_list_conversations.return_value = [test_conversation]
        response = client.get(
            "/api/ai/conversations", headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == str(test_conversation.id)
        assert data[0]["message"] == test_conversation.message


@pytest.mark.asyncio
async def test_list_conversations_empty(
    client: TestClient, test_user: UserProfile
) -> None:
    """Testa listagem de conversas vazia."""
    with patch.object(
        AIService, "list_conversations", new_callable=AsyncMock
    ) as mock_list_conversations:
        mock_list_conversations.return_value = []
        response = client.get(
            "/api/ai/conversations", headers={"Authorization": f"Bearer {test_user.id}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0


@pytest.mark.asyncio
async def test_get_conversation_success(
    client: TestClient, test_user: UserProfile, test_conversation: Conversation
) -> None:
    """Testa busca de conversa com sucesso."""
    with patch.object(
        AIService, "get_conversation", new_callable=AsyncMock
    ) as mock_get_conversation:
        mock_get_conversation.return_value = test_conversation
        response = client.get(
            f"/api/ai/conversations/{test_conversation.id}",
            headers={"Authorization": f"Bearer {test_user.id}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(test_conversation.id)
        assert data["message"] == test_conversation.message
        assert data["response"] == test_conversation.response


@pytest.mark.asyncio
async def test_get_conversation_not_found(
    client: TestClient, test_user: UserProfile, test_conversation: Conversation
) -> None:
    """Testa busca de conversa não encontrada."""
    with patch.object(
        AIService, "get_conversation", new_callable=AsyncMock
    ) as mock_get_conversation:
        mock_get_conversation.return_value = None
        response = client.get(
            f"/api/ai/conversations/{test_conversation.id}",
            headers={"Authorization": f"Bearer {test_user.id}"},
        )
        assert response.status_code == 404
