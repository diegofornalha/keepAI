from flask import Blueprint, request, jsonify
from flask_socketio import emit
from flasgger import swag_from
from typing import Dict, Any

realtime_blueprint = Blueprint("realtime", __name__)


@realtime_blueprint.route("/rooms", methods=["GET"])
def list_rooms():
    """
    Lista todas as salas ativas
    ---
    tags:
      - Tempo Real
    responses:
      200:
        description: Lista de salas ativas
        schema:
          type: array
          items:
            type: string
            description: ID da sala
    """
    from flask import current_app

    rooms = current_app.config.get("active_rooms", {})
    return jsonify(list(rooms.keys()))


@realtime_blueprint.route("/rooms", methods=["POST"])
def create_room():
    """
    Cria uma nova sala
    ---
    tags:
      - Tempo Real
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - room_id
          properties:
            room_id:
              type: string
              description: ID da sala a ser criada
    responses:
      200:
        description: Sala criada com sucesso
        schema:
          type: object
          properties:
            room_id:
              type: string
              description: ID da sala criada
            status:
              type: string
              description: Status da operação
      400:
        description: ID da sala não fornecido
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        data = request.get_json()
        room_id = data.get("room_id")

        if not room_id:
            return jsonify({"error": "ID da sala não fornecido"}), 400

        # Adicionar sala à lista de salas ativas
        from flask import current_app

        rooms = current_app.config.setdefault("active_rooms", {})
        rooms[room_id] = {"users": [], "messages": []}

        return jsonify({"room_id": room_id, "status": "created"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@realtime_blueprint.route("/rooms/<room_id>", methods=["DELETE"])
def delete_room(room_id: str):
    """
    Remove uma sala
    ---
    tags:
      - Tempo Real
    parameters:
      - name: room_id
        in: path
        type: string
        required: true
        description: ID da sala a ser removida
    responses:
      200:
        description: Sala removida com sucesso
        schema:
          type: object
          properties:
            room_id:
              type: string
              description: ID da sala removida
            status:
              type: string
              description: Status da operação
      404:
        description: Sala não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        from flask import current_app

        rooms = current_app.config.get("active_rooms", {})

        if room_id not in rooms:
            return jsonify({"error": "Sala não encontrada"}), 404

        # Notificar usuários e remover sala
        emit("room_deleted", {"room": room_id}, room=room_id, namespace="/")
        del rooms[room_id]

        return jsonify({"room_id": room_id, "status": "deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@realtime_blueprint.route("/rooms/<room_id>/messages", methods=["GET"])
def get_room_messages(room_id: str):
    """
    Obtém mensagens de uma sala
    ---
    tags:
      - Tempo Real
    parameters:
      - name: room_id
        in: path
        type: string
        required: true
        description: ID da sala
    responses:
      200:
        description: Lista de mensagens da sala
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: string
                description: ID do usuário que enviou a mensagem
              content:
                type: string
                description: Conteúdo da mensagem
              timestamp:
                type: string
                format: date-time
                description: Data e hora do envio
      404:
        description: Sala não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        from flask import current_app

        rooms = current_app.config.get("active_rooms", {})

        if room_id not in rooms:
            return jsonify({"error": "Sala não encontrada"}), 404

        messages = rooms[room_id].get("messages", [])
        return jsonify(messages)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@realtime_blueprint.route("/rooms/<room_id>/users", methods=["GET"])
def get_room_users(room_id: str):
    """
    Obtém usuários de uma sala
    ---
    tags:
      - Tempo Real
    parameters:
      - name: room_id
        in: path
        type: string
        required: true
        description: ID da sala
    responses:
      200:
        description: Lista de usuários na sala
        schema:
          type: array
          items:
            type: object
            properties:
              user_id:
                type: string
                description: ID do usuário
              username:
                type: string
                description: Nome do usuário
              status:
                type: string
                description: Status do usuário (online/offline)
      404:
        description: Sala não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
      500:
        description: Erro interno do servidor
        schema:
          type: object
          properties:
            error:
              type: string
    """
    try:
        from flask import current_app

        rooms = current_app.config.get("active_rooms", {})

        if room_id not in rooms:
            return jsonify({"error": "Sala não encontrada"}), 404

        users = rooms[room_id].get("users", [])
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
