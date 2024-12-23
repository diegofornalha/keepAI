#!/bin/bash

# Aguarda serviços necessários
echo "Aguardando Redis..."
while ! redis-cli -h redis ping > /dev/null 2>&1; do
    sleep 1
done

echo "Aguardando PostgreSQL..."
while ! pg_isready -h postgres -U keepai > /dev/null 2>&1; do
    sleep 1
done

# Configura timezone
ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Inicia monitoramento em background
python scripts/monitoring.py &

# Inicia a aplicação Flask com a configuração do gunicorn
gunicorn -c gunicorn.conf.py "server.app:create_app()" 