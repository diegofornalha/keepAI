from functools import wraps

from flask import g, jsonify, request

from ..services.auth_service import AuthService

clerk = AuthService()


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error": "No authorization header"}), 401

        try:
            token = auth_header.split(" ")[1]
            result = clerk.verify_token(token)

            if not result["success"]:
                return jsonify({"error": result["error"]}), 401

            user_result = clerk.get_user(result["user_id"])
            if not user_result["success"]:
                return jsonify({"error": user_result["error"]}), 401

            g.user = user_result["user"]
            g.user_id = result["user_id"]
            g.session_id = result["session_id"]

            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 401

    return decorated


def current_user():
    return g.user if hasattr(g, "user") else None


def role_required(roles):
    """Decorator para verificar roles do usuário"""

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = get_current_user()
            if not user:
                return (
                    jsonify(
                        {
                            "error": "Não autorizado",
                            "message": "Você precisa estar autenticado para acessar este recurso",
                        }
                    ),
                    401,
                )

            user_roles = user.get("public_metadata", {}).get("roles", [])
            if not any(role in user_roles for role in roles):
                return (
                    jsonify(
                        {
                            "error": "Acesso negado",
                            "message": "Você não tem permissão para acessar este recurso",
                        }
                    ),
                    403,
                )

            return f(*args, **kwargs)

        return decorated

    return decorator
