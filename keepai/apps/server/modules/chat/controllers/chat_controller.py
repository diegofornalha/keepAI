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
from flasgger import swag_from

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
    """
    Lista todas as sessões de chat do usuário
    ---
    tags:
      - Chat
    security:
      - Bearer: []
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
    responses:
      200:
        description: Lista de sessões de chat
        schema:
          type: object
          properties:
            chats:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: string
                  user_id:
                    type: string
                  title:
                    type: string
                  created_at:
                    type: string
                    format: date-time
                  updated_at:
                    type: string
                    format: date-time
            total:
              type: integer
            page:
              type: integer
            per_page:
              type: integer
      401:
        description: Não autorizado
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Cria uma nova sessão de chat
    ---
    tags:
      - Chat
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - user_id
          properties:
            user_id:
              type: string
              description: ID do usuário
            title:
              type: string
              description: Título da sessão
    responses:
      201:
        description: Sessão criada com sucesso
        schema:
          type: object
          properties:
            id:
              type: string
            user_id:
              type: string
            title:
              type: string
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time
      400:
        description: Dados inválidos
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Retorna uma sessão específica
    ---
    tags:
      - Chat
    security:
      - Bearer: []
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: ID da sessão
    responses:
      200:
        description: Sessão encontrada
        schema:
          type: object
          properties:
            id:
              type: string
            user_id:
              type: string
            title:
              type: string
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time
      401:
        description: Não autorizado
        schema:
          type: object
          properties:
            error:
              type: string
      403:
        description: Acesso negado
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Sessão não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Atualiza uma sessão de chat
    ---
    tags:
      - Chat
    security:
      - Bearer: []
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: ID da sessão
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              description: Novo título da sessão
    responses:
      200:
        description: Sessão atualizada com sucesso
        schema:
          type: object
          properties:
            id:
              type: string
            user_id:
              type: string
            title:
              type: string
            created_at:
              type: string
              format: date-time
            updated_at:
              type: string
              format: date-time
      401:
        description: Não autorizado
        schema:
          type: object
          properties:
            error:
              type: string
      403:
        description: Acesso negado
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Sessão não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Remove uma sessão de chat
    ---
    tags:
      - Chat
    security:
      - Bearer: []
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: ID da sessão
    responses:
      204:
        description: Sessão removida com sucesso
      401:
        description: Não autorizado
        schema:
          type: object
          properties:
            error:
              type: string
      403:
        description: Acesso negado
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Sessão não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    Lista todas as mensagens de uma sessão
    ---
    tags:
      - Chat
    security:
      - Bearer: []
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: ID da sessão
      - name: page
        in: query
        type: integer
        default: 1
        description: Número da página
      - name: per_page
        in: query
        type: integer
        default: 50
        description: Itens por página
    responses:
      200:
        description: Lista de mensagens
        schema:
          type: object
          properties:
            messages:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  chat_id:
                    type: string
                  user_id:
                    type: string
                  role:
                    type: string
                    enum: [user, assistant]
                  content:
                    type: string
                  status:
                    type: string
                    enum: [pending, sent, delivered, read]
                  created_at:
                    type: string
                    format: date-time
            total:
              type: integer
            chat_id:
              type: string
            page:
              type: integer
            per_page:
              type: integer
      401:
        description: Não autorizado
        schema:
          type: object
          properties:
            error:
              type: string
      403:
        description: Acesso negado
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Sessão não encontrada
        schema:
          type: object
          properties:
            error:
              type: string
    """
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
    """
    WebSocket para chat em tempo real
    ---
    tags:
      - Chat
    security:
      - Bearer: []
    parameters:
      - name: session_id
        in: path
        type: string
        required: true
        description: ID da sessão
    responses:
      101:
        description: Conexão WebSocket estabelecida
      401:
        description: Não autorizado
      403:
        description: Acesso negado
      404:
        description: Sessão não encontrada
    """
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
