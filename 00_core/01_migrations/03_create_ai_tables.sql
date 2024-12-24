-- Tabelas para o serviço de IA
CREATE TABLE ai.conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    model_used TEXT DEFAULT 'gemini-pro',
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Índices
CREATE INDEX idx_ai_conversations_user_id ON ai.conversations(user_id);
CREATE INDEX idx_ai_conversations_created_at ON ai.conversations(created_at DESC);

-- RLS
ALTER TABLE ai.conversations ENABLE ROW LEVEL SECURITY;

-- Políticas
CREATE POLICY "Users can manage their own conversations" ON ai.conversations
    FOR ALL
    USING (auth.uid()::text = user_id)
    WITH CHECK (auth.uid()::text = user_id); 