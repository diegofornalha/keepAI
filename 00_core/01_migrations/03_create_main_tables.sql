BEGIN;

-- Drop the notes table if it exists
DROP TABLE IF EXISTS notes.notes;

-- Create the notes table
CREATE TABLE notes.notes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notes_user_id ON notes.notes(user_id);
ALTER TABLE notes.notes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own notes" ON notes.notes
    FOR ALL
    USING (auth.uid()::text = user_id)
    WITH CHECK (auth.uid()::text = user_id);

-- Drop the conversations table if it exists
DROP TABLE IF EXISTS ai.conversations;

-- Create the conversations table
CREATE TABLE ai.conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    message TEXT NOT NULL,
    response TEXT,
    created_at TIMESTAMPTZ DEFAULT now(),
    model_used TEXT DEFAULT 'gemini-pro',
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_ai_conversations_user_id ON ai.conversations(user_id);
CREATE INDEX idx_ai_conversations_created_at ON ai.conversations(created_at DESC);
ALTER TABLE ai.conversations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own conversations" ON ai.conversations
    FOR ALL
    USING (auth.uid()::text = user_id)
    WITH CHECK (auth.uid()::text = user_id);

-- Drop the tasks table if it exists
DROP TABLE IF EXISTS tasks.tasks;

-- Create the tasks table
CREATE TABLE tasks.tasks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    priority TEXT DEFAULT 'medium',
    due_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_tasks_user_id ON tasks.tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks.tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks.tasks(due_date);
ALTER TABLE tasks.tasks ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can manage their own tasks" ON tasks.tasks
    FOR ALL
    USING (auth.uid()::text = user_id)
    WITH CHECK (auth.uid()::text = user_id);

COMMIT;