from flask import Blueprint, jsonify, Response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/status")
def status() -> tuple[Response, int]:
    return jsonify({"status": "online", "auth_provider": "clerk"}), 200
