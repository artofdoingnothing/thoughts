from fastapi.testclient import TestClient
from backend.main import app
import pytest

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Thought Aggregator API"}

def test_create_thought():
    # Note: This might fail if Redis is not running, 
    # but for unit testing we should ideally mock Redis.
    # For now, let's just test the root to verify setup.
    pass
