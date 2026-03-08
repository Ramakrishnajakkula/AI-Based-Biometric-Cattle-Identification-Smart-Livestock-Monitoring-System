"""
MQTT Message Handlers - Process incoming sensor data
Author: Jaswanth
"""

import logging
from datetime import datetime, timezone
from .db import insert_sensor_reading
from .alert_checker import check_thresholds

logger = logging.getLogger(__name__)


def handle_sensor_message(topic: str, payload: dict):
    """
    Route incoming MQTT messages to appropriate handlers.
    
    Topic format: livestock/{farm_id}/{cattle_id}/{sensor_type}
    """
    parts = topic.split("/")
    
    if len(parts) < 4:
        logger.warning(f"Invalid topic format: {topic}")
        return
    
    farm_id = parts[1]
    cattle_id = parts[2]
    sensor_type = parts[3]
    
    # Build document for MongoDB
    document = {
        "cattle_id": cattle_id,
        "farm_id": farm_id,
        "sensor_type": sensor_type,
        "data": payload,
        "device_id": payload.get("device_id", "unknown"),
        "timestamp": payload.get("timestamp", datetime.now(timezone.utc).isoformat()),
        "received_at": datetime.now(timezone.utc)
    }
    
    # Store in MongoDB
    insert_sensor_reading(document)
    logger.info(f"Stored {sensor_type} data for {cattle_id}")
    
    # Check for anomalies
    alerts = check_thresholds(cattle_id, sensor_type, payload)
    if alerts:
        for alert in alerts:
            logger.warning(f"ALERT for {cattle_id}: {alert['type']} - {alert['message']}")
