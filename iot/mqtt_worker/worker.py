"""
MQTT Worker - Subscribes to sensor topics and stores data in MongoDB
Author: Jaswanth
"""

import json
import os
import logging
from datetime import datetime, timezone

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from dotenv import load_dotenv

from .handlers import handle_sensor_message
from .config import MQTT_BROKER, MQTT_PORT, MQTT_TOPICS

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def on_connect(client, userdata, flags, reason_code, properties):
    """Callback when connected to MQTT broker."""
    logger.info(f"Connected to MQTT broker: {reason_code}")
    for topic in MQTT_TOPICS:
        client.subscribe(topic)
        logger.info(f"Subscribed to: {topic}")


def on_message(client, userdata, msg):
    """Callback when message received."""
    try:
        payload = json.loads(msg.payload.decode())
        handle_sensor_message(msg.topic, payload)
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON on topic {msg.topic}")
    except Exception as e:
        logger.error(f"Error handling message: {e}")


def on_disconnect(client, userdata, flags, reason_code, properties):
    """Callback when disconnected."""
    logger.warning(f"Disconnected from MQTT broker: {reason_code}")


def start_worker():
    """Start the MQTT subscriber worker."""
    client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="cattle-mqtt-worker")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    
    logger.info(f"Connecting to MQTT broker at {MQTT_BROKER}:{MQTT_PORT}")
    client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
    
    logger.info("MQTT Worker started. Listening for sensor data...")
    client.loop_forever()


if __name__ == "__main__":
    start_worker()
