# KeepAI

KeepAI é um aplicativo web moderno para gerenciamento de notas, tarefas e calendário, com recursos inteligentes de IA.

## Funcionalidades

- 📝 **Notas**: Crie e organize suas notas com suporte a markdown
- ✅ **Tarefas**: Gerencie suas tarefas com listas personalizadas
- 📅 **Calendário**: Organize seus eventos e compromissos
- 🤖 **IA**: Assistente inteligente para ajudar em suas atividades
- 🔄 **Sincronização**: Seus dados sempre atualizados em todos os dispositivos
- 🌙 **Tema Escuro**: Interface adaptável para melhor conforto visual

## Scripts Utilitários

O projeto inclui scripts úteis para desenvolvimento e manutenção:

### Setup do Banco de Dados

Para configurar o banco de dados Supabase:

```bash
python 00_core/04_scripts/setup_database.py
```

Este script:

- Cria as tabelas necessárias no Supabase
- Configura as colunas e relacionamentos
- Requer as variáveis de ambiente `SUPABASE_URL` e `SUPABASE_KEY`

### Limpeza de Arquivos Temporários

Para manter o projeto organizado, use o script de limpeza:

```bash
python 00_core/04_scripts/cleanup.py
```

Este script remove automaticamente:

- Arquivos de cache Python (`__pycache__`, `.pyc`, etc.)
- Ambientes virtuais (`.venv`, `venv`)
- Caches de ferramentas (`.mypy_cache`, `.pytest_cache`, etc.)
- Arquivos de build (`*.egg-info`, `build`, `dist`)
- Arquivos temporários de IDEs
- Arquivos de log
- Outros arquivos temporários do sistema

O script é seguro e:

- Protege diretórios importantes (`.git`, `static`, etc.)
- Mostra feedback detalhado
- Trata erros graciosamente

## Arquitetura

O KeepAI segue uma arquitetura modular e limpa:

- **API RESTful**: Interface clara e bem definida para todas as operações
- **Autenticação**: Opção de autenticação com Clerk
- **Banco de Dados**: Persistência eficiente com Supabase
- **Frontend**: Interface feita no flask
- **IA**: Integração otimizada com Google Gemini

## Tecnologias

- **Backend**:

  - Python 3.11
  - Flask (Framework em Python)
  - Supabase (Banco de Dados)
  - Clerk (Autenticação)
  - JWT (Tokens de Acesso)
  - Gunicorn (Servidor WSGI)
  - Google Gemini (IA)
  - LangChain (Framework de IA)

- **Frontend**:
  - Jinja2 Templates
  - HTML5 & CSS3
  - JavaScript (ES6+)
  - Bootstrap 5
  - FullCalendar

## Requisitos

- Python 3.11+
- Docker e Docker Compose
- Conta no Supabase
- Conta no Clerk

## Configuração

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/keepai.git
cd keepai
```

2. Inicie o container:

```bash
docker compose up -d
```

3. Acesse o aplicativo em `http://localhost:5001`

## Desenvolvimento

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Execute os testes:

```bash
pytest
```

3. Verifique o estilo do código:

```bash
flake8
black .
mypy .
```

## Estrutura do Projeto

- [EC_estrutura_core.md](00_core/EC_estrutura_core.md)
- [EC_estrutura_server.md](server/EC_estrutura_server.md)

## Prioridades e Dependências

1. **01_migrations**: Base do projeto, define a estrutura do banco de dados
2. **02_notebooks**: Ferramentas para teste e análise do sistema
3. **03_server**: Implementação principal da aplicação
4. **04_infra**: Configurações de infraestrutura para deploy
5. **05_nginx**: Configurações do servidor web
6. **06_scripts**: Scripts auxiliares e automações

## Tecnologias Principais

- **Backend**: Python 3.11+ com Flask
- **Banco de Dados**: Supabase (PostgreSQL)
- **Autenticação**: Clerk
- **Cache**: Redis
- **IA**: LangChain
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Containerização**: Docker
- **Proxy Reverso**: Nginx
- **CI/CD**: GitHub Actions

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Configuração do Gemini

O projeto utiliza o Google Gemini Pro com as seguintes configurações otimizadas:

- Modelo: gemini-pro
- Temperatura: 0.7
- Max Output Tokens: 2048
- Top P: 0.8
- Top K: 40

Estas configurações foram ajustadas para fornecer um equilíbrio ideal entre criatividade e precisão nas respostas.
