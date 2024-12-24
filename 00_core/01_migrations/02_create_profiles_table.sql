-- Criar tabela de perfis dos usuários
CREATE TABLE public.profiles (
    id uuid REFERENCES auth.users PRIMARY KEY,
    username text,
    first_name text,
    last_name text,
    email text UNIQUE,
    image_url text,
    created_at timestamptz DEFAULT now(),
    updated_at timestamptz DEFAULT now()
);

-- Criar função para atualizar o timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Criar trigger para atualizar o timestamp automaticamente
CREATE TRIGGER update_profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW
    EXECUTE PROCEDURE update_updated_at_column();

-- Habilitar RLS
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;

-- Criar políticas de acesso
CREATE POLICY "Usuários podem visualizar seu próprio perfil" 
    ON public.profiles FOR SELECT 
    USING (auth.uid() = id);

CREATE POLICY "Usuários podem atualizar seu próprio perfil" 
    ON public.profiles FOR UPDATE 
    USING (auth.uid() = id);

CREATE POLICY "Usuários podem inserir seu próprio perfil" 
    ON public.profiles FOR INSERT 
    WITH CHECK (auth.uid() = id);

-- Criar função para inserir perfil automaticamente quando um novo usuário é criado
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
    INSERT INTO public.profiles (id, email, username, first_name, last_name, image_url)
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

-- Criar trigger para criar perfil automaticamente
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user(); 