from functools import wraps
from flask import request, jsonify, current_app
import time
import re
from datetime import datetime, timedelta
import hashlib
import secrets
import logging

logger = logging.getLogger("security")


class SecurityConfig:
    # Configurações de Rate Limiting
    RATE_LIMIT = 60  # requisições
    RATE_WINDOW = 60  # segundos

    # Configurações de Tamanho de Payload
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB

    # Configurações de Segurança de Headers
    SECURE_HEADERS = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
        "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';",
    }

    # Lista de IPs bloqueados
    BLOCKED_IPS = set()

    # Padrões suspeitos em requisições
    SUSPICIOUS_PATTERNS = [
        r"(?i)(<script|javascript:|vbscript:|livescript:)",
        r"(?i)(onload=|onerror=|onmouseover=|onclick=|onmouseout=)",
        r"(?i)(/etc/passwd|/etc/shadow)",
        r"(?i)(SELECT.*FROM|INSERT.*INTO|UPDATE.*SET|DELETE.*FROM)",
        r"(?i)(\.\./|\.\./\./|~\/)",
    ]


class RateLimiter:
    def __init__(self, limit=60, window=60):
        self.limit = limit
        self.window = window
        self.requests = {}

    def is_allowed(self, ip):
        now = time.time()

        # Remove requisições antigas
        self.requests[ip] = [
            req for req in self.requests.get(ip, []) if req > now - self.window
        ]

        # Verifica se excedeu o limite
        if len(self.requests.get(ip, [])) >= self.limit:
            return False

        # Adiciona nova requisição
        self.requests.setdefault(ip, []).append(now)
        return True


class SecurityMiddleware:
    def __init__(self):
        self.rate_limiter = RateLimiter(
            SecurityConfig.RATE_LIMIT, SecurityConfig.RATE_WINDOW
        )

    def check_request(self, request):
        """Verifica a segurança da requisição"""
        ip = request.remote_addr

        # Verifica IP bloqueado
        if ip in SecurityConfig.BLOCKED_IPS:
            logger.warning(f"Tentativa de acesso de IP bloqueado: {ip}")
            return False, "IP bloqueado"

        # Rate limiting
        if not self.rate_limiter.is_allowed(ip):
            logger.warning(f"Rate limit excedido para IP: {ip}")
            return False, "Taxa limite excedida"

        # Verifica tamanho do conteúdo
        content_length = request.content_length or 0
        if content_length > SecurityConfig.MAX_CONTENT_LENGTH:
            logger.warning(f"Payload muito grande de {ip}: {content_length} bytes")
            return False, "Payload muito grande"

        # Verifica padrões suspeitos
        payload = str(request.get_data())
        for pattern in SecurityConfig.SUSPICIOUS_PATTERNS:
            if re.search(pattern, payload):
                logger.warning(f"Padrão suspeito detectado de {ip}: {pattern}")
                SecurityConfig.BLOCKED_IPS.add(ip)
                return False, "Conteúdo suspeito detectado"

        return True, None


def security_check(f):
    """Decorator para verificar segurança das requisições"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        middleware = SecurityMiddleware()
        is_safe, error = middleware.check_request(request)

        if not is_safe:
            return jsonify({"error": error, "status": "error"}), 403

        # Adiciona headers de segurança
        response = current_app.make_response(f(*args, **kwargs))
        for header, value in SecurityConfig.SECURE_HEADERS.items():
            response.headers[header] = value

        return response

    return decorated_function


def sanitize_input(text):
    """Sanitiza input do usuário"""
    if not isinstance(text, str):
        return text

    # Remove caracteres perigosos
    text = re.sub(r"[<>]", "", text)
    # Escapa aspas
    text = text.replace('"', "&quot;").replace("'", "&#x27;")
    return text


def generate_csrf_token():
    """Gera token CSRF"""
    return secrets.token_hex(32)


def verify_csrf_token(token):
    """Verifica token CSRF"""
    expected_token = current_app.config.get("CSRF_TOKEN")
    return secrets.compare_digest(token, expected_token)
