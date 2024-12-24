## EC_estrutura_core.md

```
/KeepAI
├── 01_migrations/          # Estrutura e evolução do banco de dados
│   ├── 01_create_notes_table.sql
│   └── 02_create_profiles_table.sql
│
├── 02_notebooks/          # Notebooks Jupyter para testes e análises
│   ├── keepAI.ipynb
│
├── 03_server/            # Código principal da aplicação
│   ├── config/          # Configurações
│   ├── modules/         # Módulos da aplicação
│   └── langchain_components/  # Componentes LangChain
│
├── 04_infra/            # Configurações de infraestrutura
│   ├── docker/         # Configurações Docker
│   └── kubernetes/     # Configurações Kubernetes
│
├── 05_nginx/            # Configurações do servidor web
│   └── conf.d/         # Arquivos de configuração Nginx
│
└── 06_scripts/          # Scripts de utilidade e automação
    └── setup_database.py
```
