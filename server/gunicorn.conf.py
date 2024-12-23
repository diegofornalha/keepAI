import multiprocessing
import os

# Configurações básicas
bind = "0.0.0.0:5001"  # Mantendo a mesma porta que estávamos usando
workers = multiprocessing.cpu_count() * 2 + 1

# Configurações de timeout (importante para requisições de IA)
timeout = 120  # 2 minutos para processar requisições
keepalive = 5

# Configurações de logging
accesslog = "-"  # stdout
errorlog = "-"  # stdout
loglevel = "info"

# Configurações de performance
worker_class = "sync"  # Usando worker sync por ser mais estável
max_requests = 1000  # Reinicia worker após 1000 requisições
max_requests_jitter = 50  # Adiciona variação para evitar reinício simultâneo

# Configurações de ambiente
raw_env = [
    f"FLASK_APP=app:app",
    f"FLASK_ENV={'development' if os.getenv('FLASK_ENV') == 'development' else 'production'}",
    f"PYTHONPATH={os.getcwd()}",
]

# Configurações de debug (ativas apenas em desenvolvimento)
reload = os.getenv("FLASK_ENV") == "development"
capture_output = True
