"""
Módulo de banco de dados usando Supabase

Componentes:
- config: Configuração do banco de dados
- repositories: Repositórios de dados
"""

from .config.database import db

__all__ = ["db"]
