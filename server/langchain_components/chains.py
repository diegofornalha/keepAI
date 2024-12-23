from typing import Dict, Any
from pydantic import SecretStr
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI


class NoteChain:
    def __init__(self, api_key: str) -> None:
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            api_key=SecretStr(api_key),
            temperature=0.7,
        )

        self.prompt = PromptTemplate(
            input_variables=["content"],
            template="""Analise esta nota e sugira melhorias:

Nota: {content}

Por favor, forneça:
1. Um resumo conciso
2. Sugestões de melhorias na estrutura
3. Possíveis tags/categorias
4. Próximos passos recomendados""",
        )

        self.chain = LLMChain(llm=self.llm, prompt=self.prompt, verbose=True)

    def analyze_note(self, content: str) -> Dict[str, Any]:
        try:
            result = self.chain.predict(content=content)
            return {"success": True, "analysis": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
