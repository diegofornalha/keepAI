import psutil
import time
import logging
from prometheus_client import start_http_server, Gauge, Counter
import os

# Métricas Prometheus
cpu_usage = Gauge("cpu_usage_percent", "CPU usage in percent")
memory_usage = Gauge("memory_usage_percent", "Memory usage in percent")
requests_total = Counter("requests_total", "Total requests processed")
request_duration = Gauge("request_duration_seconds", "Request duration in seconds")


class SystemMonitor:
    def __init__(self):
        self.logger = logging.getLogger("system_monitor")

    def collect_metrics(self):
        while True:
            try:
                # CPU
                cpu_percent = psutil.cpu_percent()
                cpu_usage.set(cpu_percent)

                # Memória
                memory = psutil.virtual_memory()
                memory_usage.set(memory.percent)

                # Logs
                if cpu_percent > 80:
                    self.logger.warning(f"Alto uso de CPU: {cpu_percent}%")
                if memory.percent > 80:
                    self.logger.warning(f"Alto uso de memória: {memory.percent}%")

                time.sleep(5)

            except Exception as e:
                self.logger.error(f"Erro ao coletar métricas: {str(e)}")


if __name__ == "__main__":
    # Inicia servidor Prometheus
    start_http_server(int(os.getenv("METRICS_PORT", 9090)))

    # Inicia monitoramento
    monitor = SystemMonitor()
    monitor.collect_metrics()
