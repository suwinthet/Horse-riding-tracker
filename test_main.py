import pytest
from fastapi.testclient import TestClient
import sqlite3
import os
from main import app
from database import get_db

TEST_DB = "test_app.db"

def get_test_db():
    conn = sqlite3.connect(TEST_DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()

@pytest.fixture(autouse=True)
def setup_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    conn = sqlite3.connect(TEST_DB)
    with open("DB_commands.sql", "r") as f:
        conn.executescript(f.read())
    
    # Insert some dummy data for foreign keys
    conn.execute("INSERT INTO horses (name, discipline, daily_limit) VALUES ('Spirit', 'Jumping', 2)")
    conn.execute("INSERT INTO trainers (name, surname, specialization) VALUES ('John', 'Doe', 'Jumping')")
    conn.execute("INSERT INTO training_types (discipline, training_mode) VALUES ('Jumping', 'individual')")
    conn.commit()
    conn.close()
    
    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides.clear()

client = TestClient(app)

def test_register():
    response = client.post("/api/users", json={
        "name": "Alice",
        "surname": "Smith",
        "email": "alice@example.com",
        "password": "password123"
    })
    assert response.status_code == 201

def test_login():
    client.post("/api/users", json={
        "name": "Alice",
        "surname": "Smith",
        "email": "alice@example.com",
        "password": "password123"
    })
    response = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

@pytest.fixture
def auth_headers():
    client.post("/api/users", json={
        "name": "Bob",
        "surname": "Brown",
        "email": "bob@example.com",
        "password": "password123"
    })
    res = client.post("/api/auth/login", json={
        "email": "bob@example.com",
        "password": "password123"
    })
    token = res.json()["token"]
    return {"Authorization": f"Bearer {token}"}

def test_get_horses(auth_headers):
    response = client.get("/api/horses", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_trainers(auth_headers):
    response = client.get("/api/trainers", headers=auth_headers)
    assert response.status_code == 200

def test_get_training_types(auth_headers):
    response = client.get("/api/training-types", headers=auth_headers)
    assert response.status_code == 200

def test_create_training(auth_headers):
    response = client.post("/api/trainings", json={
        "horse_id": 1,
        "trainer_id": 1,
        "training_type_id": 1,
        "date": "2026-06-02T10:00:00Z"
    }, headers=auth_headers)
    assert response.status_code == 201

def test_get_trainings(auth_headers):
    client.post("/api/trainings", json={
        "horse_id": 1,
        "trainer_id": 1,
        "training_type_id": 1,
        "date": "2026-06-02T10:00:00Z"
    }, headers=auth_headers)
    
    response = client.get("/api/trainings", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_training(auth_headers):
    client.post("/api/trainings", json={
        "horse_id": 1,
        "trainer_id": 1,
        "training_type_id": 1,
        "date": "2026-06-02T10:00:00Z"
    }, headers=auth_headers)
    
    response = client.put("/api/trainings/1", json={
        "status": "completed"
    }, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "completed"

def test_join_training(auth_headers):
    client.post("/api/trainings", json={
        "horse_id": 1,
        "trainer_id": 1,
        "training_type_id": 1,
        "date": "2026-06-02T10:00:00Z"
    }, headers=auth_headers)
    
    response = client.post("/api/trainings/1/join", json={}, headers=auth_headers)
    assert response.status_code == 201

def test_get_participants(auth_headers):
    client.post("/api/trainings", json={
        "horse_id": 1,
        "trainer_id": 1,
        "training_type_id": 1,
        "date": "2026-06-02T10:00:00Z"
    }, headers=auth_headers)
    client.post("/api/trainings/1/join", json={}, headers=auth_headers)
    
    response = client.get("/api/trainings/1/participants", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_delete_training(auth_headers):
    client.post("/api/trainings", json={
        "horse_id": 1,
        "trainer_id": 1,
        "training_type_id": 1,
        "date": "2026-06-02T10:00:00Z"
    }, headers=auth_headers)
    
    response = client.delete("/api/trainings/1", headers=auth_headers)
    assert response.status_code == 204
    
    res2 = client.get("/api/trainings", headers=auth_headers)
    assert len(res2.json()) == 0

def test_invalid_input():
    response = client.post("/api/users", json={
        "name": "Bad",
        "surname": "User",
        "email": "invalid-email",
        "password": "123"
    })
    assert response.status_code == 422
