from typing import Dict, Any
from ..services.agent_service import AgentService


class AgentController:
    def __init__(self, agent_service: AgentService):
        self.agent_service = agent_service

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analisa texto usando o serviço de IA

        Args:
            text (str): Texto para análise

        Returns:
            Dict[str, Any]: Resultado da análise
        """
        return self.agent_service.analyze_text(text)

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """
        Gera conteúdo usando o serviço de IA

        Args:
            prompt (str): Prompt para geração

        Returns:
            Dict[str, Any]: Conteúdo gerado
        """
        return self.agent_service.generate_content(prompt)

    def summarize_text(self, text: str) -> Dict[str, Any]:
        """
        Sumariza texto usando o serviço de IA

        Args:
            text (str): Texto para sumarização

        Returns:
            Dict[str, Any]: Resumo do texto
        """
        return self.agent_service.summarize_text(text)
