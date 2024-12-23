from typing import Dict, Any
import google.generativeai as genai
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os


class AgentService:
    def __init__(self):
        # Configurar Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel("gemini-pro")

        # Configurar memória
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analisa texto usando IA"""
        try:
            response = self.model.generate_content(
                f"""Analise o seguinte texto e forneça insights relevantes:
                {text}
                
                Forneça a análise no seguinte formato:
                - Principais pontos
                - Sentimento
                - Sugestões
                """
            )

            return {
                "success": True,
                "analysis": response.text,
                "metadata": {"model": "gemini-pro", "type": "analysis"},
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_content(self, prompt: str) -> Dict[str, Any]:
        """Gera conteúdo usando IA"""
        try:
            response = self.model.generate_content(prompt)

            return {
                "success": True,
                "content": response.text,
                "metadata": {"model": "gemini-pro", "type": "generation"},
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def summarize_text(self, text: str) -> Dict[str, Any]:
        """Sumariza texto usando IA"""
        try:
            response = self.model.generate_content(
                f"""Faça um resumo conciso do seguinte texto:
                {text}
                
                Forneça o resumo em tópicos principais.
                """
            )

            return {
                "success": True,
                "summary": response.text,
                "metadata": {"model": "gemini-pro", "type": "summary"},
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
