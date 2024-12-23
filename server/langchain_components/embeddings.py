from langchain.embeddings import OpenAIEmbeddings
from langchain.cache import InMemoryCache
import numpy as np
from typing import Optional
import os
import redis


class CachedEmbeddings:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.redis_client = redis.Redis.from_url(os.getenv("CACHE_REDIS_URL"))
        self.cache_ttl = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))

    async def get_embedding(self, text: str) -> np.ndarray:
        cache_key = f"embed_{hash(text)}"

        # Tenta recuperar do cache
        cached = self.redis_client.get(cache_key)
        if cached:
            return np.frombuffer(cached)

        # Gera novo embedding
        embedding = await self.embeddings.aembed_query(text)

        # Salva no cache
        self.redis_client.setex(cache_key, self.cache_ttl, embedding.tobytes())

        return embedding
