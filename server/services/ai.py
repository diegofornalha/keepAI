from server.modules.agent import KeepAIAgent

# Instância global do agente
agent = KeepAIAgent()


def process_chat_message(message: str) -> str:
    """
    Processa uma mensagem do usuário usando o agente do LangChain.

    Args:
        message: A mensagem do usuário.

    Returns:
        A resposta do agente.
    """
    try:
        # Adiciona o contexto do sistema à mensagem
        system_prompt = """Você é um assistente IA amigável e prestativo do KeepAI.
        Você deve:
        1. Responder em português do Brasil
        2. Ser conciso e direto
        3. Usar emojis ocasionalmente para tornar a conversa mais amigável
        4. Formatar código usando blocos de código Markdown (```)
        5. Ajudar com tarefas de produtividade, organização e programação
        """

        full_message = f"{system_prompt}\n\nUsuário: {message}"

        # Usa o agente para processar a mensagem
        response = agent.get_agent().run(full_message)
        return str(response)

    except (ValueError, RuntimeError, Exception) as error:
        raise ValueError(
            "Não foi possível processar sua mensagem. Por favor, tente novamente."
        ) from error
