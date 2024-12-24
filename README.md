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

2. Configure o ambiente:

```bash
cp .env.example .env
# Configure suas variáveis de ambiente no .env
```

3. Inicie o container:

```bash
docker compose up -d
```

4. Acesse o aplicativo em `http://localhost:5001`

## Scripts Utilitários

### Configurar URLs do Supabase

```bash
python 00_core/04_scripts/setup_env.py
```

Configura as URLs necessárias para conexão com o Supabase:

- `DATABASE_URL`: Conexão direta para a aplicação
- `SUPABASE_DB_URL`: Alias para scripts de migração

### Migrações do Banco de Dados

Para executar e testar as migrações, use o Jupyter Notebook:

1. Instale as dependências:

```bash
pip install jupyter notebook pandas numpy matplotlib seaborn
```

2. Inicie o Jupyter:

```bash
jupyter notebook  # Acesse em http://localhost:8888/tree
```

3. Abra o notebook `00_core/02_notebooks/01_test_migrations.ipynb`

O notebook usa LangChain + Gemini Pro para:

- Executar as migrações em ordem
- Verificar se cada migração foi bem sucedida
- Validar o estado final do banco
- Fornecer feedback em linguagem natural

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
