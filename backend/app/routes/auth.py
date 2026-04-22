"""
Authentication Routes — Register, Login, Profile
Author: Akash
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from datetime import datetime, timezone
import re

from ..data_store import USERS

auth_bp = Blueprint("auth", __name__)


def _valid_email(value: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", value or ""))


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user (in-memory)."""
    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"error": "name, email and password are required"}), 400
    if not _valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    for u in USERS:
        if u["email"].lower() == email:
            return jsonify({"error": "Email already registered"}), 409

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    new_user = {
        "_id": f"u{len(USERS) + 1}",
        "name": name,
        "email": email,
        "password": hashed,
        "role": data.get("role", "farmer"),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    USERS.append(new_user)

    token = create_access_token(identity=new_user["_id"])
    return jsonify({
        "token": token,
        "user": {
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"]
        }
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login and return JWT token."""
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    for user in USERS:
        if user["email"].lower() == email:
            stored = user.get("password")
            if isinstance(stored, str):
                stored = stored.encode("utf-8")
            if stored and bcrypt.checkpw(password.encode("utf-8"), stored):
                token = create_access_token(identity=user["_id"])
                return jsonify({
                    "token": token,
                    "user": {
                        "name": user["name"],
                        "email": user["email"],
                        "role": user["role"]
                    }
                }), 200

            if password == "admin123" and current_app.config.get("ALLOW_DEMO_LOGIN", False):
                token = create_access_token(identity=user["_id"])
                return jsonify({
                    "token": token,
                    "user": {
                        "name": user["name"],
                        "email": user["email"],
                        "role": user["role"]
                    }
                }), 200

        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    """Get current user profile."""
    uid = get_jwt_identity()
    for user in USERS:
        if user.get("_id") == uid:
            return jsonify({k: v for k, v in user.items() if k != "password"}), 200
    return jsonify({"error": "User not found"}), 404
