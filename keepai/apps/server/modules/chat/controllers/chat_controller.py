import asyncio
import json
from http import HTTPStatus

from flask import (
    Blueprint,
    g,
    jsonify,
    request,
)
from flask_sock import Sock

from keepai.apps.server.modules.auth import (
    middleware as auth_middleware,
)
from keepai.apps.server.modules.chat import (
    schemas as chat_schemas,
    services as chat_services,
)

chat_bp = Blueprint("chat", __name__, url_prefix="/api/chat")
sock = Sock()


@chat_bp.route("/sessions", methods=["GET"])
@auth_middleware.auth_required
def get_sessions():
    """Lista todas as sessões de chat do usuário"""
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    chat_service = g.container.get_service(chat_services.ChatService)
    sessions = chat_service.get_user_sessions(
        user_id=auth_middleware.current_user.get("sub"),
        page=page,
        per_page=per_page,
    )

    return jsonify(
        chat_schemas.ChatList(
            chats=sessions,
            total=len(sessions),
            page=page,
            per_page=per_page,
        ).dict()
    )


@chat_bp.route("/sessions", methods=["POST"])
async def create_session():
    """Cria uma nova sessão de chat"""
    user_id = request.json.get("user_id")
    title = request.json.get("title")

    if not user_id:
        return jsonify({"error": "user_id é obrigatório"}), HTTPStatus.BAD_REQUEST

    chat_service = g.container.get_service(chat_services.ChatService)
    session = chat_service.create_session(user_id, title)

    return jsonify(session.dict()), HTTPStatus.CREATED


@chat_bp.route("/sessions/<session_id>", methods=["GET"])
@auth_middleware.auth_required
def get_session(session_id: str):
    """Retorna uma sessão específica"""
    chat_service = g.container.get_service(chat_services.ChatService)
    session = chat_service.get_session(session_id)

    if not session:
        return jsonify({"error": "Sessão não encontrada"}), HTTPStatus.NOT_FOUND

    if session.user_id != auth_middleware.current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), HTTPStatus.FORBIDDEN

    return jsonify(session.dict())


@chat_bp.route("/sessions/<session_id>", methods=["PUT"])
@auth_middleware.auth_required
def update_session(session_id: str):
    """Atualiza uma sessão de chat"""
    data = request.get_json()
    title = data.get("title")

    chat_service = g.container.get_service(chat_services.ChatService)
    session = chat_service.get_session(session_id)

    if not session:
        return jsonify({"error": "Sessão não encontrada"}), HTTPStatus.NOT_FOUND

    if session.user_id != auth_middleware.current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), HTTPStatus.FORBIDDEN

    updated = chat_service.update_session(session_id, title)
    return jsonify(updated.dict())


@chat_bp.route("/sessions/<session_id>", methods=["DELETE"])
@auth_middleware.auth_required
def delete_session(session_id: str):
    """Remove uma sessão de chat"""
    chat_service = g.container.get_service(chat_services.ChatService)
    session = chat_service.get_session(session_id)

    if not session:
        return jsonify({"error": "Sessão não encontrada"}), HTTPStatus.NOT_FOUND

    if session.user_id != auth_middleware.current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), HTTPStatus.FORBIDDEN

    chat_service.delete_session(session_id)
    return "", HTTPStatus.NO_CONTENT


@chat_bp.route("/sessions/<session_id>/messages", methods=["GET"])
@auth_middleware.auth_required
def get_messages(session_id: str):
    """Lista todas as mensagens de uma sessão"""
    chat_service = g.container.get_service(chat_services.ChatService)
    session = chat_service.get_session(session_id)

    if not session:
        return jsonify({"error": "Sessão não encontrada"}), HTTPStatus.NOT_FOUND

    if session.user_id != auth_middleware.current_user.get("sub"):
        return jsonify({"error": "Acesso negado"}), HTTPStatus.FORBIDDEN

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    messages = chat_service.get_chat_messages(session_id, page, per_page)

    return jsonify(
        chat_schemas.ChatMessages(
            messages=messages,
            total=len(messages),
            chat_id=session_id,
            page=page,
            per_page=per_page,
        ).dict()
    )


@sock.route("/chat/<session_id>")
@auth_middleware.auth_required
async def chat_socket(ws, session_id: str):
    """WebSocket para chat em tempo real"""
    chat_service = g.container.get_service(chat_services.ChatService)
    session = chat_service.get_session(session_id)

    if not session:
        ws.send(json.dumps({"error": "Sessão não encontrada"}))
        return

    if session.user_id != auth_middleware.current_user.get("sub"):
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
                        user_id=auth_middleware.current_user.get("sub"),
                        chat_id=session_id,
                        content=content,
                    ),
                )

                # Enviar resposta
                ws.send(json.dumps(result))
    except Exception as e:
        ws.send(json.dumps({"error": str(e)}))
