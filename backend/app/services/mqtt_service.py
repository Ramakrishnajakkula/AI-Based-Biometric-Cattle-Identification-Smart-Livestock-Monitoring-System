"""
MQTT Service — Manages MQTT subscription & real-time push to frontend
Author: Akash
"""

import json
import logging
import threading

import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)


class MQTTService:
    """MQTT subscriber that forwards messages to SocketIO clients."""
    
    def __init__(self, broker: str, port: int, socketio: SocketIO):
        self.broker = broker
        self.port = port
        self.socketio = socketio
        self.client = mqtt.Client(CallbackAPIVersion.VERSION2, client_id="flask-mqtt-bridge")
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
    
    def _on_connect(self, client, userdata, flags, reason_code, properties):
        logger.info(f"MQTT bridge connected: {reason_code}")
        client.subscribe("livestock/+/+/+")
    
    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            parts = msg.topic.split("/")
            if len(parts) >= 4:
                event = {
                    "farm_id": parts[1],
                    "cattle_id": parts[2],
                    "sensor_type": parts[3],
                    "data": payload
                }
                self.socketio.emit("sensor_update", event)
        except Exception as e:
            logger.error(f"MQTT bridge error: {e}")
    
    def start(self):
        """Start MQTT subscription in a background thread."""
        self.client.connect(self.broker, self.port)
        thread = threading.Thread(target=self.client.loop_forever, daemon=True)
        thread.start()
        logger.info("MQTT → SocketIO bridge started")
