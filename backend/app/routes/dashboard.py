"""
Dashboard Routes — Hardcoded summary stats
Author: Akash
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
import copy

from ..data_store import CATTLE, HEALTH_ALERTS, INSURANCE_CLAIMS

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/stats", methods=["GET"])
@jwt_required()
def get_stats():
    """Get dashboard summary statistics."""
    total_cattle = len(CATTLE)
    healthy = sum(1 for c in CATTLE if c["health_status"] == "healthy")
    sick = total_cattle - healthy

    active_alerts = sum(1 for a in HEALTH_ALERTS if a["status"] != "resolved")
    pending_claims = sum(1 for c in INSURANCE_CLAIMS if c["status"] == "pending")

    return jsonify({
        "total_cattle": total_cattle,
        "healthy": healthy,
        "sick": sick,
        "active_alerts": active_alerts,
        "pending_claims": pending_claims
    }), 200


@dashboard_bp.route("/recent-alerts", methods=["GET"])
@jwt_required()
def recent_alerts():
    """Get recent health alerts."""
    return jsonify({"alerts": copy.deepcopy(HEALTH_ALERTS[:10])}), 200
