import asyncio
import json
import logging
import os
from typing import Any, Dict, List

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from ..config.langchain_config import get_callback_manager


class AutonomousNote:
    def __init__(self):
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")

        callback_manager = get_callback_manager()

        self.llm = ChatGoogleGenerativeAI(
            temperature=0,
            model="gemini-pro",
            google_api_key=google_api_key,
            convert_system_message_to_human=True,
            callback_manager=callback_manager,
        )

        self.prompt = PromptTemplate(
            input_variables=["content"],
            template="""Analise esta nota e determine as ações apropriadas.

Nota: {content}

Retorne apenas o JSON no seguinte formato, sem texto adicional:
{
    "analysis": {
        "type": "string",
        "priority": "high|medium|low",
        "due_date": "YYYY-MM-DD",
        "tags": ["tag1", "tag2"]
    },
    "actions": [
        {
            "type": "reminder|task|notification",
            "description": "string",
            "schedule": "YYYY-MM-DD HH:MM",
            "priority": "high|medium|low"
        }
    ]
}""",
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True)

    async def process_note(self, content: str) -> Dict[str, Any]:
        """Processa uma nota e executa ações automatizadas"""
        try:
            # Garante que estamos usando o loop de eventos correto
            loop = asyncio.get_event_loop()

            # Executa a chamada ao modelo no loop atual
            result = await loop.run_in_executor(
                None, lambda: self.chain.predict(content=content)
            )

            # Garante que o resultado é um JSON válido
            try:
                actions = json.loads(result)
            except json.JSONDecodeError:
                # Se não for um JSON válido, cria uma estrutura padrão
                actions = {
                    "analysis": {
                        "type": "note",
                        "priority": "medium",
                        "due_date": None,
                        "tags": [],
                    },
                    "actions": [],
                }

            # Executa ações automatizadas
            executed_actions = []
            for action in actions.get("actions", []):
                execution_result = await self._execute_action(action)
                executed_actions.append(
                    {"type": action.get("type", "unknown"), "result": execution_result}
                )

            return {
                "content": content,
                "analysis": actions.get("analysis", {}),
                "executed_actions": executed_actions,
            }

        except Exception as e:
            logging.error(f"Erro ao processar nota: {str(e)}")
            return {
                "content": content,
                "analysis": {
                    "type": "note",
                    "priority": "medium",
                    "due_date": None,
                    "tags": [],
                },
                "executed_actions": [],
                "error": str(e),
            }

    async def _execute_action(self, action: dict) -> str:
        """Executa uma ação específica"""
        try:
            action_type = action.get("type", "").lower()
            if action_type == "reminder":
                return await self._create_reminder(action)
            elif action_type == "task":
                return await self._create_task(action)
            elif action_type == "notification":
                return await self._send_notification(action)
            else:
                return "Ação processada com sucesso"
        except Exception as e:
            return f"Erro ao executar ação: {str(e)}"

    async def _create_reminder(self, action: dict) -> str:
        return "Lembrete criado"

    async def _create_task(self, action: dict) -> str:
        return "Tarefa criada"

    async def _send_notification(self, action: dict) -> str:
        return "Notificação enviada"
