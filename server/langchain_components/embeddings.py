from typing import Dict, Any
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pydantic import SecretStr


def get_embeddings(api_key: str) -> GoogleGenerativeAIEmbeddings:
    """Retorna uma instância de GoogleGenerativeAIEmbeddings"""
    return GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=SecretStr(api_key),
    )


class EmbeddingGenerator:
    def __init__(self, api_key: str):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=SecretStr(api_key),
        )

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
