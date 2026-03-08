"""
MongoDB Connection & Operations for MQTT Worker
Author: Jaswanth
"""

from pymongo import MongoClient
from .config import MONGO_URI, DB_NAME

_client = None
_db = None


def get_db():
    """Get MongoDB database connection (singleton)."""
    global _client, _db
    if _client is None:
        _client = MongoClient(MONGO_URI)
        _db = _client[DB_NAME]
    return _db


def insert_sensor_reading(document: dict):
    """Insert a sensor reading document into MongoDB."""
    db = get_db()
    db.sensor_readings.insert_one(document)


def insert_health_alert(alert: dict):
    """Insert a health alert document into MongoDB."""
    db = get_db()
    db.health_alerts.insert_one(alert)
