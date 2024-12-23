import React from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper,
  Chip,
  IconButton,
} from '@mui/material';
import {
  CheckCircle as CheckCircleIcon,
  Schedule as ScheduleIcon,
  Delete as DeleteIcon,
} from '@mui/icons-material';

// Dados mockados para exemplo
const mockTasks = [
  {
    id: 1,
    title: 'Agendar reunião com equipe',
    status: 'completed',
    createdAt: '2024-01-20T10:00:00',
    completedAt: '2024-01-20T11:00:00',
    source: 'chat'
  },
  {
    id: 2,
    title: 'Preparar apresentação do projeto',
    status: 'pending',
    createdAt: '2024-01-19T15:30:00',
    source: 'note'
  },
  {
    id: 3,
    title: 'Revisar documentação',
    status: 'completed',
    createdAt: '2024-01-18T09:00:00',
    completedAt: '2024-01-18T14:00:00',
    source: 'chat'
  },
  // Mais tarefas mockadas...
];

const Tasks = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Tarefas
      </Typography>
      
      <Paper elevation={3} sx={{ p: 2 }}>
        <List>
          {mockTasks.map((task) => (
            <ListItem
              key={task.id}
              secondaryAction={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Chip
                    label={task.source}
                    size="small"
                    color={task.source === 'chat' ? 'primary' : 'secondary'}
                  />
                  <IconButton edge="end" aria-label="delete">
                    <DeleteIcon />
                  </IconButton>
                </Box>
              }
              sx={{
                mb: 1,
                backgroundColor: task.status === 'completed' ? 'action.hover' : 'background.paper',
                borderRadius: 1,
              }}
            >
              <ListItemIcon>
                {task.status === 'completed' ? (
                  <CheckCircleIcon color="success" />
                ) : (
                  <ScheduleIcon color="action" />
                )}
              </ListItemIcon>
              <ListItemText
                primary={task.title}
                secondary={
                  <>
                    Criada em: {new Date(task.createdAt).toLocaleDateString('pt-BR')}
                    {task.completedAt && (
                      <> • Concluída em: {new Date(task.completedAt).toLocaleDateString('pt-BR')}</>
                    )}
                  </>
                }
                sx={{
                  '& .MuiListItemText-primary': {
                    textDecoration: task.status === 'completed' ? 'line-through' : 'none',
                  },
                }}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
    </Box>
  );
};

export default Tasks; 