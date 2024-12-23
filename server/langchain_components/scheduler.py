from langchain.agents import AgentType, AgentExecutor, initialize_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from server.config.settings import settings


def get_scheduler_agent() -> AgentExecutor:
    """Retorna um agente para agendamento de tarefas"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        api_key=SecretStr(settings.GEMINI_API_KEY or ""),
        temperature=0.7,
    )

    tools = [
        Tool(
            name="calendar",
            func=lambda x: "Evento agendado com sucesso",
            description="Agenda um evento no calendário",
        )
    ]

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )
