"""Tests for health detection and insurance verification routes."""

import io

from PIL import Image, ImageDraw


def _test_image_bytes() -> io.BytesIO:
    img = Image.new("RGB", (256, 256), "black")
    draw = ImageDraw.Draw(img)
    draw.rectangle((70, 80, 190, 190), fill="white")
    bio = io.BytesIO()
    img.save(bio, format="JPEG")
    bio.seek(0)
    return bio


def test_health_detect_endpoint(client, auth_headers):
    image = _test_image_bytes()
    res = client.post(
        "/api/health/detect?cattle_id=CTL-001",
        headers=auth_headers,
        data={"image": (image, "health_probe.jpg", "image/jpeg")},
    )
    assert res.status_code == 200
    payload = res.get_json()
    assert "count" in payload
    assert "issues" in payload


def test_insurance_verify_endpoint(client, auth_headers):
    # cl1 exists in in-memory store
    res = client.post("/api/insurance/claims/cl1/verify", headers=auth_headers)
    assert res.status_code == 200
    payload = res.get_json()
    assert "fraud_score" in payload
    assert "risk_level" in payload
    assert "recommendation" in payload
