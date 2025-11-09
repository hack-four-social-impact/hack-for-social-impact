import React, { useState } from 'react';
import {
  Box,
  Button,
  Chip,
  Divider,
  Drawer,
  InputAdornment,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Paper,
  TextField,
  Typography,
  Avatar,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import PdfUploadModal from '../PdfUploadModal';

const clients = [
  {
    id: '1',
    name: 'Sarah Johnson',
    initials: 'SJ',
    caseNumber: '2024-CV-1234',
    documents: 12,
    status: 'active',
  },
  {
    id: '2',
    name: 'Michael Chen',
    initials: 'MC',
    caseNumber: '2024-CV-1235',
    documents: 8,
    status: 'active',
  },
  {
    id: '3',
    name: 'Emily Rodriguez',
    initials: 'ER',
    caseNumber: '2024-CV-1236',
    documents: 5,
    status: 'pending',
  },
];

const statusColor = {
  active: 'primary',
  pending: 'default',
};

function Dashboard() {
  const [search, setSearch] = useState('');
  const [selected, setSelected] = useState(clients[0]);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const filteredClients = clients.filter(
    (c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.caseNumber.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Box sx={{ display: 'flex', height: '100vh', bgcolor: '#fff' }}>
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: 300,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: 350, boxSizing: 'border-box', bgcolor: '#f7f8fa', borderRight: '1px solid #e4e7ec' },
        }}
      >
        <Box sx={{ p: 3, pb: 1 }}>
          <Typography variant="h5" fontWeight={700} sx={{ mb: 2, textAlign: 'left' }}>
            Clients
          </Typography>
          <TextField
            fullWidth
            placeholder="Search clients..."
            variant="outlined"
            size="small"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon color="action" />
                </InputAdornment>
              ),
            }}
            sx={{ bgcolor: '#fff' }}
          />
        </Box>
        <List sx={{ px: 2, flex: 1 }}>
          {filteredClients.map((client) => (
            <ListItem
              key={client.id}
              onClick={() => setSelected(client)}
              sx={{
                mb: 1,
                borderRadius: 2,
                bgcolor: selected.id === client.id ? '#ebeff6ff' : 'transparent',
                boxShadow: selected.id === client.id ? 1 : 0,
                cursor: 'pointer',
                transition: 'background 0.2s',
              }}
            >
              <ListItemAvatar>
                <Avatar>{client.initials}</Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography fontWeight={600}>{client.name}</Typography>
                    <Chip
                      label={client.status}
                      color={statusColor[client.status]}
                      size="small"
                      sx={{ textTransform: 'capitalize', fontWeight: 500 }}
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="body2" color="text.secondary">
                      Case #{client.caseNumber}
                    </Typography>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
        <Box sx={{ px: 2, pb: 3 }}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            sx={{ borderRadius: 2, py: 1.5, fontWeight: 600, fontSize: 16 }}
            onClick={() => setIsModalOpen(true)}
          >
            Upload Documents
          </Button>
        </Box>
      </Drawer>

      {/* Main Content */}
      <Box sx={{ flex: 1, p: 4 }}>
        {/* Header */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Typography variant="h5" fontWeight={700} sx={{ flex: 1 }}>
            JusticeAI
          </Typography>
        </Box>
        <Divider sx={{ mb: 3 }} />
        {/* Document Analysis Section */}
        <Paper elevation={2} sx={{ p: 4, borderRadius: 3, maxWidth: 700 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5" fontWeight={700} sx={{ flex: 1 }}>
              Case Analysis
            </Typography>
            <Button variant="contained" color="primary" sx={{ borderRadius: 2 }}>
              Export
            </Button>
          </Box>
          <Typography variant="subtitle1" color="text.secondary" sx={{ mb: 2 }}>
            Comprehensive legal document summary
          </Typography>
          <Divider sx={{ mb: 2 }} />
          <Box sx={{ display: 'flex', gap: 6, mb: 2 }}>
            <Box>
              <Typography fontWeight={600}>Client's Name & CDCR No.</Typography>
              <Typography>{selected.name} (A12345)</Typography>
            </Box>
            <Box>
              <Typography fontWeight={600}>Contact Information</Typography>
              <Typography>CDCR Incarcerated Person Locator</Typography>
            </Box>
            <Box>
              <Typography fontWeight={600}>Date of Birth</Typography>
              <Typography>March 15, 1985</Typography>
            </Box>
          </Box>
          <Divider sx={{ mb: 2 }} />
          <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1 }}>
            Introduction
          </Typography>
          <Typography sx={{ mb: 2 }}>
            {selected.name} was convicted of first-degree murder in 2010. The defense argued self-defense and presented alibi witnesses. {selected.name} maintains their innocence, stating they were at their workplace at the time of the incident and were misidentified by witnesses due to similar physical appearance to another individual in the area.
          </Typography>
          <Typography variant="subtitle1" fontWeight={600} sx={{ mb: 1 }}>
            Evidence Used to Convict
          </Typography>
          <ul>
            <li>Testimony from John Doe that placed defendant at the scene</li>
            <li>Eyewitness testimony from Jane Smith identifying the defendant</li>
            <li>Forensic evidence linking defendant to the crime scene</li>
          </ul>
        </Paper>
      </Box>

      {/* PDF Upload Modal */}
      <PdfUploadModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onUpload={() => setIsModalOpen(false)}
      />
    </Box>
  );
}

export default Dashboard;