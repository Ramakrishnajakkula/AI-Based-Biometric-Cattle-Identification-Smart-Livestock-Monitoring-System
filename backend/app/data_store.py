"""
In-Memory Data Store — Uses the actual cattle_master_dataset.csv
Loads real data from data/processed/cattle_master/cattle_master_dataset.csv
and serves cattle images from the ML training set.
Author: Akash
"""

from werkzeug.security import generate_password_hash
import random
import math
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]  # cap/


def _hash(pw: str) -> str:
    return generate_password_hash(pw)


_COMMON_PW = _hash("password123")
_ADMIN_PW = _hash("admin123")


import json

# ---------------------------------------------------------------------------
# Load the dataset
# ---------------------------------------------------------------------------
JSON_DATA_PATH = ROOT / "backend" / "data" / "cattle_dataset.json"

def _build_cattle():
    if JSON_DATA_PATH.exists():
        with open(JSON_DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Ensure images point to correct static folder if needed
            return data
    return []

CATTLE = _build_cattle()

# ---------------------------------------------------------------------------
# USERS — 1 admin + 5 farmers
# ---------------------------------------------------------------------------
# Extract unique farm owners from the dataset
_farm_owners = {}
for c in CATTLE:
    fid = c.get("farm_id")
    if fid and fid not in _farm_owners:
        # Try to extract the owner string, or generate a dummy one
        _farm_owners[fid] = {
            "name": f"Owner of {fid}",
            "farm_name": fid
        }

# Build user list
USERS = [
    {
        "_id": "u1",
        "name": "Admin Ramesh",
        "email": "admin@smartlivestock.in",
        "password": _ADMIN_PW,
        "role": "admin",
        "farm_id": None,
        "created_at": "2025-01-01T00:00:00Z",
    },
]

_farm_ids = list(_farm_owners.keys()) if _farm_owners else [f"FARM-0{i}" for i in range(1, 6)]
_farmer_emails = ["rajesh@farm.in", "priya@farm.in", "suresh@farm.in", "anita@farm.in", "venkat@farm.in"]

for i, fid in enumerate(_farm_ids[:5]):
    owner = _farm_owners.get(fid, {"name": f"Farmer {i+1}", "farm_name": fid})
    email = _farmer_emails[i] if i < len(_farmer_emails) else f"farmer{i}@farm.in"
    USERS.append({
        "_id": f"u{i+2}",
        "name": owner["name"],
        "email": email,
        "password": _COMMON_PW,
        "role": "farmer",
        "farm_id": fid,
        "created_at": f"2025-0{i+2}-{10+i*5}T08:30:00Z" if i < 3 else "2025-10-10T08:30:00Z",
    })

# Map farm_id → owner user _id
_farm_to_owner = {u["farm_id"]: u["_id"] for u in USERS if u["farm_id"]}

# ---------------------------------------------------------------------------
# FARMS
# ---------------------------------------------------------------------------
FARMS = []
for fid in _farm_ids[:5]:
    owner = _farm_owners.get(fid, {"farm_name": fid})
    lat = 17.385
    lng = 78.487
    for c in CATTLE:
        if c.get("farm_id") == fid and "gps" in c:
            lat = c["gps"].get("lat", lat)
            lng = c["gps"].get("lng", lng)
            break

    FARMS.append({
        "farm_id": fid,
        "name": owner.get("farm_name", fid),
        "lat": lat,
        "lng": lng,
    })


# ---------------------------------------------------------------------------
# Sensor history — generated on the fly per cattle
# ---------------------------------------------------------------------------
def generate_sensor_history(cattle_id, sensor_type="temperature", hours=24):
    """Generate realistic sensor time series for a given cattle."""
    random.seed(hash(cattle_id + sensor_type) % 2**31)
    now = datetime.now(timezone.utc)
    readings = []
    for h in range(hours * 2):
        ts = now - timedelta(minutes=30 * (hours * 2 - h))
        if sensor_type == "temperature":
            base = 38.5 + 0.5 * math.sin(h / 6.0)
            val = round(base + random.uniform(-0.4, 0.4), 1)
            readings.append({"timestamp": ts.isoformat(), "data": {"value": val, "unit": "°C"}})
        elif sensor_type == "heartrate":
            base = 62 + 8 * math.sin(h / 8.0)
            bpm = int(base + random.uniform(-5, 5))
            readings.append({"timestamp": ts.isoformat(), "data": {"bpm": bpm}})
        elif sensor_type == "activity":
            levels = ["resting", "grazing", "walking", "ruminating"]
            readings.append({"timestamp": ts.isoformat(), "data": {"activity_level": random.choice(levels)}})
    return readings


def get_latest_sensors(cattle_id):
    """Get latest sensor snapshot from the dataset cattle record."""
    cattle = next((c for c in CATTLE if c["_id"] == cattle_id or c["tag_id"] == cattle_id), None)
    if cattle:
        return {
            "temperature": {"data": {"value": cattle.get("temperature_c", 38.5), "unit": "°C"}},
            "heartrate": {"data": {"bpm": cattle.get("heart_rate_bpm", 65)}},
            "activity": {"data": {"activity_level": cattle.get("activity_level", "moderate")}},
        }
    random.seed(hash(cattle_id) % 2**31)
    return {
        "temperature": {"data": {"value": round(38.0 + random.uniform(0, 2.0), 1), "unit": "°C"}},
        "heartrate": {"data": {"bpm": random.randint(55, 80)}},
        "activity": {"data": {"activity_level": random.choice(["grazing", "resting", "walking", "ruminating"])}},
    }


# ---------------------------------------------------------------------------
# GPS positions — from cattle data
# ---------------------------------------------------------------------------
def get_gps_positions(farm_id=None):
    """Get GPS positions, optionally filtered by farm."""
    positions = []
    for c in CATTLE:
        if farm_id and c.get("farm_id") != farm_id:
            continue
        gps = c.get("gps")
        if not gps:
            continue
        positions.append({
            "cattle_id": c.get("tag_id", c.get("_id")),
            "name": c.get("name", "Unknown"),
            "farm_id": c.get("farm_id", ""),
            "lat": gps.get("lat", 0),
            "lng": gps.get("lng", 0),
        })
    return positions


# ---------------------------------------------------------------------------
# HEALTH ALERTS — generated from cattle with non-healthy status
# ---------------------------------------------------------------------------
_alert_types = [
    ("high_fever", "high", "Temperature reading above 40°C"),
    ("irregular_heartbeat", "medium", "Heart rate irregularity detected"),
    ("low_activity", "low", "Activity level below normal for 12+ hours"),
    ("respiratory_distress", "high", "Rapid breathing pattern detected"),
    ("lameness_detected", "medium", "Abnormal gait via activity sensor"),
    ("dehydration_risk", "medium", "Water intake below threshold"),
    ("mastitis_indicator", "high", "Milk yield dropped — possible mastitis"),
    ("weight_loss", "low", "Weight decreased significantly"),
]

HEALTH_ALERTS = []
_sick = [c for c in CATTLE if c.get("health_status", "healthy") != "healthy"]
random.seed(42)
for i, sc in enumerate(_sick):
    atype, severity, msg = _alert_types[i % len(_alert_types)]
    if sc.get("health_status") == "critical":
        severity = "high"
    HEALTH_ALERTS.append({
        "_id": f"alert-{i+1}",
        "cattle_id": sc.get("tag_id", sc.get("_id", f"unknown-{i}")),
        "cattle_name": sc.get("name", "Unknown"),
        "farm_id": sc.get("farm_id", ""),
        "owner_id": sc.get("owner_id", ""),
        "type": atype,
        "severity": severity,
        "message": f"{msg} — {sc.get('name', 'Unknown')} ({sc.get('tag_id', '?')})",
        "status": "active" if i % 4 != 0 else "resolved",
        "created_at": (datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 72))).isoformat(),
    })

# ---------------------------------------------------------------------------
# INSURANCE CLAIMS
# ---------------------------------------------------------------------------
INSURANCE_CLAIMS = []
_critical = [c for c in CATTLE if c["health_status"] == "critical"]
for i, sc in enumerate(_critical[:5]):
    claim_types = ["illness", "death", "accident", "theft"]
    INSURANCE_CLAIMS.append({
        "_id": f"claim-{i+1}",
        "cattle_id": sc["tag_id"],
        "cattle_name": sc["name"],
        "owner_id": sc["owner_id"],
        "farm_id": sc["farm_id"],
        "claim_type": claim_types[i % len(claim_types)],
        "amount": random.randint(10000, 60000),
        "description": f"Insurance claim for {sc['name']} ({sc['tag_id']}) - {sc.get('disease_label', 'illness')}",
        "status": "pending" if i % 2 == 0 else "under_review",
        "fraud_score": None if i % 2 == 0 else random.randint(10, 45),
        "created_at": (datetime.now(timezone.utc) - timedelta(days=random.randint(1, 30))).isoformat(),
    })
