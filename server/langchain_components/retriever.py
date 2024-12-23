from langchain.retrievers import SupabaseVectorStore
from langchain.schema import Document
from typing import List, Optional
import os


class CustomRetriever:
    def __init__(self, embeddings, supabase_client):
        self.vector_store = SupabaseVectorStore(
            embedding=embeddings,
            client=supabase_client,
            table_name="documents",
            query_name="match_documents",
        )

    async def similar_search(
        self, query: str, k: int = 4, threshold: float = 0.7
    ) -> List[Document]:
        results = await self.vector_store.asimilarity_search(
            query, k=k, threshold=threshold
        )

        return results

    async def add_documents(self, documents: List[Document]):
        await self.vector_store.aadd_documents(documents)
