from .clerk import auth_bp
from .decorators import require_auth
from flask import request
from typing import Optional


def get_current_user() -> Optional[str]:
    """Retorna o ID do usuário atual se autenticado"""
    return getattr(request, "user_id", None)


__all__ = ["auth_bp", "require_auth", "get_current_user"]
