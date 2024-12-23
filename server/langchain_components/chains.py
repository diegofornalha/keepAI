from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Dict, Any
import json
import os

class NoteProcessingChain:
    def __init__(self):
        google_api_key = os.getenv('GOOGLE_API_KEY')
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada nas variáveis de ambiente")
            
        self.llm = ChatGoogleGenerativeAI(
            temperature=0,
            model="gemini-pro",
            google_api_key=google_api_key,
            convert_system_message_to_human=True
        )
        
        self.prompt = PromptTemplate(
            input_variables=["note_content"],
            template="""
            Analise esta nota e extraia:
            1. Principais tópicos
            2. Palavras-chave
            3. Ações necessárias
            4. Resumo conciso
            5. Prioridade (Alta/Média/Baixa)
            
            Nota: {note_content}
            
            Retorne apenas o JSON no seguinte formato, sem texto adicional:
            {
                "topics": [],
                "keywords": [],
                "actions": [],
                "summary": "",
                "priority": ""
            }
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    async def process(self, note_content: str) -> Dict[str, Any]:
        try:
            result = await self.chain.arun(note_content=note_content)
            # Tenta converter a string em JSON
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                # Se falhar ao converter para JSON, retorna um formato padrão
                return {
                    "error": "Erro ao processar JSON",
                    "topics": [],
                    "keywords": [],
                    "actions": [],
                    "summary": "Erro ao processar nota",
                    "priority": "Média"
                }
        except Exception as e:
            return {
                "error": str(e),
                "topics": [],
                "keywords": [],
                "actions": [],
                "summary": "Erro ao processar nota",
                "priority": "Média"
            }