"""
Utility Helpers — Response formatting, file handling
Author: Akash
"""

from flask import jsonify


def api_response(data=None, message="Success", status=200, error=None):
    """Standard API response wrapper."""
    body = {"success": status < 400, "message": message}
    if data is not None:
        body["data"] = data
    if error:
        body["error"] = error
    return jsonify(body), status


def paginate(query_result, page: int = 1, per_page: int = 20):
    """Paginate a MongoDB cursor result."""
    skip = (page - 1) * per_page
    items = list(query_result.skip(skip).limit(per_page))
    for item in items:
        item["_id"] = str(item["_id"])
    return items
