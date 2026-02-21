from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch, MagicMock
from libs.db_service import ConversationDomain

client = TestClient(app)

mock_conversation = {
    "id": 1,
    "title": "Test Convo",
    "context": "Context",
    "persona_ids": [1],
    "messages": [],
    "is_active": True,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
}

@patch("backend.routers.conversation_routes.ConversationService.create_conversation")
def test_create_conversation(mock_create):
    mock_create.return_value = mock_conversation
    response = client.post("/conversations/", json={"title": "Test Convo", "context": "Context", "persona_ids": [1]})
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("backend.routers.conversation_routes.ConversationService.list_conversations")
def test_list_conversations(mock_list):
    mock_list.return_value = [mock_conversation]
    response = client.get("/conversations/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@patch("backend.routers.conversation_routes.ConversationService.get_conversation")
def test_get_conversation(mock_get):
    mock_get.return_value = mock_conversation
    response = client.get("/conversations/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("backend.routers.conversation_routes.Queue")
@patch("backend.routers.conversation_routes.ConversationService.get_conversation")
def test_generate_message(mock_get, mock_queue):
    mock_get.return_value = mock_conversation
    mock_q_instance = MagicMock()
    mock_queue.return_value = mock_q_instance
    
    response = client.post("/conversations/1/generate", json={"persona_id": 1})
    assert response.status_code == 200
    mock_q_instance.enqueue.assert_called_once()

@patch("backend.routers.conversation_routes.Queue")
@patch("backend.routers.conversation_routes.ConversationService.get_conversation")
def test_generate_sequence(mock_get, mock_queue):
    mock_get.return_value = mock_conversation
    mock_q_instance = MagicMock()
    mock_queue.return_value = mock_q_instance
    
    response = client.post("/conversations/1/generate_sequence", json={"persona_ids": [1, 2]})
    assert response.status_code == 200
    mock_q_instance.enqueue.assert_called_once()

@patch("backend.routers.conversation_routes.ConversationService.add_persona_to_conversation")
def test_add_persona_to_conversation(mock_add):
    mock_add.return_value = True
    response = client.post("/conversations/1/personas", json={"persona_id": 2})
    assert response.status_code == 200

@patch("backend.routers.conversation_routes.ConversationService.end_conversation")
def test_end_conversation(mock_end):
    mock_end.return_value = True
    response = client.post("/conversations/1/end")
    assert response.status_code == 200
