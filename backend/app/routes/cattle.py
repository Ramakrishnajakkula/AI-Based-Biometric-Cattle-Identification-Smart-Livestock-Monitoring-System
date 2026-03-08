"""
Cattle CRUD Routes — Hardcoded data
Author: Akash
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime, timezone
import copy

from ..data_store import CATTLE

cattle_bp = Blueprint("cattle", __name__)


@cattle_bp.route("/", methods=["GET"])
@jwt_required()
def list_cattle():
    """List all cattle with optional filters."""
    query_breed = request.args.get("breed")
    query_status = request.args.get("status")

    result = CATTLE
    if query_breed:
        result = [c for c in result if c["breed"] == query_breed]
    if query_status:
        result = [c for c in result if c["health_status"] == query_status]

    return jsonify({"cattle": copy.deepcopy(result), "total": len(result)}), 200


@cattle_bp.route("/<cattle_id>", methods=["GET"])
@jwt_required()
def get_cattle(cattle_id):
    """Get single cattle details."""
    for c in CATTLE:
        if c["_id"] == cattle_id or c["tag_id"] == cattle_id:
            return jsonify(copy.deepcopy(c)), 200
    return jsonify({"error": "Cattle not found"}), 404


@cattle_bp.route("/", methods=["POST"])
@jwt_required()
def register_cattle():
    """Register a new cattle."""
    data = request.get_json()

    cattle = {
        "_id": f"c{len(CATTLE) + 1}",
        "tag_id": data["tag_id"],
        "name": data.get("name", ""),
        "breed": data["breed"],
        "age_years": data.get("age_years"),
        "weight_kg": data.get("weight_kg"),
        "owner_id": data.get("owner_id"),
        "farm_id": data.get("farm_id"),
        "health_status": "healthy",
        "image_url": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    CATTLE.append(cattle)
    return jsonify(cattle), 201


@cattle_bp.route("/<cattle_id>", methods=["PUT"])
@jwt_required()
def update_cattle(cattle_id):
    """Update cattle record."""
    data = request.get_json()
    for c in CATTLE:
        if c["_id"] == cattle_id:
            for k, v in data.items():
                c[k] = v
            c["updated_at"] = datetime.now(timezone.utc).isoformat()
            return jsonify({"message": "Updated successfully"}), 200
    return jsonify({"error": "Cattle not found"}), 404


@cattle_bp.route("/<cattle_id>", methods=["DELETE"])
@jwt_required()
def delete_cattle(cattle_id):
    """Delete cattle record."""
    for i, c in enumerate(CATTLE):
        if c["_id"] == cattle_id:
            CATTLE.pop(i)
            return jsonify({"message": "Deleted successfully"}), 200
    return jsonify({"error": "Cattle not found"}), 404
