import React, { useState, useEffect, useRef } from 'react';
import { Box, Typography, Paper, Button, Chip, CircularProgress } from '@mui/material';
import { jsPDF } from 'jspdf';
import ConversationList from './components/ConversationList';
import CreateConversationModal from './components/CreateConversationModal';
import AddPersonaModal from './components/AddPersonaModal';
import SequenceGeneratorModal from './components/SequenceGeneratorModal';
import type { Message } from '../../types';
import { usePersonas } from '../../hooks/usePersonas';
import { 
    useConversations, 
    useCreateConversation, 
    useGenerateMessage, 
    useAddPersonaToConversation, 
    useGenerateSequence, 
    useEndConversation 
} from '../../hooks/useConversations';

// Soft neutral pastel colors for distinguishing message owners
const PERSONA_COLORS = [
  '#f0f4f8', // Cool Grey
  '#fef9ef', // Warm Cream
  '#f0fdf4', // Soft Mint
  '#fdf2f8', // Soft Pink
  '#eff6ff', // Light Sky
  '#fefce8', // Pale Yellow
  '#f5f3ff', // Lavender
  '#ecfdf5', // Sea Foam
  '#fff7ed', // Peach
  '#f1f5f9', // Slate Grey
];

const getPersonaColor = (personaId: number): string => {
  return PERSONA_COLORS[personaId % PERSONA_COLORS.length];
};
// Icons
// import SendIcon from '@mui/icons-material/Send'; // Assuming material icons might be available or not, avoiding imports if not sure. 
// Using text buttons for safety if icons not installed.

