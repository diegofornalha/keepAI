from typing import Dict, Any
from langchain.embeddings import OpenAIEmbeddings


class EmbeddingGenerator:
    def __init__(self, api_key: str):
        self.embeddings = OpenAIEmbeddings(openai_api_key=api_key)

    def generate_embeddings(self, text: str) -> Dict[str, Any]:
        try:
            embedding = self.embeddings.embed_query(text)
            return {"success": True, "embedding": embedding}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def generate_batch_embeddings(self, texts: list[str]) -> Dict[str, Any]:
        try:
            embeddings = self.embeddings.embed_documents(texts)
            return {"success": True, "embeddings": embeddings}
        except Exception as e:
            return {"success": False, "error": str(e)}
