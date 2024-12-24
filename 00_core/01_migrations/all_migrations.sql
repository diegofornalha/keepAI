-- Combinação de todas as migrações em ordem
-- Executar este arquivo irá criar toda a estrutura do banco de dados

-- 00. Criar schemas
\i 00_create_schemas.sql

-- 01. Criar tabela de notas
\i 01_create_notes_table.sql

-- 02. Criar tabela de perfis
\i 02_create_profiles_table.sql

-- 03. Criar tabelas de IA
\i 03_create_ai_tables.sql

-- 04. Criar tabelas de tarefas
\i 04_create_tasks_tables.sql

-- Confirmar transação
COMMIT; 