const ConversationGenerator: React.FC = () => {
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(null);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isAddPersonaModalOpen, setIsAddPersonaModalOpen] = useState(false);
  const [isSequenceModalOpen, setIsSequenceModalOpen] = useState(false);
  const [isPolling, setIsPolling] = useState(false);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const { data: personas = [] } = usePersonas();
  const { data: conversations = [], isLoading: isLoadingConversations } = useConversations(isPolling ? 2000 : false);

  const createMutation = useCreateConversation();
  const generateMessageMutation = useGenerateMessage();
  const addPersonaMutation = useAddPersonaToConversation();
  const sequenceMutation = useGenerateSequence();
  const endMutation = useEndConversation();

  const selectedConversation = conversations.find(c => c.id === selectedConversationId);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [selectedConversation?.messages]);

  const startPolling = () => {
      setIsPolling(true);
      setTimeout(() => setIsPolling(false), 10000);
  };

  const handleCreateConversation = (title: string, context: string, personaIds: number[]) => {
      createMutation.mutate({ title, context, persona_ids: personaIds });
  };

  const handleGenerateMessage = (personaId: number) => {
    if (!selectedConversationId) return;
    generateMessageMutation.mutate({ conversationId: selectedConversationId, personaId }, {
        onSuccess: () => startPolling()
    });
  };

  const handleAddPersona = (personaId: number) => {
      if (!selectedConversationId) return;
      addPersonaMutation.mutate({ conversationId: selectedConversationId, personaId });
  };

  const handleGenerateSequence = (personaIds: number[]) => {
      if (!selectedConversationId) return;
      sequenceMutation.mutate({ conversationId: selectedConversationId, personaIds }, {
          onSuccess: () => startPolling()
      });
  };

  const handleEndConversation = () => {
      if (!selectedConversationId) return;
      if (!window.confirm("Are you sure? This will convert all messages to thoughts.")) return;
      endMutation.mutate(selectedConversationId, {
          onSuccess: () => alert("Conversation ended and thoughts created!"),
          onError: () => alert("Error ending conversation")
      });
  };

  const handleDownloadPdf = () => {
    if (!selectedConversation) return;

    const doc = new jsPDF();
    const margin = 15;
    const pageWidth = doc.internal.pageSize.getWidth();
    const maxWidth = pageWidth - margin * 2;
    let yPosition = margin;

    // Title
    doc.setFontSize(20);
    doc.setFont("helvetica", "bold");
    const titleLines = doc.splitTextToSize(selectedConversation.title, maxWidth);
    doc.text(titleLines, margin, yPosition);
    yPosition += titleLines.length * 10;

    // Context
    doc.setFontSize(12);
    doc.setFont("helvetica", "italic");
    doc.setTextColor(100);
    const contextLines = doc.splitTextToSize(selectedConversation.context, maxWidth);
    doc.text(contextLines, margin, yPosition);
    yPosition += contextLines.length * 8 + 10;

    // Date
    doc.setFontSize(10);
    doc.setFont("helvetica", "normal");
    const dateStr = `Exported on: ${new Date().toLocaleString()}`;
    doc.text(dateStr, margin, yPosition);
    yPosition += 15;

    doc.setTextColor(0);

    // Messages
    const messages = [...selectedConversation.messages].sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime());

    for (const msg of messages) {
        // Persona Name and Timestamp
        doc.setFontSize(11);
        doc.setFont("helvetica", "bold");
        const headerText = `${msg.persona?.name || 'Unknown'} - ${new Date(msg.created_at).toLocaleString()}`;
        
        // Check page break
        if (yPosition + 10 > doc.internal.pageSize.getHeight() - margin) {
            doc.addPage();
            yPosition = margin;
        }
        
        doc.text(headerText, margin, yPosition);
        yPosition += 6;

        // Content
        doc.setFontSize(10);
        doc.setFont("helvetica", "normal");
        const contentLines = doc.splitTextToSize(msg.content, maxWidth);
        
        for (const line of contentLines) {
             if (yPosition + 7 > doc.internal.pageSize.getHeight() - margin) {
                doc.addPage();
                yPosition = margin;
            }
            doc.text(line, margin, yPosition);
            yPosition += 6;
        }
        yPosition += 8; // Space between messages
    }

    doc.save(`${selectedConversation.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.pdf`);
  };

  return (
    <Box sx={{ display: 'flex', height: 'calc(100vh - 100px)', gap: 2, p: 2 }}>
      {/* Sidebar */}
      <Box sx={{ width: 300, flexShrink: 0 }}>
        {isLoadingConversations ? (
             <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>
        ) : (
            <ConversationList
              conversations={conversations}
              selectedId={selectedConversationId}
              onSelect={setSelectedConversationId}
              onCreateNew={() => setIsCreateModalOpen(true)}
            />
        )}
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
                <Button variant="outlined" color="primary" size="small" onClick={handleDownloadPdf}>
                    Download PDF
                </Button>
                <Button variant="outlined" color="error" size="small" onClick={handleEndConversation}>
                    End Conversation
                </Button>
              </Box>
            </Box>

            {/* Messages */}
            <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2, display: 'flex', flexDirection: 'column' }}>
                {[...selectedConversation.messages]
                  .sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
                  .map((msg: Message, index: number, sortedArr: Message[]) => {
                    const prevMsg = index > 0 ? sortedArr[index - 1] : null;
                    const isConsecutive = prevMsg && prevMsg.persona?.id === msg.persona?.id;
                    const personaColor = getPersonaColor(msg.persona_id);

                    return (
                    <Box
                        key={msg.id}
                        sx={{
                            display: 'flex',
                            width: '100%',
                            mt: isConsecutive ? 0 : 0.5,
                        }}
                    >
                        {/* Left accent bar */}
                        <Box
                            sx={{
                                width: 4,
                                flexShrink: 0,
                                bgcolor: isConsecutive ? 'transparent' : personaColor,
                                borderRadius: '2px',
                            }}
                        />
                        {/* Message content */}
                        <Box
                            sx={{
                                flexGrow: 1,
                                py: isConsecutive ? 0.25 : 1,
                                px: 2,
                                bgcolor: personaColor,
                                borderBottom: '1px solid',
                                borderColor: 'divider',
                                '&:hover': {
                                    bgcolor: `color-mix(in srgb, ${personaColor} 85%, #9ca3af)`,
                                },
                                transition: 'background-color 0.15s ease',
                            }}
                        >
                            {!isConsecutive && (
                                <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 1, mb: 0.25 }}>
                                    <Typography
                                        variant="subtitle2"
                                        sx={{ fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.4 }}
                                    >
                                        {msg.persona?.name || 'Unknown'}
                                    </Typography>
                                    <Typography variant="caption" sx={{ color: 'var(--text-muted)', fontSize: '0.7rem' }}>
                                        {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </Typography>
                                </Box>
                            )}
                            <Typography
                                variant="body2"
                                sx={{ color: 'var(--text-secondary)', lineHeight: 1.5, wordBreak: 'break-word' }}
                            >
                                {msg.content}
                            </Typography>
                        </Box>
                    </Box>
                    );
                })}
                {selectedConversation.messages.length === 0 && (
                    <Typography color="text.secondary" align="center" sx={{ mt: 4 }}>
                        No messages yet. Start by generating one!
                    </Typography>
                )}
                <div ref={messagesEndRef} />
            </Box>

            {/* Controls */}
            <Paper variant="outlined" sx={{ p: 2, display: 'flex', gap: 1, alignItems: 'center', flexWrap: 'wrap' }}>
                <Typography variant="body2">Generate response for:</Typography>
                {selectedConversation.personas.map(p => (
                    <Button 
                        key={p.id} 
                        variant="outlined" 
                        size="small"
                        onClick={() => handleGenerateMessage(p.id)}
                        disabled={generateMessageMutation.isPending || isPolling}
                    >
                        {p.name}
                    </Button>
                ))}
                <Box sx={{ flexGrow: 1 }} />
                <Button 
                    variant="contained" 
                    color="secondary" 
                    size="small"
                    onClick={() => setIsSequenceModalOpen(true)}
                    disabled={sequenceMutation.isPending || isPolling}
                >
                    Sequence Generator
                </Button>
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

      <SequenceGeneratorModal
        open={isSequenceModalOpen}
        onClose={() => setIsSequenceModalOpen(false)}
        onGenerate={handleGenerateSequence}
        personas={selectedConversation?.personas || []}
      />

    </Box>
  );
};

export default ConversationGenerator;
