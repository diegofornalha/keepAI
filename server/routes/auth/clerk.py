from flask import Blueprint, jsonify, request
from server.database import supabase
from datetime import datetime
import os
import jwt
import requests

auth_bp = Blueprint("auth", __name__)

# Configuração do Clerk
CLERK_JWT_KEY = os.getenv("CLERK_JWT_KEY")
CLERK_API_KEY = os.getenv("CLERK_API_KEY")
CLERK_FRONTEND_API = os.getenv("CLERK_FRONTEND_API")


def get_jwks():
    """Busca as chaves públicas do Clerk"""
    url = f"https://{CLERK_FRONTEND_API}/.well-known/jwks.json"
    response = requests.get(url)
    return response.json()


@auth_bp.route("/verify", methods=["POST"])
def verify_token():
    """Verifica o token JWT do Clerk"""
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

        # Buscar ou criar usuário no Supabase
        user_id = decoded.get("sub")
        response = supabase.table("users").select("*").eq("id", user_id).execute()

        if not response.data:
            # Criar novo usuário
            user_data = {
                "id": user_id,
                "email": decoded.get("email"),
                "name": decoded.get("name", ""),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
            supabase.table("users").insert(user_data).execute()

        return jsonify({"message": "Token válido", "user_id": user_id})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 401


@auth_bp.route("/user", methods=["GET"])
def get_user():
    """Retorna os dados do usuário atual"""
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

        # Buscar usuário no Supabase
        user_id = decoded.get("sub")
        response = supabase.table("users").select("*").eq("id", user_id).execute()

        if not response.data:
            return jsonify({"message": "Usuário não encontrado"}), 404

        return jsonify(response.data[0])
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Token inválido"}), 401
