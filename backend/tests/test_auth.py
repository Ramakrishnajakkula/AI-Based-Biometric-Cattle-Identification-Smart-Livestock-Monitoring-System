"""
Tests for Authentication Routes
Author: Akash
"""

import pytest
import uuid


def test_register(client):
    """Test user registration endpoint."""
    email = f"reg_{uuid.uuid4().hex[:8]}@cattle.com"
    res = client.post(
        "/api/auth/register",
        json={"name": "Reg User", "email": email, "password": "admin123", "role": "farmer"},
    )
    assert res.status_code == 201
    data = res.get_json()
    assert "token" in data
    assert data["user"]["email"] == email


def test_login(client):
    """Test login endpoint."""
    email = f"login_{uuid.uuid4().hex[:8]}@cattle.com"
    reg = client.post(
        "/api/auth/register",
        json={"name": "Login User", "email": email, "password": "admin123", "role": "farmer"},
    )
    assert reg.status_code == 201

    res = client.post(
        "/api/auth/login",
        json={"email": email, "password": "admin123"},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "token" in data
    assert data["user"]["email"] == email


def test_profile_requires_auth(client):
    """Test profile endpoint requires JWT."""
    res = client.get("/api/auth/profile")
    assert res.status_code in (401, 422)
