from flask import Blueprint, jsonify, Response

api_v1_bp = Blueprint("api_v1", __name__)


@api_v1_bp.route("/status")
def status() -> tuple[Response, int]:
    return jsonify({"status": "online", "version": "1.0.0"}), 200
