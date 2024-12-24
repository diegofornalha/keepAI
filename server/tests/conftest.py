import pytest
from fastapi.testclient import TestClient
from uuid import UUID, uuid4

from server.run import app
from server.models.user import UserProfile
from server.models.note import Note, NoteCreate
from server.models.task import Task, TaskCreate, TaskStatus, TaskPriority
from server.models.conversation import Conversation, ConversationCreate

@pytest.fixture
def client():
    """Cliente de teste para a API."""
    return TestClient(app)

@pytest.fixture
def test_user():
    """Usuário de teste."""
    return UserProfile(
        id=uuid4(),
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    )

@pytest.fixture
def test_note():
    """Nota de teste."""
    return Note(
        id=uuid4(),
        user_id="test_user",
        title="Test Note",
        content="Test content",
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    )

@pytest.fixture
def test_note_create():
    """Dados para criar nota de teste."""
    return NoteCreate(
        title="New Test Note",
        content="New test content"
    )

@pytest.fixture
def test_task():
    """Tarefa de teste."""
    return Task(
        id=uuid4(),
        user_id="test_user",
        title="Test Task",
        description="Test description",
        status=TaskStatus.PENDING,
        priority=TaskPriority.MEDIUM,
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    )

@pytest.fixture
def test_task_create():
    """Dados para criar tarefa de teste."""
    return TaskCreate(
        title="New Test Task",
        description="New test description",
        priority=TaskPriority.HIGH
    )

@pytest.fixture
def test_conversation():
    """Conversa de teste."""
    return Conversation(
        id=uuid4(),
        user_id="test_user",
        message="Test message",
        response="Test response",
        created_at="2024-01-01T00:00:00Z",
        model_used="gemini-pro"
    )

@pytest.fixture
def test_conversation_create():
    """Dados para criar conversa de teste."""
    return ConversationCreate(
        message="New test message"
    ) 