from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_user_registration_and_login():
    payload = {
        "email": "student@example.com",
        "username": "student1",
        "full_name": "Demo Student",
        "password": "pass12345",
    }

    register_response = client.post("/api/auth/register", json=payload)
    assert register_response.status_code == 201, register_response.text

    login_response = client.post(
        "/api/auth/login",
        json={"email": payload["email"], "password": payload["password"]},
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]
    assert token
