BEGIN;

-- Tabela de perfis (users)
CREATE TABLE users.profiles (
    id uuid REFERENCES auth.users PRIMARY KEY,
    username text,
    first_name text,
    last_name text,
    email text UNIQUE,
    image_url text,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Função de timestamp
CREATE OR REPLACE FUNCTION users.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger de timestamp
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON users.profiles
    FOR EACH ROW
    EXECUTE PROCEDURE users.update_updated_at_column();

-- RLS para profiles
ALTER TABLE users.profiles ENABLE ROW LEVEL SECURITY;

-- Políticas para profiles
CREATE POLICY "Usuários podem visualizar seu próprio perfil" 
    ON users.profiles FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Usuários podem atualizar seu próprio perfil" 
    ON users.profiles FOR UPDATE 
    USING (auth.uid() = id);

CREATE POLICY "Usuários podem inserir seu próprio perfil" 
    ON users.profiles FOR INSERT 
    WITH CHECK (auth.uid() = id);

COMMIT;