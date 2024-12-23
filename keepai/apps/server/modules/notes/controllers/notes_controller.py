from typing import Any, Dict

from flask import Blueprint, jsonify, request

from ..schemas.note_schema import NoteCreate, NoteList, NoteUpdate, TagList
from ..services.note_service import NoteService

notes_bp = Blueprint("notes", __name__)
note_service = NoteService()


@notes_bp.route("", methods=["GET"])
def get_notes():
    """Lista todas as notas"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    tag = request.args.get("tag")

    if tag:
        notes = note_service.get_notes_by_tag(tag)
    else:
        notes = note_service.get_all_notes()

    # Paginação básica
    start = (page - 1) * per_page
    end = start + per_page
    paginated_notes = notes[start:end]

    return jsonify(
        NoteList(
            notes=paginated_notes, total=len(notes), page=page, per_page=per_page
        ).dict()
    )


@notes_bp.route("/<int:note_id>", methods=["GET"])
def get_note(note_id: int):
    """Retorna uma nota específica"""
    note = note_service.get_note_by_id(note_id)
    if note:
        return jsonify(note)
    return jsonify({"error": "Nota não encontrada"}), 404


@notes_bp.route("", methods=["POST"])
def create_note():
    """Cria uma nova nota"""
    data = request.get_json()
    note_data = NoteCreate(**data).dict()
    note = note_service.create_note(note_data)
    return jsonify(note), 201


@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id: int):
    """Atualiza uma nota existente"""
    data = request.get_json()
    note_data = NoteUpdate(**data).dict(exclude_unset=True)
    note = note_service.update_note(note_id, note_data)
    if note:
        return jsonify(note)
    return jsonify({"error": "Nota não encontrada"}), 404


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id: int):
    """Remove uma nota"""
    note_service.delete_note(note_id)
    return "", 204


@notes_bp.route("/search", methods=["GET"])
def search_notes():
    """Pesquisa notas"""
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Parâmetro de busca não fornecido"}), 400

    notes = note_service.search_notes(query)
    return jsonify(notes)


@notes_bp.route("/tags", methods=["GET"])
def get_tags():
    """Lista todas as tags"""
    tags = note_service.get_all_tags()
    return jsonify(TagList(tags=tags).dict())
