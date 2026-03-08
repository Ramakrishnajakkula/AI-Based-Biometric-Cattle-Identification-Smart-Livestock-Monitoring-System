"""
MQTT Worker Configuration
Author: Jaswanth
"""

import os
from dotenv import load_dotenv

load_dotenv()

# MQTT Broker settings
MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "")

# MongoDB settings
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/cattle_monitoring")
DB_NAME = "cattle_monitoring"

# MQTT Topics to subscribe
MQTT_TOPICS = [
    "livestock/+/+/temperature",
    "livestock/+/+/heartrate",
    "livestock/+/+/gps",
    "livestock/+/+/activity",
    "livestock/+/+/status",
    "livestock/alerts/+/health",
    "livestock/alerts/+/geofence",
]
