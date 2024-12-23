from flask import Blueprint, render_template, jsonify, Response, request
from server.routes.auth import require_auth
from server.services.ai import process_chat_message

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    return render_template("index.html")


@main_bp.route("/health")
def health() -> tuple[Response, int]:
    return jsonify({"status": "healthy", "version": "0.1.0"}), 200


@main_bp.route("/notes")
@require_auth
def notes() -> str:
    return render_template("notes.html")


@main_bp.route("/tasks")
@require_auth
def tasks() -> str:
    return render_template("tasks.html")


@main_bp.route("/calendar")
@require_auth
def calendar() -> str:
    return render_template("calendar.html")


@main_bp.route("/settings")
@require_auth
def settings() -> str:
    return render_template("settings.html")


@main_bp.route("/chat")
@require_auth
def chat() -> str:
    return render_template("chat.html")


@main_bp.route("/api/v1/chat", methods=["POST"])
@require_auth
def chat_message() -> tuple[Response, int]:
    data = request.get_json()
    message = data.get("message")

    if not message:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    try:
        response = process_chat_message(message)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
