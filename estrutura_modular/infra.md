# Estrutura de Infraestrutura

```
infra/
├── docker/            # Configurações Docker
│   ├── Dockerfile
│   └── docker-compose.yml
├── nginx/            # Configuração do proxy reverso
│   ├── nginx.conf
│   └── ssl/
├── scripts/          # Scripts de automação
│   ├── backup/
│   └── deploy/
└── env/             # Variáveis de ambiente
    ├── .env.example
    └── .env.local
```

## Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "wsgi:app"]
```

### docker-compose.yml

```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "5001:5001"
    env_file:
      - .env.local
    volumes:
      - .:/app
```

## Nginx

### nginx.conf

```nginx
server {
    listen 80;
    server_name keepai.com;

    location / {
        proxy_pass http://app:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /ws {
        proxy_pass http://app:5001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

## Scripts

### backup.sh

```bash
#!/bin/bash
# Script de backup do banco de dados
supabase db dump -f backup.sql
```

### deploy.sh

```bash
#!/bin/bash
# Script de deploy
git pull
docker-compose down
docker-compose up --build -d
```

## Variáveis de Ambiente

### .env.local

- Chaves do Supabase
- Chaves do Clerk
- Chave do Gemini
- Configurações do servidor

### .env.example

- Template para configuração
- Valores padrão
- Documentação das variáveis
