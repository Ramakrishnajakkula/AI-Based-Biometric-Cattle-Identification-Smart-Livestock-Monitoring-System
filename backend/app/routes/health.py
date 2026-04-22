"""
Health Routes — Hardcoded alerts
Author: Akash
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
import copy
import os
import uuid
from werkzeug.utils import secure_filename

from ..data_store import HEALTH_ALERTS
from ..services.ml_service import (
    detect_health_issues,
    predict_tabular_health_status,
    get_tabular_features_by_tag_id,
)

health_bp = Blueprint("health", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


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


@health_bp.route("/detect", methods=["POST"])
@jwt_required()
def detect_health_from_image():
    """Detect health issues from an uploaded cattle image."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "" or not _allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    upload_root = os.path.join(os.path.dirname(__file__), "..", "..", "uploads", "health")
    os.makedirs(upload_root, exist_ok=True)
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    filepath = os.path.join(upload_root, filename)
    file.save(filepath)

    result = detect_health_issues(filepath)
    conditions = result.get("conditions", [])

    cattle_id = request.form.get("cattle_id") or request.args.get("cattle_id") or "UNKNOWN"
    created = []
    for item in conditions:
        alert = {
            "_id": f"a{len(HEALTH_ALERTS) + 1}",
            "cattle_id": cattle_id,
            "cattle_name": cattle_id,
            "type": item.get("condition", "health_issue"),
            "severity": item.get("severity", "medium"),
            "message": item.get("description", "Health issue detected"),
            "status": "active",
            "source": "vision",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        HEALTH_ALERTS.append(alert)
        created.append(copy.deepcopy(alert))

    return jsonify({
        "issues": conditions,
        "alerts_created": created,
        "count": len(conditions),
        "image_path": filepath,
    }), 200


@health_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict_health_from_tabular_data():
    """
    Predict health status from structured tabular data.

    Request supports either:
    - {"features": {...}} where keys match model feature columns
    - {"tag_id": "CTL-00001"} to pull features from generated master dataset
    """
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    tag_id = payload.get("tag_id") or payload.get("cattle_id")

    features = payload.get("features")
    if features is None:
        # If no features wrapper is provided, treat payload itself as feature map.
        features = {k: v for k, v in payload.items() if k not in {"tag_id", "cattle_id"}}

    if tag_id and not features:
        try:
            features = get_tabular_features_by_tag_id(str(tag_id))
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    if not isinstance(features, dict) or not features:
        return jsonify({
            "error": "Provide tabular features or a valid tag_id for dataset lookup"
        }), 400

    result = predict_tabular_health_status(features)
    if result.get("error"):
        return jsonify(result), 500

    return jsonify({
        "tag_id": tag_id,
        "prediction": result,
    }), 200
