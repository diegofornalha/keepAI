from flask import Blueprint, render_template, jsonify, request, Response
from functools import wraps
from typing import Callable, Any
from server.models.user import User

main_bp = Blueprint("main", __name__)


def clerk_auth_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated_function(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Unauthorized"}), 401

        # TODO: Validar o token JWT do Clerk e obter os dados do usuário
        # Por enquanto, usando um usuário de teste
        test_user = User(id=1, name="Usuário Teste", email="teste@example.com")
        return f(*args, current_user=test_user, **kwargs)

    return decorated_function


@main_bp.route("/")
def index() -> str:
    # Por enquanto, usando um usuário de teste
    test_user = User(id=1, name="Usuário Teste", email="teste@example.com")
    return render_template("index.html", current_user=test_user)


@main_bp.route("/health")
def health() -> tuple[Response, int]:
    return jsonify({"status": "healthy", "version": "0.1.0"}), 200


@main_bp.route("/notes")
@clerk_auth_required
def notes(current_user: User) -> str:
    return render_template("notes.html", current_user=current_user)


@main_bp.route("/tasks")
@clerk_auth_required
def tasks(current_user: User) -> str:
    return render_template("tasks.html", current_user=current_user)


@main_bp.route("/calendar")
@clerk_auth_required
def calendar(current_user: User) -> str:
    return render_template("calendar.html", current_user=current_user)


@main_bp.route("/settings")
@clerk_auth_required
def settings(current_user: User) -> str:
    return render_template("settings.html", current_user=current_user)
