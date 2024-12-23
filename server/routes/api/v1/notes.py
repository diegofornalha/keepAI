from flask import Blueprint, jsonify, request
from server.models.note import Note
from server.database import supabase
from server.routes.auth import require_auth
from datetime import datetime

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/", methods=["GET"])
@require_auth
def get_notes():
    response = (
        supabase.table("notes").select("*").eq("user_id", request.user_id).execute()
    )
    notes = [Note(note) for note in response.data]
    return jsonify([note.to_dict() for note in notes])


@notes_bp.route("/", methods=["POST"])
@require_auth
def create_note():
    data = request.get_json()
    note_data = {
        "title": data["title"],
        "content": data["content"],
        "user_id": request.user_id,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }
    response = supabase.table("notes").insert(note_data).execute()
    note = Note(response.data[0])
    return jsonify(note.to_dict()), 201


@notes_bp.route("/<int:note_id>", methods=["PUT"])
@require_auth
def update_note(note_id):
    # Verificar se a nota existe e pertence ao usuário
    response = (
        supabase.table("notes")
        .select("*")
        .eq("id", note_id)
        .eq("user_id", request.user_id)
        .execute()
    )
    if not response.data:
        return jsonify({"error": "Nota não encontrada"}), 404

    data = request.get_json()
    update_data = {
        "title": data.get("title", response.data[0]["title"]),
        "content": data.get("content", response.data[0]["content"]),
        "updated_at": datetime.utcnow().isoformat(),
    }

    response = supabase.table("notes").update(update_data).eq("id", note_id).execute()
    note = Note(response.data[0])
    return jsonify(note.to_dict())


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
@require_auth
def delete_note(note_id):
    # Verificar se a nota existe e pertence ao usuário
    response = (
        supabase.table("notes")
        .select("*")
        .eq("id", note_id)
        .eq("user_id", request.user_id)
        .execute()
    )
    if not response.data:
        return jsonify({"error": "Nota não encontrada"}), 404

    supabase.table("notes").delete().eq("id", note_id).execute()
    return jsonify({"message": "Nota excluída com sucesso"})
