# Estrutura do Banco de Dados (Supabase)

```
database/
├── tables/
│   ├── notes/         # Notas e categorias
│   ├── tasks/         # Tarefas e status
│   ├── calendar/      # Eventos e recorrências
│   ├── chat/          # Mensagens e sessões
│   └── profiles/      # Perfis de usuário
├── functions/         # Funções e triggers
└── policies/          # Políticas de segurança
```

## Tabelas Principais

### Notes

```sql
create table notes (
  id bigint primary key generated always as identity,
  user_id text not null,
  title text not null,
  content text,
  tags text[],
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### Tasks

```sql
create table tasks (
  id bigint primary key generated always as identity,
  title varchar(200) not null,
  description text,
  due_date timestamptz,
  priority smallint not null default 2,
  status varchar(20) not null default 'pending',
  tags text[] default '{}',
  created_at timestamptz default now(),
  updated_at timestamptz default now(),
  completed_at timestamptz
);
```

### Calendar

```sql
create table events (
  id bigint primary key generated always as identity,
  title text not null,
  description text,
  start_date timestamptz not null,
  end_date timestamptz not null,
  all_day boolean default false,
  recurrence jsonb,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

### Chat

```sql
create table chat_sessions (
  id uuid primary key default uuid_generate_v4(),
  user_id text not null,
  title text not null,
  metadata jsonb default '{}',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

create table chat_messages (
  id bigint primary key generated always as identity,
  chat_id uuid not null references chat_sessions(id),
  user_id text not null,
  role text not null,
  content text not null,
  status text not null default 'pending',
  metadata jsonb default '{}',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);
```

## Políticas de Segurança (RLS)

- Usuários só podem ver seus próprios dados
- Autenticação obrigatória para todas as operações
- Proteção contra injeção SQL
- Validação de dados

## Funções e Triggers

- Atualização automática de timestamps
- Notificações em tempo real
- Busca full-text
- Cache inteligente
