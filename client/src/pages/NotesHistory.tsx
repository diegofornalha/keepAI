import React from 'react';
import { Box, Typography, List, ListItem, Paper, Divider } from '@mui/material';

// Dados mockados para exemplo
const mockNotes = [
  {
    id: 1,
    title: 'Reunião de Projeto',
    content: 'Discutir próximos passos do projeto KeepAI',
    createdAt: '2024-01-20T10:00:00',
    tags: ['trabalho', 'projeto']
  },
  {
    id: 2,
    title: 'Lista de Compras',
    content: 'Leite, pão, frutas, verduras',
    createdAt: '2024-01-19T15:30:00',
    tags: ['pessoal', 'compras']
  },
  // Mais notas mockadas...
];

const NotesHistory = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Histórico de Notas
      </Typography>
      
      <List>
        {mockNotes.map((note) => (
          <React.Fragment key={note.id}>
            <Paper elevation={2} sx={{ mb: 2, p: 2 }}>
              <Typography variant="h6">{note.title}</Typography>
              <Typography variant="body2" color="text.secondary">
                {new Date(note.createdAt).toLocaleDateString('pt-BR', {
                  day: '2-digit',
                  month: '2-digit',
                  year: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </Typography>
              <Typography variant="body1" sx={{ mt: 1 }}>
                {note.content}
              </Typography>
              <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                {note.tags.map((tag) => (
                  <Typography
                    key={tag}
                    variant="caption"
                    sx={{
                      backgroundColor: 'primary.light',
                      color: 'white',
                      px: 1,
                      py: 0.5,
                      borderRadius: 1
                    }}
                  >
                    {tag}
                  </Typography>
                ))}
              </Box>
            </Paper>
            <Divider sx={{ my: 2 }} />
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default NotesHistory; 