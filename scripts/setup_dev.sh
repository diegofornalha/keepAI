#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Configurando ambiente de desenvolvimento...${NC}"

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 não encontrado. Por favor, instale o Python 3.8 ou superior.${NC}"
    exit 1
fi

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 não encontrado. Por favor, instale o pip3.${NC}"
    exit 1
fi

# Cria ambiente virtual
echo -e "${YELLOW}Criando ambiente virtual...${NC}"
python3 -m venv venv

# Ativa ambiente virtual
source venv/bin/activate

# Instala dependências
echo -e "${YELLOW}Instalando dependências...${NC}"
pip install -r requirements.txt

# Cria estrutura de diretórios
echo -e "${YELLOW}Criando estrutura de diretórios...${NC}"
mkdir -p logs
mkdir -p backups
mkdir -p data/cache
mkdir -p data/uploads
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/performance

# Configura variáveis de ambiente
if [ ! -f .env ]; then
    echo -e "${YELLOW}Criando arquivo .env...${NC}"
    cp .env.example .env
fi

# Configura git hooks
if [ -d .git ]; then
    echo -e "${YELLOW}Configurando git hooks...${NC}"
    cp scripts/pre-commit .git/hooks/
    chmod +x .git/hooks/pre-commit
fi

# Configura Redis (se disponível)
if command -v redis-cli &> /dev/null; then
    echo -e "${YELLOW}Verificando Redis...${NC}"
    if ! redis-cli ping > /dev/null 2>&1; then
        echo -e "${RED}Redis não está rodando. Por favor, inicie o serviço Redis.${NC}"
    else
        echo -e "${GREEN}Redis está rodando.${NC}"
    fi
fi

# Configura PostgreSQL (se disponível)
if command -v psql &> /dev/null; then
    echo -e "${YELLOW}Verificando PostgreSQL...${NC}"
    if ! pg_isready > /dev/null 2>&1; then
        echo -e "${RED}PostgreSQL não está rodando. Por favor, inicie o serviço PostgreSQL.${NC}"
    else
        echo -e "${GREEN}PostgreSQL está rodando.${NC}"
    fi
fi

# Verifica Docker
if command -v docker &> /dev/null; then
    echo -e "${YELLOW}Verificando Docker...${NC}"
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}Docker não está rodando. Por favor, inicie o serviço Docker.${NC}"
    else
        echo -e "${GREEN}Docker está rodando.${NC}"
    fi
fi

echo -e "${GREEN}Configuração do ambiente concluída!${NC}"
echo -e "${YELLOW}Para ativar o ambiente virtual, execute:${NC}"
echo -e "source venv/bin/activate" 