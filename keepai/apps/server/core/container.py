from typing import Dict, Type

from flask import Flask

from keepai.apps.server.config.settings import Settings
from keepai.apps.server.database.config.supabase import SupabaseClient, get_supabase
from keepai.apps.server.modules.chat.services.chat_service import ChatService
from keepai.apps.server.modules.chat.repositories.chat_repository import ChatRepository


class Container:
    """Container de injeção de dependências"""

    def __init__(self, app: Flask):
        """Inicializa o container com a aplicação Flask

        Args:
            app: Aplicação Flask
        """
        self.app = app
        self._settings = None
        self._supabase = None
        self._repositories = {}
        self._services = {}

    @property
    def settings(self) -> Settings:
        """Retorna as configurações da aplicação"""
        if self._settings is None:
            self._settings = Settings()
        return self._settings

    @property
    def supabase(self) -> SupabaseClient:
        """Retorna o cliente Supabase"""
        if self._supabase is None:
            self._supabase = get_supabase()
        return self._supabase

    def get_repository(self, repository_class: Type) -> any:
        """Retorna uma instância do repositório

        Args:
            repository_class: Classe do repositório

        Returns:
            Instância do repositório
        """
        if repository_class not in self._repositories:
            self._repositories[repository_class] = repository_class(self.supabase)
        return self._repositories[repository_class]

    def get_service(self, service_class: Type) -> any:
        """Retorna uma instância do serviço

        Args:
            service_class: Classe do serviço

        Returns:
            Instância do serviço
        """
        if service_class not in self._services:
            if service_class == ChatService:
                repository = self.get_repository(ChatRepository)
                self._services[service_class] = service_class(repository=repository)
            else:
                self._services[service_class] = service_class()
        return self._services[service_class]
