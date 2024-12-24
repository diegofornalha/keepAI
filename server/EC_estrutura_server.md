## EC_estrutura_server.md

```
/KeepAI/03_server
├── config/                     # Configurações da aplicação
│   ├── __init__.py
│   ├── settings.py            # Configurações gerais
│   └── logging_config.py      # Configuração de logs
│
├── modules/                    # Módulos principais
│   ├── __init__.py
│   ├── auth/                  # Autenticação
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── utils.py
│   │
│   ├── notes/                 # Gerenciamento de notas
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── services.py
│   │
│   ├── tasks/                 # Gerenciamento de tarefas
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── services.py
│   │
│   └── calendar/              # Gerenciamento de calendário
│       ├── __init__.py
│       ├── models.py
│       ├── routes.py
│       └── services.py
│
├── langchain_components/      # Componentes LangChain
│   ├── __init__.py
│   ├── chains/               # Cadeias personalizadas
│   │   └── __init__.py
│   ├── prompts/              # Templates de prompts
│   │   └── __init__.py
│   └── utils/                # Utilitários
│       └── __init__.py
│
├── static/                    # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── img/
│
├── templates/                 # Templates HTML
│   ├── base.html
│   ├── auth/
│   ├── notes/
│   ├── tasks/
│   └── calendar/
│
├── tests/                     # Testes
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
│
├── utils/                     # Utilitários gerais
│   ├── __init__.py
│   ├── decorators.py
│   └── helpers.py
│
├── __init__.py
├── app.py                     # Aplicação principal
└── wsgi.py                    # Entrada WSGI

```
