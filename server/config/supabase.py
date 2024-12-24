"""Configuração do cliente Supabase."""
from typing import Optional
from supabase import create_client, Client
from server.config.settings import settings
import logging

logger = logging.getLogger(__name__)


def get_supabase_client() -> Optional[Client]:
    """
    Cria e retorna um cliente Supabase configurado.

    Returns:
        Optional[Client]: Cliente Supabase configurado ou None se houver erro
    """
    try:
        client = create_client(
            supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY
        )
        return client
    except Exception as e:
        logger.error(f"Erro ao criar cliente Supabase: {str(e)}")
        return None
