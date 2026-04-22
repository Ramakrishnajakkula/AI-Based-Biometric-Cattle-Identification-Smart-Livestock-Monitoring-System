"""
RBAC Helpers — Role-based access control utilities
Author: Akash
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from .data_store import USERS


def get_current_user():
    """Get the full user object for the currently authenticated user."""
    uid = get_jwt_identity()
    for u in USERS:
        if u["_id"] == uid:
            return u
    return None


def admin_required(fn):
    """Decorator: only allow admin users."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_current_user()
        if not user or user["role"] != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def get_user_cattle_filter(user):
    """Return a filter function that checks cattle ownership.
    Admin sees all; farmer sees only their farm's cattle.
    """
    if user["role"] == "admin":
        return lambda c: True
    return lambda c: c.get("farm_id") == user.get("farm_id")
