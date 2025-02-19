from fastapi.testclient import TestClient
from src.main import app, todos

client = TestClient(app)

def setup_function():
    todos.clear()

def test_read_todos():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    response = client.post("/", json={"id": 1, "name": "Buy groceries", "completed": False})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Buy groceries", "completed": False}
    assert len(todos) == 1

def test_read_todo():
    client.post("/", json={"id": 1, "name": "Buy groceries", "completed": False})
    response = client.get("/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Buy groceries", "completed": False}

def test_update_todo():
    client.post("/", json={"id": 1, "name": "Buy groceries", "completed": False})
    response = client.put("/1", json={"id": 1, "name": "Buy vegetables", "completed": True})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Buy vegetables", "completed": True}

def test_delete_todo():
    client.post("/", json={"id": 1, "name": "Buy groceries", "completed": False})
    response = client.delete("/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Buy groceries", "completed": False}
    assert len(todos) == 0