from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

@patch("backend.routers.processor_routes.Queue")
def test_generate_thoughts(mock_queue):
    mock_q_instance = MagicMock()
    mock_queue.return_value = mock_q_instance
    
    response = client.post("/generate-thoughts/", json={"urls": ["http://example.com"], "persona_id": 1})
    assert response.status_code == 200
    mock_q_instance.enqueue.assert_called_once()

@patch("backend.routers.processor_routes.Queue")
def test_generate_essay(mock_queue):
    mock_q_instance = MagicMock()
    mock_queue.return_value = mock_q_instance
    mock_job = MagicMock()
    mock_job.id = "test_job_id"
    mock_q_instance.enqueue.return_value = mock_job
    
    response = client.post("/essay/generate", json={"starting_text": "Test essay", "persona_id": 1})
    assert response.status_code == 200
    assert response.json() == {"job_id": "test_job_id"}

@patch("backend.routers.processor_routes.Queue")
def test_get_essay_status(mock_queue):
    mock_q_instance = MagicMock()
    mock_queue.return_value = mock_q_instance
    mock_job = MagicMock()
    mock_job.id = "test_job_id"
    mock_job.get_status.return_value = "finished"
    mock_job.result = "Essay text result"
    mock_job.exc_info = None
    mock_q_instance.fetch_job.return_value = mock_job
    
    response = client.get("/essay/status/test_job_id")
    assert response.status_code == 200
    assert response.json() == {
        "job_id": "test_job_id",
        "status": "finished",
        "result": "Essay text result",
        "error": None
    }
