from fastapi.testclient import TestClient
from backend.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)

mock_persona = {
    "id": 1,
    "name": "Test Persona",
    "age": 30,
    "gender": "male",
    "additional_info": {},
    "source": "manual",
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
}

@patch("backend.routers.persona_routes.PersonaService.list_personas")
def test_list_personas(mock_list):
    mock_list.return_value = [mock_persona]
    response = client.get("/personas/")
    assert response.status_code == 200
    assert len(response.json()) == 1

@patch("backend.routers.persona_routes.PersonaService.create_persona")
def test_create_persona(mock_create):
    mock_create.return_value = mock_persona
    response = client.post("/personas/", json={"name": "Test Persona", "age": 30, "gender": "male"})
    assert response.status_code == 200
    assert response.json()["id"] == 1

@patch("backend.routers.persona_routes.PersonaService.update_persona")
def test_update_persona(mock_update):
    mock_update.return_value = mock_persona
    response = client.put("/personas/1", json={"age": 31})
    assert response.status_code == 200

@patch("backend.routers.persona_routes.PersonaService.delete_persona")
def test_delete_persona(mock_delete):
    mock_delete.return_value = True
    response = client.delete("/personas/1")
    assert response.status_code == 200

@patch("backend.routers.persona_routes.PersonaService.regenerate_persona")
def test_regenerate_persona(mock_regen):
    mock_regen.return_value = mock_persona
    response = client.post("/personas/1/regenerate")
    assert response.status_code == 200

@patch("backend.routers.persona_routes.PersonaService.derive_persona")
def test_derive_persona(mock_derive):
    mock_derive.return_value = mock_persona
    response = client.post("/personas/derive", json={"source_persona_id": 1, "name_adjective": "Smart", "percentage": 50})
    assert response.status_code == 200

def test_generate_persona_name():
    response = client.post("/personas/generate-name")
    assert response.status_code == 200
    assert "name" in response.json()

def test_enrich_persona_from_movie_characters():
    with patch("redis.Redis") as mock_redis:
        with patch("rq.Queue") as mock_queue:
            mock_q = MagicMock()
            mock_queue.return_value = mock_q
            mock_job = MagicMock()
            mock_job.id = "test-job-id"
            mock_q.enqueue.return_value = mock_job
            
            response = client.post("/personas/1/enrich-from-movie-characters", json={"character_ids": ["char1", "char2"]})
            assert response.status_code == 202
            assert response.json()["job_id"] == "test-job-id"
            assert "Enrichment task started" in response.json()["message"]
