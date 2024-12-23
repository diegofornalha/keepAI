from typing import Dict, Any
from langchain.agents import AgentType, AgentExecutor, initialize_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr
from server.config.settings import settings
from server.modules.notes_manager import NotesManager


class KeepAIAgent:
    def __init__(self) -> None:
        self.notes_manager = NotesManager()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            api_key=SecretStr(settings.GEMINI_API_KEY or ""),
            temperature=0.7,
        )

    def get_tools(self) -> list[Tool]:
        """Retorna a lista de ferramentas disponíveis"""
        return [
            Tool(
                name="create_note",
                func=self.create_note,
                description="Cria uma nova nota",
            ),
            Tool(
                name="update_note",
                func=self.update_note,
                description="Atualiza uma nota existente",
            ),
            Tool(
                name="delete_note",
                func=self.delete_note,
                description="Deleta uma nota",
            ),
            Tool(
                name="search_notes",
                func=self.search_notes,
                description="Busca notas por conteúdo",
            ),
        ]

    def get_agent(self) -> AgentExecutor:
        """Retorna um agente configurado com as ferramentas"""
        tools = self.get_tools()
        return initialize_agent(
            tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )

    def create_note(self, content: str) -> Dict[str, Any]:
        """Cria uma nova nota"""
        return self.notes_manager.create_note("", content)

    def update_note(self, note_id: str, content: str) -> Dict[str, Any]:
        """Atualiza uma nota existente"""
        return self.notes_manager.update_note(note_id, content)

    def delete_note(self, note_id: str) -> Dict[str, Any]:
        """Deleta uma nota"""
        return self.notes_manager.delete_note(note_id)

    def search_notes(self, query: str) -> Dict[str, Any]:
        """Busca notas por conteúdo"""
        notes = self.notes_manager.get_note(query)
        return {"success": True, "notes": notes}
