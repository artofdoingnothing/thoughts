import React, { useState, useEffect, useRef } from 'react';
import { Box, Typography, Paper, Button, Chip } from '@mui/material';
import axios from 'axios';
import ConversationList from './components/ConversationList';
import CreateConversationModal from './components/CreateConversationModal';
import AddPersonaModal from './components/AddPersonaModal';
import type { Conversation, Persona, Message } from '../../types';
// Icons
// import SendIcon from '@mui/icons-material/Send'; // Assuming material icons might be available or not, avoiding imports if not sure. 
// Using text buttons for safety if icons not installed.

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const ConversationGenerator: React.FC = () => {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [personas, setPersonas] = useState<Persona[]>([]);
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isAddPersonaModalOpen, setIsAddPersonaModalOpen] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const selectedConversation = conversations.find(c => c.id === selectedConversationId);

  useEffect(() => {
    fetchConversations();
    fetchPersonas();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [selectedConversation?.messages]);

  const fetchConversations = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/conversations/`);
      setConversations(response.data);
    } catch (error) {
      console.error('Error fetching conversations:', error);
    }
  };

  const fetchPersonas = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/personas/`);
      setPersonas(response.data);
    } catch (error) {
      console.error('Error fetching personas:', error);
    }
  };

  const handleCreateConversation = async (title: string, context: string, personaIds: number[]) => {
    try {
      await axios.post(`${API_BASE_URL}/conversations/`, { title, context, persona_ids: personaIds });
      fetchConversations();
    } catch (error) {
      console.error('Error creating conversation:', error);
    }
  };

  const handleGenerateMessage = async (personaId: number) => {
    if (!selectedConversationId) return;
    try {
      await axios.post(`${API_BASE_URL}/conversations/${selectedConversationId}/generate`, { persona_id: personaId });
      // Poll or re-fetch? For now re-fetch after a delay or optimistically?
      // Since it's async worker, we should probably poll.
      // For simplicity, let's just alert user or show loading state?
      // Better: Poll every few seconds if active.
      // Let's just trigger a fetch after 2 seconds for demo purposes.
      setTimeout(fetchConversations, 2000);
      setTimeout(fetchConversations, 5000);
    } catch (error) {
      console.error('Error generating message:', error);
    }
  };

  const handleAddPersona = async (personaId: number) => {
      if (!selectedConversationId) return;
      try {
          await axios.post(`${API_BASE_URL}/conversations/${selectedConversationId}/personas`, { persona_id: personaId });
          fetchConversations();
      } catch (error) {
          console.error('Error adding persona:', error);
      }
  };

  const handleEndConversation = async () => {
      if (!selectedConversationId) return;
      if (!window.confirm("Are you sure? This will convert all messages to thoughts.")) return;
      
      try {
          await axios.post(`${API_BASE_URL}/conversations/${selectedConversationId}/end`);
          alert("Conversation ended and thoughts created!");
          // Maybe refresh thoughts?
      } catch (error) {
          console.error('Error ending conversation:', error);
      }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <Box sx={{ display: 'flex', height: 'calc(100vh - 100px)', gap: 2, p: 2 }}>
      {/* Sidebar */}
      <Box sx={{ width: 300, flexShrink: 0 }}>
        <ConversationList
          conversations={conversations}
          selectedId={selectedConversationId}
          onSelect={setSelectedConversationId}
          onCreateNew={() => setIsCreateModalOpen(true)}
        />
      </Box>

      {/* Main Chat Area */}
      <Paper sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column', p: 2 }}>
        {selectedConversation ? (
          <>
            {/* Header */}
            <Box sx={{ mb: 2, borderBottom: 1, borderColor: 'divider', pb: 1 }}>
              <Typography variant="h5">{selectedConversation.title}</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                {selectedConversation.context}
              </Typography>
              
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, alignItems: 'center' }}>
                <Typography variant="subtitle2">Participants:</Typography>
                {selectedConversation.personas.map(p => (
                  <Chip key={p.id} label={p.name} size="small" />
                ))}
                <Button size="small" onClick={() => setIsAddPersonaModalOpen(true)}>+ Add</Button>
                <Box sx={{ flexGrow: 1 }} />
                <Button variant="outlined" color="error" size="small" onClick={handleEndConversation}>
                    End Conversation
                </Button>
              </Box>
            </Box>

            {/* Messages */}
            <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2, display: 'flex', flexDirection: 'column', gap: 1 }}>
                {selectedConversation.messages.map((msg: Message) => (
                    <Paper 
                        key={msg.id} 
                        sx={{ 
                            p: 2, 
                            maxWidth: '80%', 
                            alignSelf: 'flex-start',
                            bgcolor: 'grey.100' // Neutral background
                        }}
                    >
                        <Typography variant="subtitle2" color="primary">
                            {msg.persona?.name || 'Unknown'}
                        </Typography>
                        <Typography variant="body1">
                            {msg.content}
                        </Typography>
                         <Typography variant="caption" color="text.secondary">
                            {new Date(msg.created_at).toLocaleTimeString()}
                        </Typography>
                    </Paper>
                ))}
                {selectedConversation.messages.length === 0 && (
                    <Typography color="text.secondary" align="center" sx={{ mt: 4 }}>
                        No messages yet. Start by generating one!
                    </Typography>
                )}
                <div ref={messagesEndRef} />
            </Box>

            {/* Controls */}
            <Paper variant="outlined" sx={{ p: 2, display: 'flex', gap: 1, alignItems: 'center' }}>
                <Typography variant="body2">Generate response for:</Typography>
                {selectedConversation.personas.map(p => (
                    <Button 
                        key={p.id} 
                        variant="outlined" 
                        size="small"
                        onClick={() => handleGenerateMessage(p.id)}
                    >
                        {p.name}
                    </Button>
                ))}
            </Paper>
          </>
        ) : (
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
            <Typography variant="h6" color="text.secondary">
              Select or create a conversation to start.
            </Typography>
          </Box>
        )}
      </Paper>

      {/* Modals */}
      <CreateConversationModal
        open={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onCreate={handleCreateConversation}
        personas={personas}
      />
      
      <AddPersonaModal 
        open={isAddPersonaModalOpen}
        onClose={() => setIsAddPersonaModalOpen(false)}
        onAdd={handleAddPersona}
        personas={personas}
        currentPersonaIds={selectedConversation?.personas.map(p => p.id) || []}
      />

    </Box>
  );
};

export default ConversationGenerator;
