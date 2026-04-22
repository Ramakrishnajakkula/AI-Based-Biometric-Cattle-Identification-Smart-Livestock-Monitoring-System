import uuid

import pytest

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def auth_headers(client):
    email = f"test_{uuid.uuid4().hex[:8]}@cattle.com"
    password = "admin123"

    reg = client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": email, "password": password, "role": "farmer"},
    )
    assert reg.status_code == 201
    token = reg.get_json()["token"]
    return {"Authorization": f"Bearer {token}"}
