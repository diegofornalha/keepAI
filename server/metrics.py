from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from functools import wraps
import time
import psutil
import platform

# Métricas HTTP
http_requests_total = Counter(
    "http_requests_total", "Total de requisições HTTP", ["method", "endpoint", "status"]
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "Duração das requisições HTTP",
    ["method", "endpoint"],
)

# Métricas de Cache
cache_hits_total = Counter("cache_hits_total", "Total de acertos no cache")
cache_misses_total = Counter("cache_misses_total", "Total de falhas no cache")

# Métricas de Sistema
cpu_usage = Gauge("cpu_usage_percent", "Uso de CPU em porcentagem")
memory_usage = Gauge("memory_usage_percent", "Uso de memória em porcentagem")

# Informações do sistema
system_info = Info("keepai_info", "Informações do sistema KeepAI")


def track_request():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            start_time = time.time()

            try:
                response = f(*args, **kwargs)
                status = response.status_code
            except Exception as e:
                status = 500
                raise e
            finally:
                duration = time.time() - start_time
                http_requests_total.labels(
                    method=request.method, endpoint=request.endpoint, status=status
                ).inc()

                http_request_duration_seconds.labels(
                    method=request.method, endpoint=request.endpoint
                ).observe(duration)

            return response

        return wrapped

    return decorator


def update_system_metrics():
    """Atualiza métricas do sistema periodicamente"""
    cpu_usage.set(psutil.cpu_percent())
    memory_usage.set(psutil.virtual_memory().percent)


def init_metrics(app):
    """Inicializa as métricas e adiciona endpoints"""
    system_info.info(
        {
            "version": "1.0.0",
            "python_version": platform.python_version(),
        }
    )

    @app.route("/metrics")
    def metrics():
        update_system_metrics()
        return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

    return app
