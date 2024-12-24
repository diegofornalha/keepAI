"""Módulo temporário para o agente de IA."""


class KeepAIAgent:
    """Agente temporário para testes."""

    def __init__(self) -> None:
        """Inicializa o agente."""
        pass

    def get_agent(self) -> "KeepAIAgent":
        """Retorna o agente."""
        return self

    def invoke(self, input_data: dict) -> str:
        """Processa uma mensagem."""
        return "Resposta de teste do agente"

    def get_agent_response(self, message: str) -> str:
        """Processa uma mensagem e retorna uma resposta."""
        return "Resposta de teste do agente"
