"""
Authentication Routes — Register, Login, Profile
Author: Akash

Uses hardcoded users — no MongoDB required.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from datetime import datetime, timezone

from ..data_store import USERS

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user (adds to in-memory list)."""
    data = request.get_json()

    # Check if user exists
    for u in USERS:
        if u["email"] == data["email"]:
            return jsonify({"error": "Email already registered"}), 409

    hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
    new_user = {
        "_id": f"u{len(USERS) + 1}",
        "name": data["name"],
        "email": data["email"],
        "password": hashed.decode("utf-8"),
        "role": data.get("role", "farmer"),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    USERS.append(new_user)

    token = create_access_token(identity=new_user["_id"])
    return jsonify({"token": token, "user": {"name": new_user["name"], "email": new_user["email"], "role": new_user["role"]}}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login and return JWT token."""
    data = request.get_json()

    for user in USERS:
        if user["email"] == data["email"]:
            # Accept any password for demo convenience, or check bcrypt
            try:
                stored = user["password"]
                if isinstance(stored, str):
                    stored = stored.encode("utf-8")
                if bcrypt.checkpw(data["password"].encode("utf-8"), stored):
                    token = create_access_token(identity=user["_id"])
                    return jsonify({"token": token, "user": {"name": user["name"], "email": user["email"], "role": user["role"]}}), 200
            except Exception:
                pass
            # Fallback: accept password "admin123" for all demo users
            if data["password"] == "admin123":
                token = create_access_token(identity=user["_id"])
                return jsonify({"token": token, "user": {"name": user["name"], "email": user["email"], "role": user["role"]}}), 200

    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """Get current user profile."""
    uid = get_jwt_identity()
    for user in USERS:
        if user["_id"] == uid:
            return jsonify({k: v for k, v in user.items() if k != "password"}), 200
    return jsonify({"error": "User not found"}), 404
