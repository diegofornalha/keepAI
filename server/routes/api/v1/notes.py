from flask import Blueprint, request, jsonify, Response
from server.routes.auth import require_auth
from server.modules.notes_manager import NotesManager

notes_bp = Blueprint("notes", __name__)
notes_manager = NotesManager()


@notes_bp.route("/notes", methods=["POST"])
@require_auth
def create_note() -> tuple[Response, int]:
    """Cria uma nova nota"""
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Conteúdo não fornecido"}), 400

    result = notes_manager.create_note(request.user_id, content)  # type: ignore
    if result["success"]:
        return jsonify(result), 201
    return jsonify(result), 500


@notes_bp.route("/notes/<note_id>", methods=["GET"])
@require_auth
def get_note(note_id: str) -> tuple[Response, int]:
    """Retorna uma nota específica"""
    note = notes_manager.get_note(note_id)
    if note:
        return jsonify({"success": True, "data": note}), 200
    return jsonify({"error": "Nota não encontrada"}), 404


@notes_bp.route("/notes/<note_id>", methods=["PUT"])
@require_auth
def update_note(note_id: str) -> tuple[Response, int]:
    """Atualiza uma nota existente"""
    data = request.get_json()
    content = data.get("content")

    if not content:
        return jsonify({"error": "Conteúdo não fornecido"}), 400

    result = notes_manager.update_note(note_id, content)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500


@notes_bp.route("/notes/<note_id>", methods=["DELETE"])
@require_auth
def delete_note(note_id: str) -> tuple[Response, int]:
    """Deleta uma nota"""
    result = notes_manager.delete_note(note_id)
    if result["success"]:
        return jsonify(result), 200
    return jsonify(result), 500
