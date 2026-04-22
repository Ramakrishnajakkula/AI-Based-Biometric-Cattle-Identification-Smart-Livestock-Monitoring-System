"""
Tests for Cattle CRUD Routes
Author: Akash
"""

import pytest
import uuid


def test_list_cattle(client, auth_headers):
    """Test listing all cattle."""
    res = client.get("/api/cattle/", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert "cattle" in data
    assert data["total"] >= 1


def test_register_cattle(client, auth_headers):
    """Test cattle registration."""
    tag = f"CTL-T-{uuid.uuid4().hex[:6].upper()}"
    res = client.post(
        "/api/cattle/",
        headers=auth_headers,
        json={
            "tag_id": tag,
            "name": "UnitTest Cow",
            "breed": "Gir",
            "age_years": 2,
            "weight_kg": 250,
            "owner_id": "u2",
            "farm_id": "FARM-TEST",
        },
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["tag_id"] == tag
    assert data["breed"] == "Gir"


def test_get_cattle_by_id(client, auth_headers):
    """Test retrieving single cattle."""
    res = client.get("/api/cattle/c1", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["_id"] == "c1"
    assert "tag_id" in data
