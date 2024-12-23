import multiprocessing
from server.config.settings import Settings

settings = Settings()

# Configurações do servidor
bind = f"{settings.HOST}:{settings.PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
threads = 2
timeout = 120

# Configurações de logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Configurações de desenvolvimento
reload = settings.DEBUG
reload_extra_files = ["server/templates/", "server/static/"]

# Configurações de segurança
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190
