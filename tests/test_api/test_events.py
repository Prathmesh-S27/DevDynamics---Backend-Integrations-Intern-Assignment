from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_event():
    event_data = {
        "title": "Test Event", 
        "description": "A test event",
        "start_time": "2024-07-15T18:00:00",
        "end_time": "2024-07-15T22:00:00",
        "location": "Test City",
        "event_type": "outdoor"
    }
    response = client.post("/api/v1/events/", json=event_data)
    assert response.status_code == 201
    assert response.json()["title"] == "Test Event"

def test_get_events():
    response = client.get("/api/v1/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_nonexistent_event():
    response = client.get("/api/v1/events/999")
    assert response.status_code == 404

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()