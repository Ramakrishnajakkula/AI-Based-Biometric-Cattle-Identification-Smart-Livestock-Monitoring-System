"""
Seed Database — Insert sample cattle and owner documents for testing
Author: Team

Usage: python scripts/seed_db.py
"""

from pymongo import MongoClient
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/cattle_monitoring")


def seed():
    client = MongoClient(MONGO_URI)
    db = client["cattle_monitoring"]
    
    # Clear existing
    db.cattle.drop()
    db.owners.drop()
    
    # Owners
    owners = [
        {"_id": "OWN-001", "name": "Rajesh Kumar", "phone": "+919876543210", "email": "rajesh@example.com", "farm_id": "FARM-01", "location": {"lat": 17.385, "lng": 78.4867}},
        {"_id": "OWN-002", "name": "Sunita Devi", "phone": "+919876543211", "email": "sunita@example.com", "farm_id": "FARM-02", "location": {"lat": 17.390, "lng": 78.490}},
    ]
    db.owners.insert_many(owners)
    
    # Cattle
    cattle = [
        {"tag_id": "CTL-001", "name": "Lakshmi", "breed": "Gir", "age_years": 4, "weight_kg": 350, "owner_id": "OWN-001", "farm_id": "FARM-01", "health_status": "healthy", "created_at": datetime.now(timezone.utc)},
        {"tag_id": "CTL-002", "name": "Ganga", "breed": "Sahiwal", "age_years": 3, "weight_kg": 320, "owner_id": "OWN-001", "farm_id": "FARM-01", "health_status": "healthy", "created_at": datetime.now(timezone.utc)},
        {"tag_id": "CTL-003", "name": "Nandi", "breed": "Red Sindhi", "age_years": 5, "weight_kg": 400, "owner_id": "OWN-001", "farm_id": "FARM-01", "health_status": "healthy", "created_at": datetime.now(timezone.utc)},
        {"tag_id": "CTL-004", "name": "Kamadhenu", "breed": "Tharparkar", "age_years": 2, "weight_kg": 280, "owner_id": "OWN-002", "farm_id": "FARM-02", "health_status": "healthy", "created_at": datetime.now(timezone.utc)},
        {"tag_id": "CTL-005", "name": "Surabhi", "breed": "Ongole", "age_years": 6, "weight_kg": 450, "owner_id": "OWN-002", "farm_id": "FARM-02", "health_status": "healthy", "created_at": datetime.now(timezone.utc)},
    ]
    db.cattle.insert_many(cattle)
    
    # Create indexes
    db.cattle.create_index("tag_id", unique=True)
    db.cattle.create_index("owner_id")
    db.sensor_readings.create_index([("cattle_id", 1), ("sensor_type", 1), ("received_at", -1)])
    db.health_alerts.create_index([("cattle_id", 1), ("created_at", -1)])
    db.insurance_claims.create_index([("cattle_id", 1), ("status", 1)])
    
    print(f"Seeded {len(owners)} owners and {len(cattle)} cattle")
    print("MongoDB indexes created")
    
    client.close()


if __name__ == "__main__":
    seed()
