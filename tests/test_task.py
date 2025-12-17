from fastapi.testclient import TestClient

from main import app
from app.config import db

db.connect()

client = TestClient(app)

def test_root():
    response = client.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"message": "TaskFlow API is running"}

def test_create_task():
    task_data = {
        "title": "Test Task",
        "description": "This is a test",
        "priority": 3
    }
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 201
    
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test"
    assert data["priority"] == 3
    assert data["completed"] == False
    assert "id" in data
    assert "created_at" in data


def test_get_all_tasks():
    response = client.get("/tasks")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_by_id():
    task_data = {"title": "Find Me", "priority": 1}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.get(f"/tasks/{task_id}")
    
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


def test_get_task_not_found():
    response = client.get("/tasks/000000000000000000000000")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_task():
    task_data = {"title": "Update Me", "priority": 1}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    update_data = {"completed": True, "priority": 5}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    
    assert response.status_code == 200
    assert response.json()["completed"] == True
    assert response.json()["priority"] == 5


def test_delete_task():
    task_data = {"title": "Delete Me", "priority": 1}
    create_response = client.post("/tasks", json=task_data)
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}")
    
    assert response.status_code == 204
    
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_create_task_invalid_data():
    task_data = {"priority": 3}
    
    response = client.post("/tasks", json=task_data)
    
    assert response.status_code == 422