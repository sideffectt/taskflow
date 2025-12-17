from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get('/')
    
    assert response.status_code == 200
    assert response.json() == {'message': 'TaskFlow API is running'}
    
def test_create_task():
    task_data = {
        'title': 'Test Task',
        'description': 'This is tesk',
        'priority': 3
    }
    
    response = client.post('/task', json=task_data)
    
    assert response.status_code == 201
    
    data = response.json()
    assert data['title'] == 'Test Task'
    assert data['description'] == 'This is test'
    assert data['priority'] == 3
    assert data['completed'] == False
    assert 'id' in data
    assert 'created_at' in data
    
def get_all_tasks():
    