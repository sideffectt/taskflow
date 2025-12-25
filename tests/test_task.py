from fastapi.testclient import TestClient

from main import app
from app.config import db
import random
import string

db.connect()

client = TestClient(app)


def get_random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def get_token():
    username = f"testuser_{get_random_string()}"
    email = f"{username}@test.com"
    password = "test123"
    
    client.post("/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    
    response = client.post("/auth/login", json={
        "username": username,
        "password": password
    })
    return response.json()["access_token"]



def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "TaskFlow API is running"}


def test_register():
    response = client.post("/auth/register", json={
        "username": "newuser123",
        "email": "newuser123@test.com",
        "password": "123456"
    })
    assert response.status_code in [201, 400]


def test_login():
    username = f"logintest_{get_random_string()}"
    client.post("/auth/register", json={
        "username": username,
        "email": f"{username}@test.com",
        "password": "test123"
    })
    
    response = client.post("/auth/login", json={
        "username": username,
        "password": "test123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_tasks_without_token():
    response = client.get("/tasks")
    assert response.status_code == 401


def test_create_task():
    token = get_token()
    response = client.post(
        "/tasks",
        json={"title": "Test Task", "description": "This is a test", "priority": 3},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] == False


def test_get_all_tasks():
    token = get_token()
    response = client.get(
        "/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_by_id():
    token = get_token()
    create_response = client.post(
        "/tasks",
        json={"title": "Find Me", "priority": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Find Me"


def test_get_task_not_found():
    token = get_token()
    response = client.get(
        "/tasks/000000000000000000000000",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_update_task():
    token = get_token()
    create_response = client.post(
        "/tasks",
        json={"title": "Update Me", "priority": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    response = client.put(
        f"/tasks/{task_id}",
        json={"completed": True, "priority": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["completed"] == True


def test_delete_task():
    token = get_token()
    create_response = client.post(
        "/tasks",
        json={"title": "Delete Me", "priority": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]
    
    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 204