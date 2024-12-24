"""Módulo de configuração do servidor."""

from config.settings import settings
from config.database import supabase

__all__ = ["settings", "supabase"]
