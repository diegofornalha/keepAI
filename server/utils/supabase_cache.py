from datetime import datetime, timedelta
import logging
from functools import wraps
from typing import Any
import numpy as np
from langchain.embeddings import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class SupabaseCache:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.table_name = "cache"

    async def get(self, key: str):
        try:
            result = (
                self.supabase.table(self.table_name)
                .select("value, expires_at")
                .eq("key", key)
                .execute()
            )

            if not result.data:
                return None

            cache_item = result.data[0]

            # Verifica se o cache expirou
            if (
                cache_item["expires_at"]
                and datetime.now().isoformat() > cache_item["expires_at"]
            ):
                await self.delete(key)
                return None

            return cache_item["value"]

        except Exception as e:
            logger.error(f"Erro ao buscar cache: {str(e)}")
            return None

    async def set(self, key: str, value: Any, ttl_minutes: int = 5):
        try:
            expires_at = (datetime.now() + timedelta(minutes=ttl_minutes)).isoformat()

            # Upsert - insere ou atualiza
            self.supabase.table(self.table_name).upsert(
                {"key": key, "value": value, "expires_at": expires_at}
            ).execute()

        except Exception as e:
            logger.error(f"Erro ao definir cache: {str(e)}")

    async def delete(self, key: str):
        try:
            self.supabase.table(self.table_name).delete().eq("key", key).execute()
        except Exception as e:
            logger.error(f"Erro ao deletar cache: {str(e)}")


class SupabaseRateLimiter:
    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.table_name = "rate_limits"

    async def check_rate_limit(self, key: str, limit: int, window_seconds: int) -> bool:
        try:
            # Remove registros antigos
            window_start = (
                datetime.now() - timedelta(seconds=window_seconds)
            ).isoformat()

            # Conta requisições no período
            result = (
                self.supabase.table(self.table_name)
                .select("count", count="exact")
                .eq("key", key)
                .gte("timestamp", window_start)
                .execute()
            )

            count = result.count or 0

            if count >= limit:
                return False

            # Registra nova requisição
            self.supabase.table(self.table_name).insert(
                {"key": key, "timestamp": datetime.now().isoformat()}
            ).execute()

            return True

        except Exception as e:
            logger.error(f"Erro no rate limiting: {str(e)}")
            return False


class SupabaseCachedEmbeddings:
    def __init__(self, supabase_client):
        self.embeddings = OpenAIEmbeddings()
        self.cache = SupabaseCache(supabase_client)

    @supabase_cached(ttl_minutes=60)
    async def get_embedding(self, text: str) -> np.ndarray:
        # Gera embedding
        embedding = await self.embeddings.aembed_query(text)
        return embedding.tolist()  # Converte para lista para serialização


class SupabaseCacheMetrics:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    async def get_metrics(self):
        stats = {"total_items": 0, "expired_items": 0, "hit_rate": 0, "size": 0}

        try:
            result = self.supabase.rpc("get_cache_metrics").execute()
            stats.update(result.data[0])
        except Exception as e:
            logger.error(f"Erro ao coletar métricas: {str(e)}")

        return stats


def supabase_cached(ttl_minutes=5):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            from server.config.settings import get_supabase_client

            # Gera chave única para a função e argumentos
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Instancia o cache
            cache = SupabaseCache(get_supabase_client())

            # Tenta buscar do cache
            cached_result = await cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Executa a função se não estiver em cache
            result = await func(*args, **kwargs)

            # Salva no cache
            await cache.set(cache_key, result, ttl_minutes)

            return result

        return wrapper

    return decorator
