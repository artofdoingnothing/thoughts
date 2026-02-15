import React from 'react';
import type { Conversation } from '../../../types';
import { List, ListItemButton, ListItemText, Typography, Paper, Button, Box } from '@mui/material';

interface ConversationListProps {
  conversations: Conversation[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  onCreateNew: () => void;
}

const ConversationList: React.FC<ConversationListProps> = ({ conversations, selectedId, onSelect, onCreateNew }) => {
  return (
    <Paper sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Box sx={{ p: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="h6">Conversations</Typography>
            <Button variant="contained" size="small" onClick={onCreateNew}>New</Button>
        </Box>
      <List sx={{ flexGrow: 1, overflowY: 'auto' }}>
        {conversations.map((conversation) => (
          <ListItemButton
            key={conversation.id}
            selected={selectedId === conversation.id}
            onClick={() => onSelect(conversation.id)}
          >
            <ListItemText
              primary={conversation.title}
              secondary={new Date(conversation.created_at).toLocaleString()}
              primaryTypographyProps={{ noWrap: true }}
            />
          </ListItemButton>
        ))}
        {conversations.length === 0 && (
            <Typography variant="body2" sx={{ p: 2, color: 'text.secondary' }}>
                No conversations yet.
            </Typography>
        )}
      </List>
    </Paper>
  );
};

export default ConversationList;
