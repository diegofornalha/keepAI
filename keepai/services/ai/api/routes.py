from flask import Blueprint, request, jsonify
from services.agent_service import AgentService

ai_blueprint = Blueprint("ai", __name__)
agent_service = AgentService()


@ai_blueprint.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    result = agent_service.analyze_text(data["text"])
    return jsonify(result)


@ai_blueprint.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "No prompt provided"}), 400

    result = agent_service.generate_content(data["prompt"])
    return jsonify(result)


@ai_blueprint.route("/summarize", methods=["POST"])
def summarize_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400

    result = agent_service.summarize_text(data["text"])
    return jsonify(result)
