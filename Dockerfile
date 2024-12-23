FROM python:3.11-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY server/templates/ templates/
COPY server/static/ static/
COPY server/config/ server/config/
COPY app.py .
COPY gunicorn.conf.py .

# Expor porta
EXPOSE 5000

# Comando para iniciar
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]