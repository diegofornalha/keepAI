FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY server/ server/
COPY shared/ shared/
COPY app.py .
COPY gunicorn.conf.py .
COPY .env .

# Criar diretórios necessários
RUN mkdir -p logs data

# Configurar variáveis de ambiente
ENV PYTHONPATH=/app
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expor porta
EXPOSE 5000

# Comando para iniciar
CMD ["gunicorn", "--config", "gunicorn.conf.py", "app:app"]