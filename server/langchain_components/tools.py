from typing import List
from langchain.tools import Tool
from langchain.agents import AgentType, AgentExecutor, initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from server.config.settings import settings


def get_tools() -> List[Tool]:
    """Retorna a lista de ferramentas disponíveis"""
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


def get_agent() -> AgentExecutor:
    """Retorna um agente configurado com as ferramentas"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        api_key=SecretStr(settings.GEMINI_API_KEY or ""),
        temperature=0.7,
    )

    tools = get_tools()

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
