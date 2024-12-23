from flask import Blueprint, jsonify, request

from ..middleware.auth_middleware import auth_required, clerk, current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/webhook", methods=["POST"])
def webhook():
    try:
        event_type = request.json.get("type")
        data = request.json.get("data")

        if not event_type or not data:
            return jsonify({"error": "Invalid webhook payload"}), 400

        result = clerk.handle_webhook(event_type, data)

        if not result["success"]:
            return jsonify({"error": result["error"]}), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/me", methods=["GET"])
@auth_required
def me():
    try:
        user = current_user()
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
