## EC_estrutura_server.md

```
/KeepAI/server
├── config/                     # Configurações da aplicação
│   ├── __init__.py
│   ├── settings.py            # Configurações gerais
│   └── logging_config.py      # Configuração de logs
│
├── models/                     # Modelos de dados
│   ├── __init__.py
│   ├── user.py
│   ├── note.py
│   └── task.py
│
├── routes/                     # Rotas da API
│   ├── __init__.py
│   ├── auth.py
│   ├── notes.py
│   └── tasks.py
│
├── services/                   # Camada de serviços
│   ├── __init__.py
│   ├── auth_service.py
│   ├── note_service.py
│   └── task_service.py
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
│   └── tasks/                 # Gerenciamento de tarefas
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
│   └── tasks/
│
├── utils/                     # Utilitários gerais
│   ├── __init__.py
│   ├── decorators.py
│   └── helpers.py
│
├── __init__.py               # Inicialização do pacote
├── run.py                    # Script para executar o servidor
└── wsgi.py                   # Entrada WSGI

```
