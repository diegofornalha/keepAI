# Estágio de desenvolvimento
FROM python:3.11-slim as development

WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de configuração
COPY requirements.txt .
COPY pyproject.toml .
COPY .flake8 .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar scripts
COPY scripts/format.sh /usr/local/bin/format.sh
RUN chmod +x /usr/local/bin/format.sh

# Copiar código fonte
COPY . .

# Configurar PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Expor porta
EXPOSE 5001

# Comando para desenvolvimento
CMD ["python", "app.py"]

# Estágio de produção
FROM python:3.11-slim as production

WORKDIR /app

# Copiar apenas os arquivos necessários
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Configurar PYTHONPATH
ENV PYTHONPATH=/app:$PYTHONPATH

# Expor porta
EXPOSE 5001

# Comando para produção usando gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "--timeout", "120", "app:create_app()"] 