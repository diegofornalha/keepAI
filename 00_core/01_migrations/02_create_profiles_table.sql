-- Mover para schema users
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

-- Função para atualizar timestamp
CREATE OR REPLACE FUNCTION users.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para timestamp
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON users.profiles
    FOR EACH ROW
    EXECUTE PROCEDURE users.update_updated_at_column();

-- Habilitar RLS
ALTER TABLE users.profiles ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso
CREATE POLICY "Usuários podem visualizar seu próprio perfil" 
    ON users.profiles FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Usuários podem atualizar seu próprio perfil" 
    ON users.profiles FOR UPDATE 
    USING (auth.uid() = id);

CREATE POLICY "Usuários podem inserir seu próprio perfil" 
    ON users.profiles FOR INSERT 
    WITH CHECK (auth.uid() = id);

-- Função para novo usuário
CREATE OR REPLACE FUNCTION users.handle_new_user()
RETURNS trigger AS $$
BEGIN
    INSERT INTO users.profiles (id, email, username, first_name, last_name, image_url)
    VALUES (
        new.id,
        new.raw_user_meta_data->>'email',
        new.raw_user_meta_data->>'username',
        new.raw_user_meta_data->>'first_name',
        new.raw_user_meta_data->>'last_name',
        new.raw_user_meta_data->>'image_url'
    );
    RETURN new;
END;
$$ language plpgsql security definer;

-- Trigger para criar perfil
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE users.handle_new_user(); 
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user(); 