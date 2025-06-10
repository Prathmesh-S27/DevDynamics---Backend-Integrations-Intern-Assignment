from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_event():
    # Fixed: Use correct field names and endpoint structure
    event_data = {
        "title": "Test Event",  # Changed from "name" to "title"
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

def test_get_event():
    # First create an event, then get it
    event_data = {
        "title": "Test Event for Get",
        "description": "A test event", 
        "start_time": "2024-07-15T18:00:00",
        "end_time": "2024-07-15T22:00:00",
        "location": "Test City",
        "event_type": "outdoor"
    }
    create_response = client.post("/api/v1/events/", json=event_data)
    assert create_response.status_code == 201
    
    event_id = create_response.json()["id"]
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    assert "title" in response.json()

def test_update_event():
    # First create an event, then update it
    event_data = {
        "title": "Original Event",
        "description": "Original description",
        "start_time": "2024-07-15T18:00:00", 
        "end_time": "2024-07-15T22:00:00",
        "location": "Test City",
        "event_type": "outdoor"
    }
    create_response = client.post("/api/v1/events/", json=event_data)
    assert create_response.status_code == 201
    
    event_id = create_response.json()["id"]
    update_data = {
        "title": "Updated Event",
        "description": "Updated description",
        "start_time": "2024-07-15T18:00:00",
        "end_time": "2024-07-15T22:00:00", 
        "location": "Test City",
        "event_type": "outdoor"
    }
    response = client.put(f"/api/v1/events/{event_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Event"

def test_delete_event():
    # First create an event, then delete it
    event_data = {
        "title": "Event to Delete",
        "description": "Will be deleted",
        "start_time": "2024-07-15T18:00:00",
        "end_time": "2024-07-15T22:00:00",
        "location": "Test City", 
        "event_type": "outdoor"
    }
    create_response = client.post("/api/v1/events/", json=event_data)
    assert create_response.status_code == 201
    
    event_id = create_response.json()["id"]
    response = client.delete(f"/api/v1/events/{event_id}")
    assert response.status_code == 204