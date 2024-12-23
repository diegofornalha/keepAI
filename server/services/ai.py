import google.generativeai as genai  # type: ignore
from flask import current_app
from typing import Any


def setup_gemini() -> None:
    """Configura o cliente do Google Gemini."""
    api_key = current_app.config.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY não configurada")

    genai.configure(api_key=api_key)


def get_gemini_model() -> Any:
    """Retorna uma instância do modelo Gemini."""
    try:
        setup_gemini()
        return genai.GenerativeModel("gemini-pro")
    except Exception as e:
        current_app.logger.error(f"Erro ao configurar Gemini: {e}")
        raise


def process_chat_message(message: str) -> str:
    """
    Processa uma mensagem do usuário usando o Google Gemini.

    Args:
        message: A mensagem do usuário.

    Returns:
        A resposta do modelo.
    """
    try:
        model = get_gemini_model()

        # Configurar o contexto do sistema
        system_prompt = """Você é um assistente IA amigável e prestativo do KeepAI.
        Você deve:
        1. Responder em português do Brasil
        2. Ser conciso e direto
        3. Usar emojis ocasionalmente para tornar a conversa mais amigável
        4. Formatar código usando blocos de código Markdown (```)
        5. Ajudar com tarefas de produtividade, organização e programação
        """

        # Gerar a resposta
        response = model.generate_content(
            [
                {"role": "user", "parts": [system_prompt]},
                {"role": "user", "parts": [message]},
            ]
        )

        return str(response.text)

    except Exception as e:
        current_app.logger.error(f"Erro ao processar mensagem: {e}")
        raise ValueError(
            "Não foi possível processar sua mensagem. Por favor, tente novamente."
        )
