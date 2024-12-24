from flask import Blueprint, render_template, jsonify, Response, request
from server.services.ai import process_chat_message

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    return render_template("index.html")


@main_bp.route("/health")
def health() -> tuple[Response, int]:
    return jsonify({"status": "healthy", "version": "0.1.0"}), 200


@main_bp.route("/notes")
def notes() -> str:
    return render_template("notes.html")


@main_bp.route("/tasks")
def tasks() -> str:
    return render_template("tasks.html")


@main_bp.route("/calendar")
def calendar() -> str:
    return render_template("calendar.html")


@main_bp.route("/settings")
def settings() -> str:
    return render_template("settings.html")


@main_bp.route("/chat")
def chat() -> str:
    return render_template("chat.html")


@main_bp.route("/api/v1/chat", methods=["POST"])
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
