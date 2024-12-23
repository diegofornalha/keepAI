import os
from typing import Optional

import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from server.config.settings import get_supabase_client


class CachedEmbeddings:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.supabase = get_supabase_client()
        self.cache_ttl = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))

    async def get_embedding(self, text: str) -> np.ndarray:
        cache_key = f"embed_{hash(text)}"

        # Tenta recuperar do cache
        result = self.supabase.table('embeddings_cache').select('embedding').eq('key', cache_key).execute()
        
        if result.data:
            return np.frombuffer(bytes(result.data[0]['embedding']))

        # Gera novo embedding
        embedding = await self.embeddings.aembed_query(text)

        # Salva no cache
        self.supabase.table('embeddings_cache').insert({
            'key': cache_key,
            'embedding': embedding.tobytes(),
            'created_at': 'now()'  # Supabase gerencia automaticamente a expiração
        }).execute()

        return embedding
