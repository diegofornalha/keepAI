-- Tabela de cache
create table if not exists cache (
    id uuid default uuid_generate_v4() primary key,
    key text not null unique,
    value jsonb not null,
    expires_at timestamp with time zone,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Tabela de rate limits
create table if not exists rate_limits (
    id uuid default uuid_generate_v4() primary key,
    key text not null,
    timestamp timestamp with time zone default now()
);

-- Habilitar RLS (Row Level Security)
alter table cache enable row level security;
alter table rate_limits enable row level security;

-- Criar políticas de acesso
create policy "Cache é acessível por usuários autenticados"
on cache for all
using (auth.role() = 'authenticated');

create policy "Rate limits são acessíveis por usuários autenticados"
on rate_limits for all
using (auth.role() = 'authenticated');

-- Criar função para limpar cache expirado (executada via Supabase Edge Functions)
create or replace function cleanup_expired_cache()
returns void
security definer
set search_path = public
language plpgsql as $$
begin
    delete from cache where expires_at < now();
    delete from rate_limits where timestamp < now() - interval '1 day';
end;
$$;

-- Criar função para métricas do cache
create or replace function get_cache_metrics()
returns json
security definer
set search_path = public
language plpgsql as $$
declare
    result json;
begin
    select json_build_object(
        'total_items', count(*),
        'expired_items', count(*) filter (where expires_at < now()),
        'hit_rate', coalesce(
            sum(case when updated_at > created_at then 1 else 0 end)::float / 
            nullif(count(*), 0),
            0
        ),
        'size', sum(length(value::text))
    ) into result
    from cache;
    
    return result;
end;
$$; 