import time
from typing import Any, cast

try:
    import psutil
    from prometheus_client import (  # type: ignore[import-not-found]
        start_http_server,
        Gauge,
    )
except ImportError:
    psutil = cast(Any, None)
    start_http_server = cast(Any, None)
    Gauge = cast(Any, None)


# Métricas do Prometheus
if Gauge:
    cpu_usage = Gauge("cpu_usage_percent", "CPU usage in percent")
    memory_usage = Gauge("memory_usage_percent", "Memory usage in percent")
    disk_usage = Gauge("disk_usage_percent", "Disk usage in percent")
else:
    cpu_usage = None
    memory_usage = None
    disk_usage = None


def collect_metrics() -> None:
    """Coleta métricas do sistema"""
    if psutil and cpu_usage and memory_usage and disk_usage:
        cpu_usage.set(psutil.cpu_percent())
        memory_usage.set(psutil.virtual_memory().percent)
        disk_usage.set(psutil.disk_usage("/").percent)


def main() -> None:
    """Função principal do monitoramento"""
    # Inicia o servidor HTTP do Prometheus na porta 8000
    if start_http_server:
        start_http_server(8000)

    while True:
        collect_metrics()
        time.sleep(15)  # Coleta métricas a cada 15 segundos


if __name__ == "__main__":
    main()
