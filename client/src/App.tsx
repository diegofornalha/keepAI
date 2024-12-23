import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import {
  Box,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Typography,
  CssBaseline,
  AppBar,
  Toolbar,
} from '@mui/material';
import {
  Chat as ChatIcon,
  Note as NoteIcon,
  Event as EventIcon,
  Assignment as AssignmentIcon,
} from '@mui/icons-material';

import NotesHistory from './pages/NotesHistory';
import CalendarView from './pages/Calendar';
import Tasks from './pages/Tasks';

const drawerWidth = 240;

const App = () => {
  const menuItems = [
    { text: 'Chat & Notas', icon: <ChatIcon />, path: '/' },
    { text: 'Histórico de Notas', icon: <NoteIcon />, path: '/notes' },
    { text: 'Calendário', icon: <EventIcon />, path: '/calendar' },
    { text: 'Tarefas', icon: <AssignmentIcon />, path: '/tasks' },
  ];

  return (
    <Router>
      <Box sx={{ display: 'flex' }}>
        <CssBaseline />
        
        {/* AppBar */}
        <AppBar
          position="fixed"
          sx={{ width: `calc(100% - ${drawerWidth}px)`, ml: `${drawerWidth}px` }}
        >
          <Toolbar>
            <Typography variant="h6" noWrap component="div">
              KeepAI
            </Typography>
          </Toolbar>
        </AppBar>

        {/* Drawer */}
        <Drawer
          sx={{
            width: drawerWidth,
            flexShrink: 0,
            '& .MuiDrawer-paper': {
              width: drawerWidth,
              boxSizing: 'border-box',
            },
          }}
          variant="permanent"
          anchor="left"
        >
          <Toolbar />
          <List>
            {menuItems.map((item) => (
              <ListItem
                button
                key={item.text}
                component={Link}
                to={item.path}
                sx={{
                  '&:hover': {
                    backgroundColor: 'action.hover',
                  },
                }}
              >
                <ListItemIcon>{item.icon}</ListItemIcon>
                <ListItemText primary={item.text} />
              </ListItem>
            ))}
          </List>
        </Drawer>

        {/* Main Content */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            bgcolor: 'background.default',
            p: 3,
            width: `calc(100% - ${drawerWidth}px)`,
            ml: `${drawerWidth}px`,
            mt: '64px',
          }}
        >
          <Routes>
            <Route path="/notes" element={<NotesHistory />} />
            <Route path="/calendar" element={<CalendarView />} />
            <Route path="/tasks" element={<Tasks />} />
          </Routes>
        </Box>
      </Box>
    </Router>
  );
};

export default App; 