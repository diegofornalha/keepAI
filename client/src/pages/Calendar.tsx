import React from 'react';
import { Box, Typography, Paper } from '@mui/material';
import { Calendar as BigCalendar, dateFnsLocalizer } from 'react-big-calendar';
import format from 'date-fns/format';
import parse from 'date-fns/parse';
import startOfWeek from 'date-fns/startOfWeek';
import getDay from 'date-fns/getDay';
import ptBR from 'date-fns/locale/pt-BR';
import 'react-big-calendar/lib/css/react-big-calendar.css';

const locales = {
  'pt-BR': ptBR,
};

const localizer = dateFnsLocalizer({
  format,
  parse,
  startOfWeek,
  getDay,
  locales,
});

// Dados mockados para exemplo
const mockEvents = [
  {
    id: 1,
    title: 'Nota: Reunião de Projeto',
    start: new Date(2024, 0, 20, 10, 0),
    end: new Date(2024, 0, 20, 11, 0),
    type: 'note'
  },
  {
    id: 2,
    title: 'Nota: Lista de Compras',
    start: new Date(2024, 0, 19, 15, 30),
    end: new Date(2024, 0, 19, 16, 0),
    type: 'note'
  },
  // Mais eventos mockados...
];

const CalendarView = () => {
  return (
    <Box sx={{ p: 3, height: 'calc(100vh - 100px)' }}>
      <Typography variant="h4" gutterBottom>
        Calendário de Notas
      </Typography>
      
      <Paper elevation={3} sx={{ p: 2, height: 'calc(100% - 60px)' }}>
        <BigCalendar
          localizer={localizer}
          events={mockEvents}
          startAccessor="start"
          endAccessor="end"
          style={{ height: '100%' }}
          messages={{
            next: "Próximo",
            previous: "Anterior",
            today: "Hoje",
            month: "Mês",
            week: "Semana",
            day: "Dia",
            agenda: "Agenda",
            date: "Data",
            time: "Hora",
            event: "Evento",
            noEventsInRange: "Não há eventos neste período."
          }}
          eventPropGetter={(event) => ({
            style: {
              backgroundColor: event.type === 'note' ? '#3f51b5' : '#f50057',
            },
          })}
        />
      </Paper>
    </Box>
  );
};

export default CalendarView; 