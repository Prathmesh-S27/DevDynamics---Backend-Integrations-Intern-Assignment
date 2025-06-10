from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.services.event_service import EventService

app = FastAPI()

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
    assert response.content == b""