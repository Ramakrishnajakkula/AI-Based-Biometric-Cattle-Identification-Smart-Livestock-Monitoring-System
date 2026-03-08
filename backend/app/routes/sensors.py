"""
Sensor Data Routes — Hardcoded sensor readings
Author: Akash
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from ..data_store import get_latest_sensors, _generate_sensor_history, CATTLE_GPS

sensors_bp = Blueprint("sensors", __name__)


@sensors_bp.route("/<cattle_id>/latest", methods=["GET"])
@jwt_required()
def get_latest_reading(cattle_id):
    """Get latest sensor readings for a cattle."""
    latest = get_latest_sensors(cattle_id)
    return jsonify({"cattle_id": cattle_id, "latest": latest}), 200


@sensors_bp.route("/<cattle_id>/history", methods=["GET"])
@jwt_required()
def get_sensor_history(cattle_id):
    """Get sensor history for a cattle within a date range."""
    sensor_type = request.args.get("type", "temperature")
    hours = int(request.args.get("hours", 24))

    readings = _generate_sensor_history(cattle_id, sensor_type, hours)
    return jsonify({"cattle_id": cattle_id, "sensor_type": sensor_type, "readings": readings}), 200


@sensors_bp.route("/gps", methods=["GET"])
@jwt_required()
def get_all_gps():
    """Get GPS positions for all cattle."""
    import copy, random
    positions = []
    for cid, pos in CATTLE_GPS.items():
        p = copy.deepcopy(pos)
        # tiny random drift to simulate movement
        p["lat"] += random.uniform(-0.001, 0.001)
        p["lng"] += random.uniform(-0.001, 0.001)
        positions.append(p)
    return jsonify({"positions": positions}), 200
