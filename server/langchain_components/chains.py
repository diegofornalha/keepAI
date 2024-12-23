from typing import Dict, Any
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI


class NoteChain:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=api_key
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
