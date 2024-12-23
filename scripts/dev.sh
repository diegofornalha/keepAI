#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Configurações do Docker para Mac
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_DEFAULT_PLATFORM=linux/amd64

# Configurações de memória para Node
export NODE_OPTIONS="--max-old-space-size=4096"
export GENERATE_SOURCEMAP=false

echo -e "${BLUE}🔄 Iniciando ambiente de desenvolvimento...${NC}"

# Verificar se está no diretório correto
if [ ! -f "docker-compose.yml" ]; then
    cd /Users/flow/Desktop/Desktop/KeepAI || exit
fi

# Limpar ambiente anterior
echo -e "${BLUE}🧹 Limpando ambiente anterior...${NC}"
docker-compose down --remove-orphans
docker system prune -f

# Instalar dependências do cliente
echo -e "${BLUE}📦 Instalando dependências do cliente...${NC}"
cd client || exit

# Remover node_modules e package-lock apenas se necessário
if [ -d "node_modules" ] || [ -f "package-lock.json" ]; then
    echo -e "${YELLOW}⚠️  Removendo node_modules e package-lock.json antigos...${NC}"
    rm -rf node_modules package-lock.json
    npm cache clean --force
fi

# Instalar dependências principais com --legacy-peer-deps
echo -e "${BLUE}📦 Instalando dependências principais...${NC}"
npm install --legacy-peer-deps --quiet

# Build do cliente
echo -e "${BLUE}🔨 Construindo cliente...${NC}"
npm run build
cd ..

# Configurar limites de recursos do Docker
echo -e "${BLUE}⚙️ Configurando recursos do Docker...${NC}"
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock alpine sh -c '
  docker update --cpu-quota=200000 --cpu-period=100000 --memory=4G --memory-swap=4G $(docker ps -q)
'

# Iniciar serviços
echo -e "${BLUE}🚀 Iniciando serviços...${NC}"
DOCKER_BUILDKIT=1 COMPOSE_DOCKER_CLI_BUILD=1 docker-compose up --build -d

# Aguardar serviços com timeout (alterando a porta para 8000)
echo -e "${BLUE}⏳ Aguardando serviços...${NC}"
TIMEOUT=60
ELAPSED=0
until curl -s http://localhost:8000/api/v1/health > /dev/null; do
    if [ $ELAPSED -ge $TIMEOUT ]; then
        echo -e "${RED}❌ Timeout aguardando API. Verifique os logs com: docker-compose logs${NC}"
        exit 1
    fi
    echo "Aguardando API... ($ELAPSED/$TIMEOUT segundos)"
    sleep 2
    ELAPSED=$((ELAPSED+2))
done

echo -e "${GREEN}✅ Ambiente pronto!${NC}"

# Mostrar logs
echo -e "${BLUE}📋 Mostrando logs dos serviços...${NC}"
docker-compose logs -f
  