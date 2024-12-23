from datetime import datetime, timedelta
from functools import wraps
import logging
import threading
import time
import psutil

logger = logging.getLogger("keepai")


class Cache:
    def __init__(self):
        self._cache = {}
        self._expiry = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "evictions": 0,
            "memory_usage": 0,
            "peak_memory_usage": 0,
            "last_cleanup": datetime.now().isoformat(),
            "endpoints": {},
            "memory_samples": [],  # Lista para armazenar amostras de uso de memória
        }
        self._lock = threading.Lock()
        self._start_cleanup_thread()
        self._start_memory_monitor()

    def _start_cleanup_thread(self):
        def cleanup_task():
            while True:
                time.sleep(300)  # Executa a cada 5 minutos
                self.cleanup()

        thread = threading.Thread(target=cleanup_task, daemon=True)
        thread.start()

    def _start_memory_monitor(self):
        """Inicia thread de monitoramento de memória"""

        def monitor_task():
            while True:
                try:
                    process = psutil.Process()
                    memory_info = {
                        "timestamp": datetime.now().isoformat(),
                        "rss": process.memory_info().rss / 1024 / 1024,  # MB
                        "vms": process.memory_info().vms / 1024 / 1024,  # MB
                        "percent": process.memory_percent(),
                    }

                    with self._lock:
                        self._stats["memory_samples"].append(memory_info)
                        # Mantém apenas as últimas 100 amostras
                        if len(self._stats["memory_samples"]) > 100:
                            self._stats["memory_samples"].pop(0)

                        # Atualiza pico de memória
                        if memory_info["rss"] > self._stats["peak_memory_usage"]:
                            self._stats["peak_memory_usage"] = memory_info["rss"]

                    time.sleep(60)  # Coleta a cada minuto
                except Exception as e:
                    logger.error(f"Erro no monitoramento de memória: {str(e)}")
                    time.sleep(60)  # Espera antes de tentar novamente

        thread = threading.Thread(target=monitor_task, daemon=True)
        thread.start()

    def _update_endpoint_stats(self, endpoint, hit=False):
        """Atualiza estatísticas por endpoint"""
        if endpoint not in self._stats["endpoints"]:
            self._stats["endpoints"][endpoint] = {"hits": 0, "misses": 0, "sets": 0}

        if hit:
            self._stats["endpoints"][endpoint]["hits"] += 1
        else:
            self._stats["endpoints"][endpoint]["misses"] += 1

    def _estimate_size(self, value):
        """Estima o tamanho em bytes de um objeto"""
        return len(str(value).encode("utf-8"))

    def set(self, key, value, ttl_minutes=10):
        """
        Armazena um valor no cache com tempo de expiração
        """
        try:
            with self._lock:
                self._cache[key] = value
                self._expiry[key] = datetime.now() + timedelta(minutes=ttl_minutes)
                self._stats["sets"] += 1
                size = self._estimate_size(value)
                self._stats["memory_usage"] += size

                # Atualiza estatísticas do endpoint
                endpoint = key.split(":")[0] if ":" in key else "unknown"
                if endpoint not in self._stats["endpoints"]:
                    self._stats["endpoints"][endpoint] = {
                        "hits": 0,
                        "misses": 0,
                        "sets": 0,
                        "memory_usage": 0,
                    }
                self._stats["endpoints"][endpoint]["sets"] += 1
                self._stats["endpoints"][endpoint]["memory_usage"] += size

                logger.debug(
                    f"Cache set: {key} (TTL: {ttl_minutes} minutes, size: {size/1024:.2f}KB)"
                )
        except Exception as e:
            logger.error(f"Erro ao definir cache para {key}: {str(e)}")

    def get(self, key):
        """
        Recupera um valor do cache, retorna None se expirado ou não existente
        """
        try:
            with self._lock:
                if key in self._cache:
                    if datetime.now() < self._expiry[key]:
                        self._stats["hits"] += 1

                        # Atualiza estatísticas do endpoint
                        endpoint = key.split(":")[0] if ":" in key else "unknown"
                        self._update_endpoint_stats(endpoint, hit=True)

                        logger.debug(f"Cache hit: {key}")
                        return self._cache[key]
                    else:
                        logger.debug(f"Cache expired: {key}")
                        self._stats["evictions"] += 1
                        self._stats["memory_usage"] -= self._estimate_size(
                            self._cache[key]
                        )
                        del self._cache[key]
                        del self._expiry[key]

                self._stats["misses"] += 1
                # Atualiza estatísticas do endpoint
                endpoint = key.split(":")[0] if ":" in key else "unknown"
                self._update_endpoint_stats(endpoint, hit=False)

                logger.debug(f"Cache miss: {key}")
                return None
        except Exception as e:
            logger.error(f"Erro ao recuperar cache para {key}: {str(e)}")
            return None

    def clear(self):
        """Limpa todo o cache"""
        with self._lock:
            self._cache.clear()
            self._expiry.clear()
            self._stats = {
                "hits": 0,
                "misses": 0,
                "sets": 0,
                "evictions": 0,
                "memory_usage": 0,
                "peak_memory_usage": 0,
                "last_cleanup": datetime.now().isoformat(),
                "endpoints": {},
                "memory_samples": [],
            }
            logger.debug("Cache cleared")

    def cleanup(self):
        """
        Remove itens expirados do cache
        """
        try:
            with self._lock:
                now = datetime.now()
                expired = [k for k, v in self._expiry.items() if now > v]
                for key in expired:
                    self._stats["evictions"] += 1
                    self._stats["memory_usage"] -= self._estimate_size(self._cache[key])
                    del self._cache[key]
                    del self._expiry[key]
                if expired:
                    logger.debug(f"Cleaned {len(expired)} expired items from cache")
                self._stats["last_cleanup"] = now.isoformat()
        except Exception as e:
            logger.error(f"Erro durante limpeza do cache: {str(e)}")

    def get_stats(self):
        """
        Retorna estatísticas do cache
        """
        with self._lock:
            total_requests = self._stats["hits"] + self._stats["misses"]
            hit_rate = (
                (self._stats["hits"] / total_requests * 100)
                if total_requests > 0
                else 0
            )

            # Calcula estatísticas por endpoint
            endpoint_stats = {}
            for endpoint, stats in self._stats["endpoints"].items():
                total = stats["hits"] + stats["misses"]
                if total > 0:
                    endpoint_stats[endpoint] = {
                        **stats,
                        "hit_rate": f"{(stats['hits'] / total * 100):.2f}%",
                        "memory_usage_mb": f"{stats['memory_usage']/1024/1024:.2f}MB",
                    }

            # Calcula estatísticas de memória
            memory_stats = {
                "current_usage_mb": f"{self._stats['memory_usage']/1024/1024:.2f}MB",
                "peak_usage_mb": f"{self._stats['peak_memory_usage']:.2f}MB",
                "samples": self._stats["memory_samples"][-5:],  # Últimas 5 amostras
            }

            return {
                **self._stats,
                "total_items": len(self._cache),
                "hit_rate": f"{hit_rate:.2f}%",
                "memory_usage_mb": f'{self._stats["memory_usage"]/1024/1024:.2f}MB',
                "endpoints": endpoint_stats,
                "memory_stats": memory_stats,
            }


# Instância global do cache
cache = Cache()


def cached(ttl_minutes=5):
    """
    Decorator para cachear resultados de funções
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Cria uma chave única baseada na função e argumentos
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

                # Tenta obter do cache
                result = cache.get(key)
                if result is not None:
                    return result

                # Se não está no cache, executa a função
                result = func(*args, **kwargs)
                cache.set(key, result, ttl_minutes)
                return result
            except Exception as e:
                logger.error(f"Erro no decorator de cache: {str(e)}")
                # Em caso de erro no cache, executa a função normalmente
                return func(*args, **kwargs)

        return wrapper

    return decorator
