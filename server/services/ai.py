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
        # Usa o agente para processar a mensagem
        response = agent.get_agent().invoke({"input": message})

        # Verifica se a resposta é válida
        if not response or not isinstance(response, (str, dict)):
            raise ValueError("Resposta inválida do agente")

        # Extrai a resposta do resultado
        if isinstance(response, dict):
            response = response.get("output", "")

        return str(response)

    except Exception as error:
        error_msg = str(error)
        if "safety" in error_msg.lower():
            return (
                "Desculpe, não posso processar esse tipo de conteúdo "
                "por questões de segurança. 🚫"
            )
        elif "quota" in error_msg.lower() or "rate" in error_msg.lower():
            return (
                "Desculpe, estou temporariamente indisponível devido a limites de uso. "
                "Por favor, tente novamente em alguns minutos. ⏳"
            )
        else:
            return (
                "Desculpe, ocorreu um erro ao processar sua mensagem. "
                "Por favor, tente novamente ou reformule sua pergunta. 🔄"
            )
