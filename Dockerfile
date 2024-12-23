FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    redis-tools \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Configuração do pip
COPY pip.conf /etc/pip.conf

# Copia arquivos do projeto
COPY requirements.txt ./
COPY scripts/ ./scripts/
COPY server/ ./server/
COPY gunicorn.conf.py ./

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Cria diretórios necessários
RUN mkdir -p logs backups data/cache data/uploads

# Define variáveis de ambiente
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV TZ=America/Sao_Paulo
ENV LANGCHAIN_TRACING_V2=true
ENV LANGCHAIN_ENDPOINT=https://api.smith.langchain.com

# Expõe portas
EXPOSE 3000 9090

# Script de entrada
COPY scripts/entrypoint.sh ./
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"] 