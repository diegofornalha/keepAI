#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Iniciando KeepAI...${NC}\n"

# Verificar se o ambiente virtual Python existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Criando ambiente virtual Python...${NC}"
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Instalar dependências do servidor
echo -e "${YELLOW}Instalando dependências do servidor...${NC}"
cd server
pip install -r requirements.txt

# Iniciar servidor em background
echo -e "${YELLOW}Iniciando servidor FastAPI...${NC}"
uvicorn main:app --reload --port 8000 &
SERVER_PID=$!

# Voltar para a raiz
cd ..

# Instalar dependências do cliente
echo -e "${YELLOW}Instalando dependências do cliente...${NC}"
cd client
npm install

# Resolver erro do vite
echo -e "${YELLOW}Instalando dependências do Vite...${NC}"
npm install -D @types/node vite @vitejs/plugin-react

# Iniciar cliente
echo -e "${YELLOW}Iniciando cliente Vite...${NC}"
npm run dev &
CLIENT_PID=$!

# Voltar para a raiz
cd ..

echo -e "\n${GREEN}KeepAI está rodando!${NC}"
echo -e "API: ${YELLOW}http://localhost:8000${NC}"
echo -e "Cliente: ${YELLOW}http://localhost:3000${NC}"
echo -e "\nPressione ${RED}Ctrl+C${NC} para encerrar todos os serviços\n"

# Função para limpar processos ao encerrar
cleanup() {
    echo -e "\n${YELLOW}Encerrando serviços...${NC}"
    kill $SERVER_PID
    kill $CLIENT_PID
    deactivate
    echo -e "${GREEN}Serviços encerrados!${NC}"
    exit 0
}

# Registrar função de cleanup
trap cleanup SIGINT SIGTERM

# Manter script rodando
wait 