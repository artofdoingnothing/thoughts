import sys
import pytest
from unittest.mock import MagicMock

sys.modules["google"] = MagicMock()
sys.modules["google.genai"] = MagicMock()

import os
os.environ["GEMINI_API_KEY"] = "dummy_key"
from fastapi.testclient import TestClient
from backend.main import app
from libs.db_service import init_database, ThoughtService
sys.modules["redis"] = MagicMock()
from workers import tasks

client = TestClient(app)

def setup_module(module):
    init_database()

def test_delete_thought():
    # Create
    response = client.post("/thoughts/", json={"content": "Delete me"})
    assert response.status_code == 200
    thought_id = response.json()["id"]

    # Delete
    response = client.delete(f"/thoughts/{thought_id}")
    assert response.status_code == 200

    # Verify Gone
    response = client.get(f"/thoughts/{thought_id}")
    assert response.status_code == 404

def test_update_thought_success():
    # Create
    response = client.post("/thoughts/", json={"content": "Update me"})
    assert response.status_code == 200
    thought_id = response.json()["id"]

    # Update Status
    response = client.put(f"/thoughts/{thought_id}", json={"status": "archived"})
    assert response.status_code == 200
    assert response.json()["status"] == "archived"

    # Verify Persistence
    response = client.get(f"/thoughts/{thought_id}")
    assert response.json()["status"] == "archived"

def test_update_thought_restricted():
    # Create
    response = client.post("/thoughts/", json={"content": "No change"})
    assert response.status_code == 200
    thought_id = response.json()["id"]

    # Try Update Content
    response = client.put(f"/thoughts/{thought_id}", json={"content": "New Content"})
    assert response.status_code == 400

def test_worker_completion_status(monkeypatch):
    class MockProcessor:
        def analyze_cognitive_distortions(self, content):
            return ["Distortion1"]
        def analyze_sentiment(self, content):
            return ["Happy"]

    # We need to mock processor in thought_uc
    monkeypatch.setattr(tasks.thought_uc, "processor", MockProcessor())

    # Create thought
    thought = ThoughtService.create_thought("Worker Test")
    
    # Run worker task manually
    tasks.analyze_cognitive_distortions(thought.id)
    
    # Verify Status
    updated_thought = ThoughtService.get_thought(thought.id)
    assert updated_thought.status == "completed"
    assert any(t.name == "distortion1" for t in updated_thought.tags)
