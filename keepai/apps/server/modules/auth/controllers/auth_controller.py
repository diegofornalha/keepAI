from flask import Blueprint, jsonify, request
from flasgger import swag_from

from ..middleware.auth_middleware import auth_required, clerk, current_user

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/webhook", methods=["POST"])
def webhook():
    """
    Webhook para eventos do Clerk
    ---
    tags:
      - Autenticação
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - type
            - data
          properties:
            type:
              type: string
              description: Tipo do evento (user.created, user.updated, user.deleted)
            data:
              type: object
              description: Dados do evento
    responses:
      200:
        description: Evento processado com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
            message:
              type: string
      400:
        description: Payload inválido
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
        event_type = request.json.get("type")
        data = request.json.get("data")

        if not event_type or not data:
            return jsonify({"error": "Invalid webhook payload"}), 400

        result = clerk.handle_webhook(event_type, data)

        if not result["success"]:
            return jsonify({"error": result["error"]}), 400

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/me", methods=["GET"])
@auth_required
def me():
    """
    Retorna informações do usuário autenticado
    ---
    tags:
      - Autenticação
    security:
      - Bearer: []
    responses:
      200:
        description: Informações do usuário
        schema:
          type: object
          properties:
            user:
              type: object
              properties:
                id:
                  type: string
                email:
                  type: string
                first_name:
                  type: string
                last_name:
                  type: string
      401:
        description: Não autorizado
        schema:
          type: object
          properties:
            error:
              type: string
      404:
        description: Usuário não encontrado
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
        user = current_user()
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"user": user}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
