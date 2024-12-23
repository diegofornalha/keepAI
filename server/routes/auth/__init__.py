from flask import Blueprint, jsonify, Response, request, render_template
from server.database import supabase
from datetime import datetime
from typing import Any, Dict
import os
import requests
import jwt
from jwt import PyJWKClient

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

CLERK_API_KEY = os.getenv("CLERK_API_KEY", "")  # Valor padrão vazio para evitar None
CLERK_API_BASE = os.getenv("CLERK_API_BASE", "")
CLERK_JWKS_URL = os.getenv("CLERK_JWKS_URL", "")

# Inicializar o cliente JWKS
jwks_client = PyJWKClient(CLERK_JWKS_URL)


@auth_bp.route("/status")
def status() -> tuple[Response, int]:
    return jsonify({"status": "ok"}), 200


@auth_bp.route("/login")
def login() -> str:
    """Renderiza a página de login"""
    return render_template("auth/login.html")


@auth_bp.route("/register")
def register_page() -> str:
    """Renderiza a página de registro"""
    return render_template("auth/register.html")


def verify_token(token: str) -> Dict[str, Any]:
    """Verifica o token JWT usando JWKS"""
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        data: Dict[str, Any] = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience="your-audience",
            issuer=f"https://{os.getenv('CLERK_FRONTEND_API')}",
        )
        return data
    except Exception as e:
        raise ValueError(f"Token inválido: {str(e)}")


@auth_bp.route("/api/register", methods=["POST"])
def register() -> tuple[Response, int]:
    try:
        data = request.get_json() or {}
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email e senha são obrigatórios"}), 400

        # Criar usuário no Clerk via API
        headers = {
            "Authorization": f"Bearer {CLERK_API_KEY}",
            "Content-Type": "application/json",
        }

        clerk_response = requests.post(
            f"{CLERK_API_BASE}/users",
            headers=headers,
            json={"email_address": [{"email": email}], "password": password},
        )

        if clerk_response.status_code != 200:
            return (
                jsonify(
                    {
                        "error": "Erro ao criar usuário no Clerk",
                        "details": clerk_response.json(),
                    }
                ),
                400,
            )

        clerk_user = clerk_response.json()

        # Criar usuário no Supabase
        user_data = {
            "id": clerk_user["id"],
            "email": email,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        supabase.table("users").insert(user_data).execute()

        return (
            jsonify(
                {
                    "message": "Usuário registrado com sucesso",
                    "user_id": clerk_user["id"],
                }
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": "Erro ao registrar usuário", "details": str(e)}), 500


@auth_bp.route("/users", methods=["POST"])
def create_user() -> tuple[Response, int]:
    try:
        # Verificar o token de autenticação
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token não fornecido"}), 401

        token = auth_header.split(" ")[1]
        # Verificar o token - se inválido, levantará uma exceção
        verify_token(token)

        data = request.get_json() or {}
        clerk_user_id = data.get("clerk_user_id")
        email = data.get("email")

        if not clerk_user_id or not email:
            return jsonify({"error": "clerk_user_id e email são obrigatórios"}), 400

        # Criar usuário no Supabase
        user_data = {
            "id": clerk_user_id,
            "email": email,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }

        supabase.table("users").insert(user_data).execute()

        return (
            jsonify(
                {"message": "Usuário criado com sucesso", "user_id": clerk_user_id}
            ),
            201,
        )

    except Exception as e:
        return jsonify({"error": "Erro ao criar usuário", "details": str(e)}), 500
