"""Módulo de configuração do servidor."""

from .settings import (
    APP_NAME,
    APP_VERSION,
    DEBUG,
    SECRET_KEY,
    SUPABASE_URL,
    SUPABASE_KEY,
    GEMINI_API_KEY,
    LOG_LEVEL,
    LOG_FORMAT,
    LOG_DIR,
    CORS_ORIGINS,
    CORS_METHODS,
    CORS_HEADERS,
    CACHE_TYPE,
    CACHE_REDIS_URL,
    RATELIMIT_DEFAULT,
    RATELIMIT_STORAGE_URL,
)
from .database import supabase_client
from .logging_config import logger, setup_logging

__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "DEBUG",
    "SECRET_KEY",
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "GEMINI_API_KEY",
    "LOG_LEVEL",
    "LOG_FORMAT",
    "LOG_DIR",
    "CORS_ORIGINS",
    "CORS_METHODS",
    "CORS_HEADERS",
    "CACHE_TYPE",
    "CACHE_REDIS_URL",
    "RATELIMIT_DEFAULT",
    "RATELIMIT_STORAGE_URL",
    "supabase_client",
    "logger",
    "setup_logging",
]
