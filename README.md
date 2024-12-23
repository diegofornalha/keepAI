# KeepAI

KeepAI é um assistente pessoal inteligente que integra chat, notas, calendário e tarefas.

## Estrutura do Projeto

O projeto está organizado em clusters modulares para facilitar a manutenção e escalabilidade:

```
keepai/
├── client/                      # Frontend React
│   ├── src/
│   │   ├── @types/             # Definições de tipos
│   │   ├── components/         # Componentes reutilizáveis
│   │   ├── features/          # Features modulares
│   │   ├── services/          # Serviços de API
│   │   ├── hooks/             # Custom hooks
│   │   ├── store/             # Estado global
│   │   └── config/            # Configurações
│   └── public/                 # Arquivos estáticos
│
└── server/                     # Backend Python
    ├── api/                    # Endpoints da API
    ├── core/                   # Núcleo da aplicação
    ├── services/               # Serviços de negócio
    └── config/                 # Configurações


scripts/
├── start.sh       # Script principal para iniciar a aplicação
├── dev.sh         # Desenvolvimento com Docker
├── monitoring/    # Scripts de monitoramento
│   ├── load_test_extended.py
│   ├── monitoring.py
│   └── log_config.py
└── hooks/         # Git hooks
    └── pre-commit

```

## Adicionando Novas Funcionalidades

Para adicionar uma nova funcionalidade ao KeepAI, siga estes passos:

### 1. Planejamento

- Defina o escopo da funcionalidade
- Identifique as dependências necessárias
- Planeje a estrutura de dados
- Defina os endpoints da API

### 2. Backend (server/)

1. Crie um novo módulo na pasta `server/api/`
2. Defina os modelos no `server/models/`
3. Implemente os serviços em `server/services/`
4. Configure as rotas em `server/api/`
5. Atualize as configurações se necessário

Exemplo:

```python
# server/api/nova_feature/routes.py
@router.get("/nova-feature")
async def get_nova_feature():
    return {"message": "Nova feature"}
```

### 3. Frontend (client/src/)

1. Crie uma nova pasta em `features/nova_feature/`
2. Adicione os tipos em `@types/`
3. Crie o serviço em `services/`
4. Implemente os hooks em `hooks/`
5. Desenvolva os componentes
6. Atualize as rotas

Exemplo de estrutura:

```
features/nova_feature/
├── components/
│   ├── NovaFeature.tsx
│   └── NovaFeatureList.tsx
├── hooks/
│   └── useNovaFeature.ts
└── services/
    └── novaFeature.ts
```

### 4. Integração

1. Adicione a rota no `App.tsx`
2. Atualize o menu no `Sidebar.tsx`
3. Configure o estado global se necessário
4. Atualize as configurações

### 5. Testes

1. Implemente testes unitários
2. Teste a integração
3. Verifique a performance
4. Valide a UX

## Boas Práticas

### Isolamento de Features

- Cada feature deve ser independente
- Use interfaces bem definidas
- Evite acoplamento entre features
- Mantenha a coesão do código

### Gerenciamento de Estado

- Use o Zustand para estado global
- Mantenha o estado local quando possível
- Documente as mudanças de estado
- Implemente validações

### Componentização

- Crie componentes reutilizáveis
- Use TypeScript para type safety
- Implemente error boundaries
- Documente os props

### API

- Use versionamento de API
- Implemente rate limiting
- Valide inputs
- Documente endpoints

## Desenvolvimento

```bash
# Instalar dependências
npm install

# Rodar em desenvolvimento
docker-compose up --build

# Rodar testes
npm test

# Build de produção
docker-compose -f docker-compose.prod.yml up --build
```

## Contribuindo

1. Crie uma branch: `feature/nova-funcionalidade`
2. Faça suas alterações
3. Teste localmente
4. Abra um Pull Request

## Licença

MIT

## Requisitos

- Node.js 18+
- Docker e Docker Compose
- Conta no Supabase

## Configuração

1. Clone o repositório
2. Copie o arquivo `.env.example` para `.env`
3. Configure as variáveis de ambiente do Supabase no arquivo `.env`:
   ```
   SUPABASE_URL=sua_url_do_supabase
   SUPABASE_ANON_KEY=sua_chave_anonima_do_supabase
   ```
4. Execute `docker-compose up -d` para iniciar os serviços
