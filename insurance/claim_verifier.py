"""
Insurance Claim Verifier — Validates claim data against cattle records
Author: Aditi
"""

from datetime import datetime, timezone
from pymongo import MongoClient
import os

from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/cattle_monitoring")


def get_db():
    client = MongoClient(MONGO_URI)
    return client["cattle_monitoring"]


def verify_claim(claim: dict) -> dict:
    """
    Verify an insurance claim by cross-referencing cattle records.
    
    Checks:
        1. Cattle exists in database
        2. Cattle is registered under the claimant
        3. No duplicate claim for same cattle + type within 30 days
        4. Supporting sensor data aligns with claim
    
    Returns:
        dict with verified (bool), score, and reasons list.
    """
    db = get_db()
    cattle_id = claim.get("cattle_id")
    
    result = {"verified": True, "score": 100, "reasons": []}
    
    # Check 1: Cattle exists
    cattle = db.cattle.find_one({"_id": cattle_id}) or db.cattle.find_one({"tag_id": cattle_id})
    if not cattle:
        result["verified"] = False
        result["score"] -= 50
        result["reasons"].append("Cattle not found in database")
        return result
    
    # Check 2: Owner match
    if claim.get("owner_id") and str(cattle.get("owner_id")) != str(claim["owner_id"]):
        result["score"] -= 30
        result["reasons"].append("Owner mismatch: claim owner != registered owner")
    
    # Check 3: Duplicate claim
    existing = db.insurance_claims.find_one({
        "cattle_id": cattle_id,
        "claim_type": claim.get("claim_type"),
        "status": {"$nin": ["rejected"]},
    })
    if existing:
        result["score"] -= 40
        result["reasons"].append("Duplicate claim exists for same cattle and type")
    
    # Check 4: Sensor data support
    if claim.get("claim_type") == "death":
        # Check if recent sensor data exists (cattle should NOT have recent readings if dead)
        from datetime import timedelta
        recent = db.sensor_readings.find_one({
            "cattle_id": cattle_id,
            "received_at": {"$gte": datetime.now(timezone.utc) - timedelta(hours=24)}
        })
        if recent:
            result["score"] -= 20
            result["reasons"].append("Recent sensor data found — contradicts death claim")
    
    result["verified"] = result["score"] >= 60
    return result
