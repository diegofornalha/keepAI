from typing import List
from langchain.tools import Tool
from langchain.agents import AgentType, AgentExecutor, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from server.config.settings import settings
import logging
from google.generativeai import configure, GenerativeModel
from google.ai import generativelanguage as glm

logger = logging.getLogger(__name__)


def get_tools() -> List[Tool]:
    """Retorna a lista de ferramentas disponíveis para o agente."""
    try:
        return [
            Tool(
                name="search",
                func=lambda x: "Resultados da busca",
                description="Realiza uma busca na base de conhecimento",
            ),
            Tool(
                name="create_note",
                func=lambda x: "Nota criada com sucesso",
                description="Cria uma nova nota",
            ),
        ]
    except Exception as e:
        logger.error(f"Erro ao carregar ferramentas: {str(e)}")
        raise RuntimeError("Falha ao carregar ferramentas")


def get_agent() -> AgentExecutor:
    """Retorna um agente configurado com as ferramentas e configurações otimizadas."""
    try:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não está configurada")

        configure(api_key=settings.GEMINI_API_KEY)
        model = GenerativeModel(
            model_name="gemini-pro",
            generation_config=glm.GenerationConfig(
                temperature=0.7,
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
            ),
            safety_settings=[
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE",
                },
            ],
        )

        llm = ChatGoogleGenerativeAI(
            model=model,
            convert_system_message_to_human=True,
        )

        tools = get_tools()

        return initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5,
            early_stopping_method="generate",
        )
    except Exception as e:
        logger.error(f"Erro ao inicializar o agente: {str(e)}")
        raise RuntimeError("Falha ao inicializar o agente")
