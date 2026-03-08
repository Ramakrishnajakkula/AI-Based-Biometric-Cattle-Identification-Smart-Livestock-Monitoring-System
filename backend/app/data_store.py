"""
Hardcoded In-Memory Data Store
Author: Akash

All sensor, cattle, alert, and claim data — no MongoDB/MQTT needed.
"""

import random
import math
from datetime import datetime, timezone, timedelta
import copy

# ===================== USERS =====================
USERS = [
    {
        "_id": "u1",
        "name": "Admin",
        "email": "admin@cattle.com",
        "password": "$2b$12$LJ3m4ys5Rn0Z9KqKx1qXXO8JGqkVZQF3Z8VU5VJy8.s6QK1gDOVRe",  # password: admin123
        "role": "admin",
        "created_at": "2026-01-15T10:00:00Z"
    },
    {
        "_id": "u2",
        "name": "Rajesh Kumar",
        "email": "rajesh@cattle.com",
        "password": "$2b$12$LJ3m4ys5Rn0Z9KqKx1qXXO8JGqkVZQF3Z8VU5VJy8.s6QK1gDOVRe",
        "role": "farmer",
        "created_at": "2026-01-20T10:00:00Z"
    },
]

# ===================== CATTLE =====================
CATTLE = [
    {
        "_id": "c1",
        "tag_id": "CTL-001",
        "name": "Lakshmi",
        "breed": "Gir",
        "age_years": 4,
        "weight_kg": 350,
        "owner_id": "u2",
        "farm_id": "FARM-01",
        "health_status": "healthy",
        "image_url": None,
        "created_at": "2026-01-20T10:00:00Z",
        "updated_at": "2026-03-01T10:00:00Z"
    },
    {
        "_id": "c2",
        "tag_id": "CTL-002",
        "name": "Ganga",
        "breed": "Sahiwal",
        "age_years": 3,
        "weight_kg": 320,
        "owner_id": "u2",
        "farm_id": "FARM-01",
        "health_status": "healthy",
        "image_url": None,
        "created_at": "2026-01-22T10:00:00Z",
        "updated_at": "2026-03-01T10:00:00Z"
    },
    {
        "_id": "c3",
        "tag_id": "CTL-003",
        "name": "Nandi",
        "breed": "Red Sindhi",
        "age_years": 5,
        "weight_kg": 400,
        "owner_id": "u2",
        "farm_id": "FARM-01",
        "health_status": "sick",
        "image_url": None,
        "created_at": "2026-01-25T10:00:00Z",
        "updated_at": "2026-03-05T10:00:00Z"
    },
    {
        "_id": "c4",
        "tag_id": "CTL-004",
        "name": "Kamadhenu",
        "breed": "Tharparkar",
        "age_years": 2,
        "weight_kg": 280,
        "owner_id": "u2",
        "farm_id": "FARM-02",
        "health_status": "healthy",
        "image_url": None,
        "created_at": "2026-02-01T10:00:00Z",
        "updated_at": "2026-03-01T10:00:00Z"
    },
    {
        "_id": "c5",
        "tag_id": "CTL-005",
        "name": "Surabhi",
        "breed": "Ongole",
        "age_years": 6,
        "weight_kg": 450,
        "owner_id": "u2",
        "farm_id": "FARM-02",
        "health_status": "healthy",
        "image_url": None,
        "created_at": "2026-02-05T10:00:00Z",
        "updated_at": "2026-03-01T10:00:00Z"
    },
]

# ===================== HEALTH ALERTS =====================
HEALTH_ALERTS = [
    {
        "_id": "a1",
        "cattle_id": "CTL-003",
        "cattle_name": "Nandi",
        "type": "fever",
        "severity": "high",
        "message": "Temperature 40.2°C — exceeds safe threshold of 39.5°C",
        "status": "active",
        "source": "sensor",
        "created_at": "2026-03-07T14:30:00Z"
    },
    {
        "_id": "a2",
        "cattle_id": "CTL-001",
        "cattle_name": "Lakshmi",
        "type": "elevated_heartrate",
        "severity": "medium",
        "message": "Heart rate at 85 bpm — above normal range (40-80 bpm)",
        "status": "active",
        "source": "sensor",
        "created_at": "2026-03-07T10:15:00Z"
    },
    {
        "_id": "a3",
        "cattle_id": "CTL-005",
        "cattle_name": "Surabhi",
        "type": "low_activity",
        "severity": "low",
        "message": "Reduced movement detected for last 6 hours",
        "status": "active",
        "source": "sensor",
        "created_at": "2026-03-06T22:00:00Z"
    },
    {
        "_id": "a4",
        "cattle_id": "CTL-002",
        "cattle_name": "Ganga",
        "type": "eye_redness",
        "severity": "medium",
        "message": "Visual inspection flagged possible eye infection",
        "status": "resolved",
        "source": "vision",
        "created_at": "2026-03-04T09:00:00Z",
        "resolved_at": "2026-03-05T11:00:00Z"
    },
    {
        "_id": "a5",
        "cattle_id": "CTL-003",
        "cattle_name": "Nandi",
        "type": "skin_lesion",
        "severity": "high",
        "message": "Skin lesion detected on front-left leg area",
        "status": "active",
        "source": "vision",
        "created_at": "2026-03-05T16:45:00Z"
    },
]

