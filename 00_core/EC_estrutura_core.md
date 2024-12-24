## EC_estrutura_core.md

```
/KeepAI
├── 01_migrations/          # Estrutura e evolução do banco de dados
│   ├── 00_create_schemas.sql - Cria os schemas
│   ├── 01_create_notes_table.sql - Cria a tabela de notas
│   ├── 02_create_profiles_table.sql - Cria a tabela de perfis
│   ├── 03_create_main_tables.sql - Cria as tabelas principais
│   ├── 04_new_user.sql - Gerencia novos usuários
│   ├── all_migrations.sql - Arquivo consolidado de todas as migrações
│   ├── env.py - Configurações do ambiente Alembic
│   └── alembic.ini - Configurações do Alembic
│
├── 02_notebooks/          # Notebooks Jupyter para testes e análises
│   ├── 01_test_migrations.ipynb
│   └── 02_test_auth.ipynb
│
├── 03_infra/             # Configurações de infraestrutura
│   ├── docker/          # Configurações Docker
│   └── kubernetes/      # Configurações Kubernetes
│
├── 04_scripts/           # Scripts de utilidade e automação
│   └── setup_database.py
│
├── 05_config/            # Configurações do sistema
│   └── settings/        # Arquivos de configuração
│
└── 06_logs/             # Diretório de logs do sistema
    └── app/            # Logs da aplicação
```
