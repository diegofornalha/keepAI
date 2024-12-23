# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder

WORKDIR /build

# Instalar apenas o essencial para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && python -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir --upgrade pip setuptools \
    && apt-get purge -y --auto-remove gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências no venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt setup.py ./
COPY server ./server
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install -e .

# Stage final: apenas o necessário para Flask
FROM python:3.11-slim

# Configurar ambiente Flask
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=server.app:app \
    FLASK_DEBUG=1 \
    PYTHONPATH="/app"

WORKDIR /app

# Copiar apenas o necessário
COPY --from=builder /opt/venv /opt/venv
COPY setup.py ./
COPY server ./server

# Configurar usuário e diretórios Flask
RUN useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app \
    && pip install -e .

USER appuser
EXPOSE 5001

# Usar modo de desenvolvimento para melhor feedback
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001", "--reload"]