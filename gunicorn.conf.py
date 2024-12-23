from server.config.settings import settings

# Configurações do Gunicorn
bind = "0.0.0.0:8000"
workers = 4
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Nome do projeto
proc_name = settings.PROJECT_NAME
