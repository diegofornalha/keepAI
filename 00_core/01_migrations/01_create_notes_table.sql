-- Mover para schema notes
CREATE TABLE IF NOT EXISTS notes.notes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Criar índice para busca por usuário
CREATE INDEX IF NOT EXISTS idx_notes_user_id ON notes.notes(user_id);

-- Habilitar RLS
ALTER TABLE notes.notes ENABLE ROW LEVEL SECURITY;

-- Criar política de acesso
CREATE POLICY "Users can manage their own notes" ON notes.notes
    FOR ALL
    USING (auth.uid()::text = user_id)
    WITH CHECK (auth.uid()::text = user_id); 