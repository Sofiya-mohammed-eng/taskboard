import os

import pytest
from fastapi.testclient import TestClient

from main import app

needs_db = pytest.mark.skipif(
    "DB_HOST" not in os.environ, reason="no database configured"
)


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_empty_title_is_rejected():
    client = TestClient(app)
    assert client.post("/tasks", json={"title": ""}).status_code == 422


def test_missing_title_is_rejected():
    client = TestClient(app)
    assert client.post("/tasks", json={}).status_code == 422


def test_too_long_title_is_rejected():
    client = TestClient(app)
    response = client.post("/tasks", json={"title": "x" * 201})
    assert response.status_code == 422


@needs_db
def test_create_and_list_task():
    with TestClient(app) as client:
        created = client.post("/tasks", json={"title": "pytest task"})
        assert created.status_code == 201
        task = created.json()
        assert task["title"] == "pytest task"
        assert task["done"] is False

        tasks = client.get("/tasks").json()
        assert any(t["id"] == task["id"] for t in tasks)
