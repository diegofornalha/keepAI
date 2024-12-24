from typing import Dict, Any, Union
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from server.config.settings import settings
from server.modules.notes_manager import NotesManager
import logging
from google.generativeai import configure, GenerativeModel
from google.ai import generativelanguage as glm

logger = logging.getLogger(__name__)


class KeepAIAgent:
    def __init__(self) -> None:
        """Inicializa o agente KeepAI com configurações otimizadas."""
        self.notes_manager = NotesManager()

        if not settings.GEMINI_API_KEY:
            logger.error("GEMINI_API_KEY não está configurada no ambiente")
            raise RuntimeError(
                "GEMINI_API_KEY não está configurada. "
                "Configure a variável de ambiente GEMINI_API_KEY"
            )

        try:
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
            self.llm = ChatGoogleGenerativeAI(
                model=model,
                convert_system_message_to_human=True,
            )
            logger.info("Agente KeepAI inicializado com sucesso")
        except Exception as e:
            logger.error(f"Erro ao inicializar o modelo Gemini: {str(e)}")
            raise RuntimeError(f"Falha ao inicializar o agente KeepAI: {str(e)}")

    def get_tools(self) -> list[Tool]:
        """Retorna a lista de ferramentas disponíveis para o agente."""
        # Descrições das ferramentas
        descriptions = {
            "create": "Cria uma nova nota com o conteúdo fornecido como texto.",
            "update": "Atualiza uma nota existente. Params: note_id, content.",
            "delete": "Deleta uma nota específica. Param: note_id.",
            "search": "Busca notas por conteúdo. Param: query.",
        }

        try:
            tools = [
                Tool(
                    name="create_note",
                    func=self.create_note,
                    description=descriptions["create"],
                ),
                Tool(
                    name="update_note",
                    func=self.update_note,
                    description=descriptions["update"],
                ),
                Tool(
                    name="delete_note",
                    func=self.delete_note,
                    description=descriptions["delete"],
                ),
                Tool(
                    name="search_notes",
                    func=self.search_notes,
                    description=descriptions["search"],
                ),
            ]
            return tools
        except Exception:
            logger.error("Falha ao carregar ferramentas")
            raise RuntimeError("Falha ao carregar ferramentas")

    def get_agent(self) -> AgentExecutor:
        """Retorna um agente configurado com as ferramentas"""
        tools = self.get_tools()

        # Template do prompt com instruções mais claras
        base_prompt = (
            "Você é um assistente IA amigável e prestativo do KeepAI.\n"
            "Seu objetivo é ajudar os usuários com tarefas de produtividade "
            "e organização.\n\n"
        )

        instrucoes = (
            "IMPORTANTE:\n"
            "1. Responda sempre em português do Brasil\n"
            "2. Seja conciso e direto\n"
            "3. Use emojis para tornar a conversa amigável\n"
            "4. Use apenas texto simples, não JSON\n\n"
        )

        ferramentas = (
            "Você tem acesso às seguintes ferramentas:\n\n"
            "create_note: Cria uma nova nota com texto simples\n"
            "update_note: Atualiza uma nota existente\n"
            "delete_note: Deleta uma nota específica\n"
            "search_notes: Busca notas por conteúdo\n\n"
        )

        final = (
            "Mensagem do usuário: {input}\n\n"
            "Pense cuidadosamente sobre a resposta antes de agir."
        )

        prompt_template = base_prompt + instrucoes + ferramentas + final

        prompt = PromptTemplate(template=prompt_template, input_variables=["input"])

        agent = create_react_agent(llm=self.llm, tools=tools, prompt=prompt)

        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3,
            early_stopping_method="generate",
        )

    def create_note(self, content: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Cria uma nova nota"""
        try:
            if isinstance(content, dict):
                content = str(content.get("content", ""))
            return self.notes_manager.create_note("", content)
        except Exception as e:
            return {"success": False, "error": f"Erro ao criar nota: {str(e)}"}

    def update_note(
        self, note_id: str, content: Union[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Atualiza uma nota existente"""
        try:
            if isinstance(content, dict):
                content = str(content.get("content", ""))
            return self.notes_manager.update_note(note_id, content)
        except Exception as e:
            return {"success": False, "error": f"Erro ao atualizar nota: {str(e)}"}

    def delete_note(self, note_id: str) -> Dict[str, Any]:
        """Deleta uma nota"""
        try:
            return self.notes_manager.delete_note(note_id)
        except Exception as e:
            return {"success": False, "error": f"Erro ao deletar nota: {str(e)}"}

    def search_notes(self, query: str) -> Dict[str, Any]:
        """Busca notas por conteúdo"""
        try:
            notes = self.notes_manager.get_note(query)
            return {"success": True, "notes": notes}
        except Exception as e:
            return {"success": False, "error": f"Erro ao buscar notas: {str(e)}"}
