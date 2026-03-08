"""
Health Routes — Hardcoded alerts
Author: Akash
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
import copy

from ..data_store import HEALTH_ALERTS

health_bp = Blueprint("health", __name__)


@health_bp.route("/alerts", methods=["GET"])
@jwt_required()
def get_alerts():
    """Get all health alerts with optional filters."""
    severity = request.args.get("severity")
    status = request.args.get("status")

    result = HEALTH_ALERTS
    if severity:
        result = [a for a in result if a["severity"] == severity]
    if status:
        result = [a for a in result if a["status"] == status]
    else:
        result = [a for a in result if a["status"] != "resolved"]

    return jsonify({"alerts": copy.deepcopy(result), "total": len(result)}), 200


@health_bp.route("/alerts/<cattle_id>", methods=["GET"])
@jwt_required()
def get_cattle_alerts(cattle_id):
    """Get health alerts for a specific cattle."""
    alerts = [a for a in HEALTH_ALERTS if a["cattle_id"] == cattle_id]
    return jsonify({"cattle_id": cattle_id, "alerts": copy.deepcopy(alerts)}), 200


@health_bp.route("/alerts/<alert_id>/resolve", methods=["PUT"])
@jwt_required()
def resolve_alert(alert_id):
    """Mark a health alert as resolved."""
    for a in HEALTH_ALERTS:
        if a["_id"] == alert_id:
            a["status"] = "resolved"
            a["resolved_at"] = datetime.now(timezone.utc).isoformat()
            return jsonify({"message": "Alert resolved"}), 200
    return jsonify({"error": "Alert not found"}), 404
