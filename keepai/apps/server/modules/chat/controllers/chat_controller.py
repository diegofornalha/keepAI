import asyncio
import json

from flask import Blueprint, jsonify, request
from flask_sock import Sock

from ...auth.middleware.auth_middleware import auth_required, current_user
from ..schemas.chat_schema import ChatList, ChatMessages, MessageCreate
from ..services.chat_service import ChatService

chat_bp = Blueprint("chat", __name__)
sock = Sock()
chat_service = ChatService()


@chat_bp.route("/sessions", methods=["GET"])
@auth_required
def get_sessions():
    """Lista todas as sessões de chat do usuário"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    sessions = chat_service.get_user_sessions(
        user_id=current_user.get("sub"), page=page, per_page=per_page
    )

    return jsonify(
        ChatList(
            chats=sessions, total=len(sessions), page=page, per_page=per_page
        ).dict()
    )


@chat_bp.route("/sessions", methods=["POST"])
@auth_required
def create_session():
    """Cria uma nova sessão de chat"""
    data = request.get_json()
    title = data.get("title")

    session = chat_service.create_session(user_id=current_user.get("sub"), title=title)

    return jsonify(session.dict()), 201


@chat_bp.route("/sessions/<session_id>", methods=["GET"])
@auth_required
def get_session(session_id: str):
    """Retorna uma sessão específica"""
    session = chat_service.get_session(session_id)
    if not session:
        return jsonify({"error": "Sessão não encontrada"}), 404

    if session.user_id != current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), 403

    return jsonify(session.dict())


@chat_bp.route("/sessions/<session_id>", methods=["PUT"])
@auth_required
def update_session(session_id: str):
    """Atualiza uma sessão de chat"""
    data = request.get_json()
    title = data.get("title")

    session = chat_service.get_session(session_id)
    if not session:
        return jsonify({"error": "Sessão não encontrada"}), 404

    if session.user_id != current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), 403

    updated = chat_service.update_session(session_id, title)
    return jsonify(updated.dict())


@chat_bp.route("/sessions/<session_id>", methods=["DELETE"])
@auth_required
def delete_session(session_id: str):
    """Remove uma sessão de chat"""
    session = chat_service.get_session(session_id)
    if not session:
        return jsonify({"error": "Sessão não encontrada"}), 404

    if session.user_id != current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), 403

    chat_service.delete_session(session_id)
    return "", 204


@chat_bp.route("/sessions/<session_id>/messages", methods=["GET"])
@auth_required
def get_messages(session_id: str):
    """Lista todas as mensagens de uma sessão"""
    session = chat_service.get_session(session_id)
    if not session:
        return jsonify({"error": "Sessão não encontrada"}), 404

    if session.user_id != current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), 403

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    messages = chat_service.get_chat_messages(session_id, page, per_page)

    return jsonify(
        ChatMessages(
            messages=messages,
            total=len(messages),
            chat_id=session_id,
            page=page,
            per_page=per_page,
        ).dict()
    )


@sock.route("/chat/<session_id>")
@auth_required
async def chat_socket(ws, session_id: str):
    """WebSocket para chat em tempo real"""
    session = chat_service.get_session(session_id)
    if not session:
        ws.send(json.dumps({"error": "Sessão não encontrada"}))
        return

    if session.user_id != current_user.get("sub"):
        ws.send(json.dumps({"error": "Acesso negado"}))
        return

    def on_update(payload):
        """Callback para atualizações em tempo real"""
        ws.send(json.dumps(payload))

    # Inscrever para atualizações
    chat_service.subscribe_to_updates(session_id, on_update)

    try:
        while True:
            data = json.loads(ws.receive())
            content = data.get("content")

            if content:
                # Processar mensagem de forma assíncrona
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: chat_service.send_message(
                        user_id=current_user.get("sub"),
                        chat_id=session_id,
                        content=content,
                    ),
                )

                # Enviar resposta
                ws.send(json.dumps(result))
    except Exception as e:
        ws.send(json.dumps({"error": str(e)}))
