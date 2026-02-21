from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

class MockThought:
    def __init__(self, id=1):
        self.id = id

    def dict(self):
        return {
            "id": self.id,
            "persona_id": 1,
            "content": "Test thought",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }

mock_thought = MockThought()

@patch("backend.routers.thought_routes.Queue")
@patch("backend.routers.thought_routes.ThoughtService.create_thought")
def test_create_thought(mock_create, mock_queue):
    mock_create.return_value = mock_thought
    mock_q_instance = MagicMock()
    mock_queue.return_value = mock_q_instance
    
    response = client.post("/thoughts/", json={"persona_id": 1, "content": "Test thought"})
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert mock_q_instance.enqueue.called

@patch("backend.routers.thought_routes.ThoughtService.list_thoughts")
def test_list_thoughts(mock_list):
    mock_list.return_value = {"total": 1, "items": [mock_thought]}
    response = client.get("/thoughts/?persona_id=1")
    assert response.status_code == 200
    assert len(response.json()["items"]) == 1

@patch("backend.routers.thought_routes.ThoughtService.update_thought")
def test_update_thought(mock_update):
    mock_update.return_value = mock_thought
    response = client.put("/thoughts/1", json={"status": "completed"})
    assert response.status_code == 200

@patch("backend.routers.thought_routes.ThoughtService.delete_thought")
def test_delete_thought(mock_delete):
    mock_delete.return_value = True
    response = client.delete("/thoughts/1")
    assert response.status_code == 200

@patch("backend.routers.thought_routes.ThoughtService.get_thought")
def test_get_thought(mock_get):
    mock_get.return_value = mock_thought
    response = client.get("/thoughts/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("backend.routers.thought_routes.ThoughtService.link_thoughts")
def test_link_thought(mock_link):
    mock_link.return_value = True
    response = client.post("/thoughts/1/links", json={"target_id": 2})
    assert response.status_code == 200
