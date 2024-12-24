# KeepAI

KeepAI é um aplicativo web moderno para gerenciamento de notas, tarefas e calendário, com recursos inteligentes de IA.

## Funcionalidades

- 📝 **Notas**: Crie e organize suas notas com suporte a markdown
- ✅ **Tarefas**: Gerencie suas tarefas com listas personalizadas
- 📅 **Calendário**: Organize seus eventos e compromissos
- 🤖 **IA**: Assistente inteligente para ajudar em suas atividades
- 🔄 **Sincronização**: Seus dados sempre atualizados em todos os dispositivos
- 🌙 **Tema Escuro**: Interface adaptável para melhor conforto visual

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

```
keepai/
├── server/                    # Aplicação principal
│   ├── __init__.py           # Inicialização do pacote
│   ├── app.py                # Factory pattern e configuração do Flask
│   ├── config.py             # Configurações da aplicação
│   ├── database.py           # Configuração do Supabase
│   ├── models/               # Modelos de dados
│   ├── routes/               # Rotas da API e páginas
│   │   ├── __init__.py      # Registro de blueprints
│   │   ├── api/             # Endpoints da API
│   │   ├── auth/            # Rotas de autenticação
│   │   └── main.py          # Rotas principais
│   ├── templates/           # Templates HTML
│   ├── static/             # Arquivos estáticos
│   ├── utils/              # Utilitários
│   └── langchain_components/ # Componentes do LangChain
├── migrations/              # Migrações do banco de dados
├── scripts/                # Scripts de utilidade
├── infra/                  # Configurações de infraestrutura
├── nginx/                  # Configurações do Nginx
├── wsgi.py                # Ponto de entrada para produção
├── requirements.txt        # Dependências Python
├── setup.py               # Configuração do pacote Python
├── Dockerfile             # Configuração do Docker
└── docker-compose.yml     # Configuração do Docker Compose
```

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
