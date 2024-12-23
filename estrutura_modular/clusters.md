# Estrutura de Clusters

## Visão Geral dos Clusters

```
keepai/
├── apps/              # Aplicações
│   ├── web/          # Frontend Flask
│   └── server/       # Backend Flask
├── packages/          # Pacotes compartilhados
│   ├── ui/           # Biblioteca de UI
│   ├── types/        # Tipos compartilhados
│   └── utils/        # Utilitários comuns
├── services/         # Microsserviços
│   ├── ai/           # Serviço de IA
│   └── realtime/     # Serviço de tempo real
└── infrastructure/   # Infraestrutura
    ├── docker/       # Configurações Docker
    ├── nginx/        # Proxy reverso
    └── scripts/      # Scripts de automação
```

## Descrição dos Clusters

### Apps

#### Web (Frontend)

```
web/
├── src/
│   ├── features/     # Funcionalidades por domínio
│   │   ├── auth/     # Autenticação
│   │   ├── notes/    # Notas
│   │   ├── tasks/    # Tarefas
│   │   └── chat/     # Chat
│   ├── shared/       # Recursos compartilhados
│   └���─ core/         # Núcleo da aplicação
└── public/           # Arquivos estáticos
```

#### Server (Backend)

```
server/
├── modules/          # Módulos por domínio
│   ├── auth/         # Autenticação
│   ├── notes/        # Notas
│   ├── tasks/        # Tarefas
│   └── chat/         # Chat
├── core/             # Núcleo da aplicação
└── database/         # Acesso a dados
```

### Packages

#### UI

```
ui/
├── components/       # Componentes base
├── hooks/           # Hooks
└── styles/          # Estilos e temas
```

#### Types

```
types/
├── models/          # Modelos de dados
├── api/             # Tipos da API
└── shared/          # Tipos compartilhados
```

#### Utils

```
utils/
├── formatters/      # Formatadores
├── validators/      # Validadores
└── helpers/         # Funções auxiliares
```

### Services

#### AI

```
ai/
├── models/          # Modelos de IA
├── pipelines/       # Pipelines de processamento
└── api/             # API do serviço
```

#### Realtime

```
realtime/
├── websocket/       # Servidor WebSocket
├── events/          # Gerenciamento de eventos
└── api/             # API do serviço
```

## Vantagens desta Estrutura

1. **Separação Clara de Responsabilidades**

   - Cada cluster tem um propósito específico
   - Facilita a manutenção e escalabilidade
   - Reduz acoplamento entre módulos

2. **Reusabilidade**

   - Pacotes compartilhados entre aplicações
   - Componentes UI reutilizáveis
   - Tipos e utilitários comuns

3. **Escalabilidade**

   - Serviços podem ser escalados independentemente
   - Facilita adição de novas funcionalidades
   - Suporta crescimento do projeto

4. **Desenvolvimento em Equipe**

   - Times podem trabalhar em paralelo
   - Menos conflitos de código
   - Melhor organização do trabalho

5. **Deployment**
   - Deploy independente por serviço
   - Facilita CI/CD
   - Melhor gerenciamento de recursos

## Próximos Passos

1. **Microsserviços**

   - Separar IA em serviço independente
   - Implementar comunicação via mensageria
   - Adicionar cache distribuído

2. **Monitoramento**

   - Implementar logging centralizado
   - Adicionar métricas e traces
   - Configurar alertas

3. **Performance**
   - Implementar CDN
   - Otimizar carga de assets
   - Adicionar cache em múltiplas camadas
