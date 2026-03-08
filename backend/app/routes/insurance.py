"""
Insurance Routes — Hardcoded claims
Author: Akash
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
import copy

from ..data_store import INSURANCE_CLAIMS

insurance_bp = Blueprint("insurance", __name__)


@insurance_bp.route("/claims", methods=["GET"])
@jwt_required()
def list_claims():
    """List all insurance claims."""
    return jsonify({"claims": copy.deepcopy(INSURANCE_CLAIMS), "total": len(INSURANCE_CLAIMS)}), 200


@insurance_bp.route("/claims", methods=["POST"])
@jwt_required()
def create_claim():
    """Create a new insurance claim."""
    data = request.get_json()

    claim = {
        "_id": f"claim{len(INSURANCE_CLAIMS) + 1}",
        "cattle_id": data["cattle_id"],
        "owner_id": data.get("owner_id"),
        "claim_type": data["claim_type"],
        "description": data.get("description", ""),
        "amount": data.get("amount", 0),
        "status": "pending",
        "fraud_score": None,
        "submitted_by": get_jwt_identity(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    INSURANCE_CLAIMS.append(claim)
    return jsonify(claim), 201


@insurance_bp.route("/claims/<claim_id>", methods=["GET"])
@jwt_required()
def get_claim(claim_id):
    """Get claim details."""
    for c in INSURANCE_CLAIMS:
        if c["_id"] == claim_id:
            return jsonify(copy.deepcopy(c)), 200
    return jsonify({"error": "Claim not found"}), 404


@insurance_bp.route("/claims/<claim_id>/verify", methods=["POST"])
@jwt_required()
def verify_claim(claim_id):
    """Trigger fraud verification for a claim."""
    for c in INSURANCE_CLAIMS:
        if c["_id"] == claim_id:
            c["status"] = "under_review"
            c["updated_at"] = datetime.now(timezone.utc).isoformat()
            return jsonify({"message": "Verification initiated", "claim_id": claim_id}), 200
    return jsonify({"error": "Claim not found"}), 404
