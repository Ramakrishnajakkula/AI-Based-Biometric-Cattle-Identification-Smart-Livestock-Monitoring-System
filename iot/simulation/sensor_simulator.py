"""
Sensor Data Simulator — Simulates ESP32 neckband data for testing
Author: Jaswanth

Publishes realistic sensor data to MQTT topics without requiring physical hardware.
"""

import json
import time
import random
import math
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion

from .cattle_profiles import CATTLE_PROFILES


MQTT_BROKER = "localhost"
MQTT_PORT = 1883
FARM_ID = "FARM-01"
PUBLISH_INTERVAL = 5  # seconds


def generate_temperature(profile: dict, hour: int) -> float:
    """Generate realistic temperature with daily variation."""
    base = profile["base_temp"]
    variation = 0.3 * math.sin(2 * math.pi * hour / 24)  # daily cycle
    noise = random.gauss(0, 0.1)
    return round(base + variation + noise, 1)


def generate_heartrate(profile: dict) -> int:
    """Generate realistic heart rate."""
    base = profile["base_hr"]
    noise = random.randint(-5, 5)
    return max(35, base + noise)


def generate_gps(profile: dict) -> dict:
    """Generate GPS coordinates with small random movement."""
    lat = profile["base_lat"] + random.gauss(0, 0.0001)
    lng = profile["base_lng"] + random.gauss(0, 0.0001)
    return {"lat": round(lat, 6), "lng": round(lng, 6), "altitude": 542.3, "speed": round(random.uniform(0, 2), 1)}


def generate_activity(profile: dict) -> dict:
    """Generate accelerometer data."""
    activity_level = random.choice(["resting", "walking", "grazing"])
    return {
        "accel_x": round(random.gauss(0, 0.5), 2),
        "accel_y": round(random.gauss(0, 0.5), 2),
        "accel_z": round(9.8 + random.gauss(0, 0.1), 2),
        "activity_level": activity_level
    }


def run_simulator():
    """Run the sensor simulator."""
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="cattle-simulator")
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()
    
    print(f"Sensor Simulator started — publishing every {PUBLISH_INTERVAL}s")
    print(f"Simulating {len(CATTLE_PROFILES)} cattle on {FARM_ID}")
    
    try:
        while True:
            now = datetime.now(timezone.utc)
            hour = now.hour
            
            for cattle_id, profile in CATTLE_PROFILES.items():
                device_id = f"ESP32-{FARM_ID}-{cattle_id}"
                timestamp = now.isoformat()
                
                # Temperature
                temp = generate_temperature(profile, hour)
                client.publish(
                    f"livestock/{FARM_ID}/{cattle_id}/temperature",
                    json.dumps({"value": temp, "unit": "celsius", "timestamp": timestamp, "device_id": device_id})
                )
                
                # Heart Rate
                hr = generate_heartrate(profile)
                client.publish(
                    f"livestock/{FARM_ID}/{cattle_id}/heartrate",
                    json.dumps({"bpm": hr, "spo2": random.randint(95, 99), "timestamp": timestamp, "device_id": device_id})
                )
                
                # GPS
                gps = generate_gps(profile)
                client.publish(
                    f"livestock/{FARM_ID}/{cattle_id}/gps",
                    json.dumps({**gps, "timestamp": timestamp, "device_id": device_id})
                )
                
                # Activity
                activity = generate_activity(profile)
                client.publish(
                    f"livestock/{FARM_ID}/{cattle_id}/activity",
                    json.dumps({**activity, "timestamp": timestamp, "device_id": device_id})
                )
                
                print(f"  {cattle_id}: temp={temp}°C, hr={hr}bpm, gps=({gps['lat']},{gps['lng']})")
            
            print(f"--- Cycle complete at {timestamp} ---")
            time.sleep(PUBLISH_INTERVAL)
    
    except KeyboardInterrupt:
        print("\nSimulator stopped.")
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    run_simulator()
