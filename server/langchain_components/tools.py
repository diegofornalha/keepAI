from langchain.agents import initialize_agent, Tool
from langchain.tools import BaseTool
from typing import Optional, List
from supabase import create_client
import os


class SearchNoteDatabase(BaseTool):
    name = "search_notes"
    description = "Busca notas relacionadas no banco de dados"

    def __init__(self):
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        )

    def _run(self, query: str) -> List[dict]:
        try:
            result = (
                self.supabase.table("notes")
                .select("*")
                .textSearch("content", query)
                .execute()
            )
            return result.data
        except Exception as e:
            return f"Erro na busca: {str(e)}"


class CreateNoteTool(BaseTool):
    name = "create_note"
    description = "Cria uma nova nota com conteúdo estruturado"

    def __init__(self):
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY")
        )

    def _run(self, content: dict) -> str:
        try:
            result = self.supabase.table("notes").insert(content).execute()
            return f"Nota criada com ID: {result.data[0]['id']}"
        except Exception as e:
            return f"Erro ao criar nota: {str(e)}"


def setup_note_agent(llm):
    tools = [SearchNoteDatabase(), CreateNoteTool()]

    return initialize_agent(
        tools, llm, agent="chat-conversational-react-description", verbose=True
    )