# ===================== INSURANCE CLAIMS =====================
INSURANCE_CLAIMS = [
    {
        "_id": "cl1",
        "cattle_id": "CTL-003",
        "cattle_name": "Nandi",
        "owner_id": "u2",
        "claim_type": "illness",
        "description": "Cattle showing fever symptoms and skin lesion, requires medical treatment.",
        "amount": 15000,
        "status": "pending",
        "fraud_score": None,
        "submitted_by": "u2",
        "created_at": "2026-03-06T10:00:00Z",
        "updated_at": "2026-03-06T10:00:00Z"
    },
    {
        "_id": "cl2",
        "cattle_id": "CTL-004",
        "cattle_name": "Kamadhenu",
        "owner_id": "u2",
        "claim_type": "theft",
        "description": "Cattle went missing from farmland on March 2.",
        "amount": 45000,
        "status": "under_review",
        "fraud_score": 35,
        "submitted_by": "u2",
        "created_at": "2026-03-03T08:00:00Z",
        "updated_at": "2026-03-04T15:00:00Z"
    },
    {
        "_id": "cl3",
        "cattle_id": "CTL-002",
        "cattle_name": "Ganga",
        "owner_id": "u2",
        "claim_type": "illness",
        "description": "Eye infection treatment expenses.",
        "amount": 5000,
        "status": "approved",
        "fraud_score": 10,
        "submitted_by": "u2",
        "created_at": "2026-02-20T12:00:00Z",
        "updated_at": "2026-02-25T09:00:00Z"
    },
]

# ===================== GPS POSITIONS =====================
CATTLE_GPS = {
    "CTL-001": {"lat": 17.3850, "lng": 78.4867, "name": "Lakshmi"},
    "CTL-002": {"lat": 17.3854, "lng": 78.4872, "name": "Ganga"},
    "CTL-003": {"lat": 17.3847, "lng": 78.4863, "name": "Nandi"},
    "CTL-004": {"lat": 17.3860, "lng": 78.4880, "name": "Kamadhenu"},
    "CTL-005": {"lat": 17.3843, "lng": 78.4858, "name": "Surabhi"},
}


# ===================== SENSOR GENERATORS =====================
def _generate_sensor_history(cattle_id, sensor_type, hours=24, points=48):
    """Generate realistic fake sensor history."""
    now = datetime.now(timezone.utc)
    data = []
    base_temp = {"CTL-001": 38.5, "CTL-002": 38.3, "CTL-003": 39.8, "CTL-004": 38.4, "CTL-005": 38.6}
    base_hr = {"CTL-001": 65, "CTL-002": 60, "CTL-003": 72, "CTL-004": 62, "CTL-005": 68}

    for i in range(points):
        t = now - timedelta(hours=hours * (points - i) / points)
        hour = t.hour
        ts = t.isoformat()

        if sensor_type == "temperature":
            base = base_temp.get(cattle_id, 38.5)
            val = round(base + 0.3 * math.sin(2 * math.pi * hour / 24) + random.gauss(0, 0.15), 1)
            data.append({"timestamp": ts, "data": {"value": val, "unit": "celsius"}})
        elif sensor_type == "heartrate":
            base = base_hr.get(cattle_id, 65)
            val = max(38, base + random.randint(-6, 6))
            data.append({"timestamp": ts, "data": {"bpm": val, "spo2": random.randint(95, 99)}})
        elif sensor_type == "activity":
            data.append({"timestamp": ts, "data": {
                "activity_level": random.choice(["resting", "walking", "grazing"]),
                "steps": random.randint(0, 120)
            }})
    return data


def get_latest_sensors(cattle_id):
    """Get the most recent sensor readings for a cattle."""
    now = datetime.now(timezone.utc).isoformat()
    base_temp = {"CTL-001": 38.5, "CTL-002": 38.3, "CTL-003": 40.2, "CTL-004": 38.4, "CTL-005": 38.6}
    base_hr = {"CTL-001": 65, "CTL-002": 60, "CTL-003": 72, "CTL-004": 62, "CTL-005": 68}

    temp = round(base_temp.get(cattle_id, 38.5) + random.gauss(0, 0.1), 1)
    hr = base_hr.get(cattle_id, 65) + random.randint(-3, 3)
    gps = CATTLE_GPS.get(cattle_id, {"lat": 17.385, "lng": 78.487})

    return {
        "temperature": {"data": {"value": temp, "unit": "celsius"}, "timestamp": now},
        "heartrate": {"data": {"bpm": hr, "spo2": random.randint(96, 99)}, "timestamp": now},
        "gps": {"data": {"lat": gps["lat"] + random.gauss(0, 0.0001), "lng": gps["lng"] + random.gauss(0, 0.0001)}, "timestamp": now},
        "activity": {"data": {"activity_level": random.choice(["resting", "walking", "grazing"]), "steps": random.randint(10, 80)}, "timestamp": now},
    }
