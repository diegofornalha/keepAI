from functools import wraps
from flask import request, jsonify
import jwt
import os

# Configuração do Clerk
CLERK_JWT_KEY = os.getenv("CLERK_JWT_KEY")
CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"message": "Token não fornecido"}), 401

        try:
            # Remover o prefixo 'Bearer ' se presente
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            else:
                token = auth_header

            # Verificar o token com a chave pública do Clerk
            decoded = jwt.decode(
                token,
                CLERK_JWT_KEY,
                algorithms=["RS256"],
                audience="your-audience",  # Configure conforme sua aplicação Clerk
                issuer=f"https://{CLERK_FRONTEND_API}",
            )

            # Adicionar o user_id ao request para uso nas rotas
            request.user_id = decoded.get("sub")
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

    return decorated
