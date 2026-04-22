"""
Insurance Routes — Hardcoded claims
Author: Akash
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timezone
import copy

from ..data_store import INSURANCE_CLAIMS, CATTLE, get_gps_positions

try:
    from insurance.geo_verifier import verify_location
except ImportError:
    verify_location = None

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
        if c["_id"] != claim_id:
            continue

        reasons = []
        score = 0

        # Find cattle in app store.
        cattle = next((x for x in CATTLE if x["tag_id"] == c["cattle_id"] or x["_id"] == c["cattle_id"]), None)
        if not cattle:
            score += 60
            reasons.append("Cattle record not found")
        else:
            # Owner mismatch check.
            if c.get("owner_id") and cattle.get("owner_id") and str(c["owner_id"]) != str(cattle["owner_id"]):
                score += 30
                reasons.append("Owner mismatch with registered cattle owner")

            # Duplicate active claims check.
            dup_count = sum(
                1 for x in INSURANCE_CLAIMS
                if x["_id"] != c["_id"] and x.get("cattle_id") == c.get("cattle_id") and x.get("claim_type") == c.get("claim_type") and x.get("status") != "rejected"
            )
            if dup_count > 0:
                score += 25
                reasons.append("Duplicate active claim found")

            # Pattern check on owner.
            owner_claim_count = sum(1 for x in INSURANCE_CLAIMS if x.get("owner_id") == c.get("owner_id"))
            if owner_claim_count >= 3:
                score += 10
                reasons.append("Owner has multiple claims")

            # Geo check using existing GPS demo data.
            gps = None
            if cattle:
                all_gps = get_gps_positions()
                gps = next((p for p in all_gps if p["cattle_id"] == cattle.get("tag_id")), None)
            if verify_location and gps:
                farm_center = {"lat": 17.3850, "lng": 78.4867}
                geo = verify_location(gps, farm_center, radius_meters=5000)
                if not geo.get("within_fence", True):
                    score += 20
                    reasons.append("Cattle outside expected farm geofence")

        score = min(score, 100)
        if score >= 70:
            risk_level = "HIGH"
            recommendation = "REJECT"
            status = "rejected"
        elif score >= 40:
            risk_level = "MEDIUM"
            recommendation = "REVIEW"
            status = "under_review"
        else:
            risk_level = "LOW"
            recommendation = "APPROVE"
            status = "approved"

        c["fraud_score"] = score
        c["status"] = status
        c["verification"] = {
            "risk_level": risk_level,
            "recommendation": recommendation,
            "reasons": reasons,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }
        c["updated_at"] = datetime.now(timezone.utc).isoformat()

        return jsonify({
            "claim_id": claim_id,
            "fraud_score": score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "status": c["status"],
            "reasons": reasons,
        }), 200

    return jsonify({"error": "Claim not found"}), 404
