import sys
import pytest
from unittest.mock import MagicMock

# Mock google module before importing workers
sys.modules["google"] = MagicMock()
sys.modules["google.genai"] = MagicMock()

import os
os.environ["GEMINI_API_KEY"] = "dummy_key"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from fastapi.testclient import TestClient
from backend.main import app
from libs.db_service import init_database, ThoughtService
# Mock redis to avoid connection issues if needed, strictly speaking redis is used in main.py
sys.modules["redis"] = MagicMock()
from workers import tasks
import os

client = TestClient(app)

# Ensure we use a test DB or similar if possible, but for now we might be running against local dev DB.
# CAUTION: This might affect local data. Ideally we use a separate test DB.
# Given the environment, I'll proceed but ideally we'd mock or segregate.

def setup_module(module):
    init_database()

def test_delete_thought():
    # Create
    response = client.post("/thoughts/", json={"title": "To Delete", "content": "Delete me"})
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
    response = client.post("/thoughts/", json={"title": "To Update", "content": "Update me"})
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
    response = client.post("/thoughts/", json={"title": "Restricted", "content": "No change"})
    assert response.status_code == 200
    thought_id = response.json()["id"]

    # Try Update Title
    response = client.put(f"/thoughts/{thought_id}", json={"title": "New Title"})
    assert response.status_code == 400
    assert "Cannot update title or content" in response.json()["detail"]

    # Try Update Content
    response = client.put(f"/thoughts/{thought_id}", json={"content": "New Content"})
    assert response.status_code == 400

def test_worker_completion_status(monkeypatch):
    # Mock processor to avoid calling actual LLM
    class MockProcessor:
        def analyze_cognitive_distortions(self, content):
            return ["Distortion1"]
        def analyze_sentiment(self, content):
            return ["Happy"]

    monkeypatch.setattr(tasks, "processor", MockProcessor())

    # Create thought
    thought = ThoughtService.create_thought("Worker Test", "Testing worker")
    
    # Run worker task manually
    tasks.analyze_cognitive_distortions(thought.id)
    
    # Verify Status
    updated_thought = ThoughtService.get_thought(thought.id)
    assert updated_thought.status == "completed"
    assert any(t.name == "distortion1" for t in updated_thought.tags)
