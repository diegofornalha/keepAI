from typing import Optional
import os
from dataclasses import dataclass
from supabase import create_client, Client
import logging


# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log"),
    ],
)

logger = logging.getLogger(__name__)


@dataclass
class Settings:
    """Configurações do projeto"""

    _PROJECT_NAME: str = "KeepAI"
    _VERSION: str = "0.1.0"
    _SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    _SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    _GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")

    # Configurações do Gemini
    GEMINI_CONFIG = {
        "model": "gemini-pro",
        "temperature": 0.7,
        "max_output_tokens": 2048,
        "top_p": 0.8,
        "top_k": 40,
        "safety_settings": {
            "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
        },
        "generation_config": {
            "candidate_count": 1,
            "stop_sequences": ["Human:", "Assistant:"],
        },
    }

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
        if not self._GEMINI_API_KEY:
            logger.warning("GEMINI_API_KEY não está configurada")
        return self._GEMINI_API_KEY

    def get_supabase_client(self) -> Client:
        """Retorna um cliente Supabase configurado"""
        if not self._SUPABASE_URL or not self._SUPABASE_KEY:
            logger.error("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar configurados")
        return create_client(self._SUPABASE_URL, self._SUPABASE_KEY)


settings = Settings()
