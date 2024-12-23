from typing import Optional
import os
from dataclasses import dataclass
from supabase import create_client, Client


@dataclass
class Settings:
    """Configurações do projeto"""

    _PROJECT_NAME: str = "KeepAI"
    _VERSION: str = "0.1.0"
    _SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    _SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    _GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    @property
    def PROJECT_NAME(self) -> str:
        return self._PROJECT_NAME

    @property
    def VERSION(self) -> str:
        return self._VERSION

    @property
    def SUPABASE_URL(self) -> Optional[str]:
        return self._SUPABASE_URL

    @property
    def SUPABASE_KEY(self) -> Optional[str]:
        return self._SUPABASE_KEY

    @property
    def GEMINI_API_KEY(self) -> Optional[str]:
        return self._GEMINI_API_KEY

    def get_supabase_client(self) -> Client:
        """Retorna um cliente Supabase configurado"""
        if not self._SUPABASE_URL or not self._SUPABASE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
        return create_client(self._SUPABASE_URL, self._SUPABASE_KEY)


settings = Settings()
