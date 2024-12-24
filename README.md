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

- [EC_estrutura_core.md](00_core/EC_estrutura_core.md)
- [EC_estrutura_server.md](server/EC_estrutura_server.md)

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
