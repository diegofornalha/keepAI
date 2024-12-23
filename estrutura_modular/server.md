# Estrutura do Servidor

```
server/
├── modules/
│   ├── auth/          # Autenticação com Clerk
│   ├── notes/         # Gerenciamento de notas
│   ├── tasks/         # Gerenciamento de tarefas
│   ├── calendar/      # Gerenciamento de eventos
│   ├── chat/          # Chat em tempo real
│   └── ai/            # Integração com IA
├── database/
│   ├── config/        # Configurações do Supabase
│   └── repositories/  # Repositórios de dados
└── core/
    └── app.py         # Aplicação principal
```

## Descrição dos Módulos

### Auth

- Autenticação usando Clerk
- Middleware de proteção de rotas
- Gerenciamento de sessões
- Webhooks para eventos de usuário

### Notes

- CRUD de notas
- Categorização e tags
- Busca e filtros
- Validação com Pydantic

### Tasks

- Gerenciamento de tarefas
- Sistema de prioridades
- Status de progresso
- Datas e lembretes

### Calendar

- Eventos e compromissos
- Recorrência
- Notificações
- Integração com tarefas

### Chat

- Chat em tempo real
- WebSocket
- Histórico de conversas
- Integração com Gemini

### AI

- Processamento de linguagem natural
- Integração com LangChain
- Memória de conversas
- Ferramentas de automação
