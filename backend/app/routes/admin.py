"""
Admin Routes — Admin dashboard and user management APIs.
"""

from datetime import datetime, timezone
import copy

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..data_store import USERS, CATTLE, HEALTH_ALERTS, INSURANCE_CLAIMS

admin_bp = Blueprint("admin", __name__)

ALLOWED_ROLES = {"admin", "farmer", "veterinarian"}


def _current_user():
    uid = get_jwt_identity()
    return next((u for u in USERS if u.get("_id") == uid), None)


def _require_admin():
    user = _current_user()
    if not user:
        return None, (jsonify({"error": "User not found"}), 404)
    if user.get("role") != "admin":
        return None, (jsonify({"error": "Admin access required"}), 403)
    return user, None


@admin_bp.route("/stats", methods=["GET"])
@jwt_required()
def admin_stats():
    """Admin dashboard summary metrics."""
    _, err = _require_admin()
    if err:
        return err

    total_users = len(USERS)
    admins = sum(1 for u in USERS if u.get("role") == "admin")
    farmers = sum(1 for u in USERS if u.get("role") == "farmer")
    veterinarians = sum(1 for u in USERS if u.get("role") == "veterinarian")

    total_cattle = len(CATTLE)
    active_alerts = sum(1 for a in HEALTH_ALERTS if a.get("status") != "resolved")
    pending_claims = sum(1 for c in INSURANCE_CLAIMS if c.get("status") == "pending")
    high_risk_claims = sum(1 for c in INSURANCE_CLAIMS if (c.get("fraud_score") or 0) >= 70)

    return jsonify({
        "total_users": total_users,
        "admins": admins,
        "farmers": farmers,
        "veterinarians": veterinarians,
        "total_cattle": total_cattle,
        "active_alerts": active_alerts,
        "pending_claims": pending_claims,
        "high_risk_claims": high_risk_claims,
    }), 200


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def list_users():
    """List all users (password removed)."""
    _, err = _require_admin()
    if err:
        return err

    users = []
    for user in USERS:
        row = copy.deepcopy(user)
        row.pop("password", None)
        users.append(row)

    return jsonify({"users": users, "total": len(users)}), 200


@admin_bp.route("/users/<user_id>/role", methods=["PUT"])
@jwt_required()
def update_user_role(user_id):
    """Update user role by admin."""
    _, err = _require_admin()
    if err:
        return err

    payload = request.get_json() or {}
    new_role = (payload.get("role") or "").strip().lower()
    if new_role not in ALLOWED_ROLES:
        return jsonify({"error": f"role must be one of: {sorted(ALLOWED_ROLES)}"}), 400

    for user in USERS:
        if user.get("_id") == user_id:
            user["role"] = new_role
            user["updated_at"] = datetime.now(timezone.utc).isoformat()
            sanitized = {k: v for k, v in user.items() if k != "password"}
            return jsonify({"message": "Role updated", "user": sanitized}), 200

    return jsonify({"error": "User not found"}), 404


@admin_bp.route("/claims", methods=["GET"])
@jwt_required()
def list_claims():
    """List insurance claims for admin review."""
    _, err = _require_admin()
    if err:
        return err

    status = request.args.get("status")
    claims = INSURANCE_CLAIMS
    if status:
        claims = [c for c in claims if c.get("status") == status]

    return jsonify({"claims": copy.deepcopy(claims), "total": len(claims)}), 200
