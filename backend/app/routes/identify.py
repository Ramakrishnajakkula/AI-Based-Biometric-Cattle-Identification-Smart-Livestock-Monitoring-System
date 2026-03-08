"""
Identify Routes — Demo cattle identification
Author: Akash
"""

import os
import uuid
import random
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

from ..data_store import CATTLE

identify_bp = Blueprint("identify", __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@identify_bp.route("/", methods=["POST"])
@jwt_required()
def identify_cattle():
    """
    Upload an image and return a demo identification result.
    In production this would run YOLOv8 + ArcFace pipeline.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Save file
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "identify")
    os.makedirs(upload_dir, exist_ok=True)
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)

    # Demo: randomly match one of the hardcoded cattle
    matched = random.choice(CATTLE)
    confidence = round(random.uniform(0.82, 0.98), 2)

    return jsonify({
        "matched": True,
        "confidence": confidence,
        "cattle": {
            "_id": matched["_id"],
            "tag_id": matched["tag_id"],
            "name": matched["name"],
            "breed": matched["breed"],
            "health_status": matched["health_status"]
        },
        "image_path": filepath
    }), 200
