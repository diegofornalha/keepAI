BEGIN;

CREATE TABLE IF NOT EXISTS public.notes (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES public.profiles(id),
    title VARCHAR(255) NOT NULL,
    content TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Configurar permissões
GRANT ALL ON public.notes TO authenticated;

COMMIT; 