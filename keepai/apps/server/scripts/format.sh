#!/bin/bash

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir mensagens de erro
error() {
    echo -e "${RED}Erro: $1${NC}" >&2
    exit 1
}

# Função para imprimir mensagens de sucesso
success() {
    echo -e "${GREEN}$1${NC}"
}

# Função para imprimir mensagens de aviso
warning() {
    echo -e "${YELLOW}Aviso: $1${NC}"
}

# Verificar se estamos no diretório correto
if [ ! -f "pyproject.toml" ]; then
    error "Este script deve ser executado do diretório raiz do projeto"
fi

# Instalar dependências de desenvolvimento se necessário
if ! pip freeze | grep -q "black=="; then
    warning "Instalando dependências de desenvolvimento..."
    pip install -r requirements.txt
fi

# Formatar código com Black
echo "Formatando código com Black..."
if ! black --check .; then
    warning "Arquivos precisam ser formatados"
    black .
else
    success "Código já está formatado corretamente com Black"
fi

# Ordenar imports com isort
echo -e "\nOrdenando imports com isort..."
if ! isort --check-only .; then
    warning "Imports precisam ser ordenados"
    isort .
else
    success "Imports já estão ordenados corretamente"
fi

# Verificar tipos com mypy
echo -e "\nVerificando tipos com mypy..."
if ! mypy .; then
    warning "Verificação de tipos encontrou problemas"
else
    success "Verificação de tipos passou com sucesso"
fi

# Verificar estilo com flake8
echo -e "\nVerificando estilo com flake8..."
if ! flake8 .; then
    warning "Verificação de estilo encontrou problemas"
else
    success "Verificação de estilo passou com sucesso"
fi

# Executar testes
echo -e "\nExecutando testes..."
if ! pytest; then
    warning "Alguns testes falharam"
else
    success "Todos os testes passaram com sucesso"
fi

success "\nProcesso de formatação e verificação concluído!"