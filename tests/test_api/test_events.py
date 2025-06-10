from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/api/v1/events/", json={"name": "Test Event", "date": "2023-10-01"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Event"

def test_get_event():
    response = client.get("/api/v1/events/1")
    assert response.status_code == 200
    assert "name" in response.json()

def test_update_event():
    response = client.put("/api/v1/events/1", json={"name": "Updated Event"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Event"

def test_delete_event():
    response = client.delete("/api/v1/events/1")
    assert response.status_code == 204

def test_get_nonexistent_event():
    response = client.get("/api/v1/events/999")
    assert response.status_code == 404