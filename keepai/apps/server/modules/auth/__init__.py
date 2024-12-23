"""
Módulo de autenticação usando Clerk

Componentes:
- controllers: Rotas e endpoints
- services: Lógica de autenticação
- schemas: Validação de dados
- middleware: Proteção de rotas
"""

from .controllers.auth_controller import auth_bp
from .middleware.auth_middleware import auth_required, current_user
from .services.auth_service import AuthService

__all__ = ["auth_bp", "AuthService", "auth_required", "current_user"]
