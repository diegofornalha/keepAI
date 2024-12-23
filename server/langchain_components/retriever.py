from typing import Dict, Any
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


class DocumentRetriever:
    def __init__(self, api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        self.vectorstore = None

    def create_vectorstore(self, texts: list[str]) -> Dict[str, Any]:
        try:
            self.vectorstore = FAISS.from_texts(texts, self.embeddings)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def search(self, query: str, k: int = 4) -> Dict[str, Any]:
        try:
            if not self.vectorstore:
                return {"success": False, "error": "Vectorstore não inicializado"}

            results = self.vectorstore.similarity_search(query, k=k)
            return {"success": True, "results": results}
        except Exception as e:
            return {"success": False, "error": str(e)}
