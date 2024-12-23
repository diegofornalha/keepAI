from typing import Any, Dict

from flask import Blueprint, jsonify, request
from flasgger import swag_from

from ..schemas.note_schema import NoteCreate, NoteList, NoteUpdate, TagList
from ..services.note_service import NoteService

notes_bp = Blueprint("notes", __name__)
note_service = NoteService()


@notes_bp.route("", methods=["GET"])
def get_notes():
    """
    Lista todas as notas
    ---
    tags:
      - Notas
    parameters:
      - name: page
        in: query
        type: integer
        default: 1
        description: Número da página
      - name: per_page
        in: query
        type: integer
        default: 10
        description: Itens por página
      - name: tag
        in: query
        type: string
        description: Filtrar por tag
    responses:
      200:
        description: Lista de notas
        schema:
          type: object
          properties:
            notes:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  title:
                    type: string
                  content:
                    type: string
                  tags:
                    type: array
                    items:
                      type: string
            total:
              type: integer
            page:
              type: integer
            per_page:
              type: integer
    """
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
    """
    Retorna uma nota específica
    ---
    tags:
      - Notas
    parameters:
      - name: note_id
        in: path
        type: integer
        required: true
        description: ID da nota
    responses:
      200:
        description: Nota encontrada
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            content:
              type: string
            tags:
              type: array
              items:
                type: string
      404:
        description: Nota não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    note = note_service.get_note_by_id(note_id)
    if note:
        return jsonify(note)
    return jsonify({"error": "Nota não encontrada"}), 404


@notes_bp.route("", methods=["POST"])
def create_note():
    """
    Cria uma nova nota
    ---
    tags:
      - Notas
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - title
            - content
          properties:
            title:
              type: string
              description: Título da nota
            content:
              type: string
              description: Conteúdo da nota
            tags:
              type: array
              items:
                type: string
              description: Tags da nota
    responses:
      201:
        description: Nota criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            content:
              type: string
            tags:
              type: array
              items:
                type: string
    """
    data = request.get_json()
    note_data = NoteCreate(**data).dict()
    note = note_service.create_note(note_data)
    return jsonify(note), 201


@notes_bp.route("/<int:note_id>", methods=["PUT"])
def update_note(note_id: int):
    """
    Atualiza uma nota existente
    ---
    tags:
      - Notas
    parameters:
      - name: note_id
        in: path
        type: integer
        required: true
        description: ID da nota
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Título da nota
            content:
              type: string
              description: Conteúdo da nota
            tags:
              type: array
              items:
                type: string
              description: Tags da nota
    responses:
      200:
        description: Nota atualizada com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
            title:
              type: string
            content:
              type: string
            tags:
              type: array
              items:
                type: string
      404:
        description: Nota não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    data = request.get_json()
    note_data = NoteUpdate(**data).dict(exclude_unset=True)
    note = note_service.update_note(note_id, note_data)
    if note:
        return jsonify(note)
    return jsonify({"error": "Nota não encontrada"}), 404


@notes_bp.route("/<int:note_id>", methods=["DELETE"])
def delete_note(note_id: int):
    """
    Remove uma nota
    ---
    tags:
      - Notas
    parameters:
      - name: note_id
        in: path
        type: integer
        required: true
        description: ID da nota
    responses:
      204:
        description: Nota removida com sucesso
      404:
        description: Nota não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
    note_service.delete_note(note_id)
    return "", 204


@notes_bp.route("/search", methods=["GET"])
def search_notes():
    """
    Pesquisa notas
    ---
    tags:
      - Notas
    parameters:
      - name: q
        in: query
        type: string
        required: true
        description: Termo de busca
    responses:
      200:
        description: Resultados da pesquisa
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              title:
                type: string
              content:
                type: string
              tags:
                type: array
                items:
                  type: string
      400:
        description: Parâmetro de busca não fornecido
        schema:
          type: object
          properties:
            error:
              type: string
    """
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "Parâmetro de busca não fornecido"}), 400

    notes = note_service.search_notes(query)
    return jsonify(notes)


@notes_bp.route("/tags", methods=["GET"])
def get_tags():
    """
    Lista todas as tags
    ---
    tags:
      - Notas
    responses:
      200:
        description: Lista de tags
        schema:
          type: object
          properties:
            tags:
              type: array
              items:
                type: string
    """
    tags = note_service.get_all_tags()
    return jsonify(TagList(tags=tags).dict())
