import React, { useState } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  Chip,
  IconButton
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import type { Persona } from '../../../types';

interface SequenceGeneratorModalProps {
  open: boolean;
  onClose: () => void;
  onGenerate: (sequencePersonaIds: number[]) => void;
  personas: Persona[];
}

const SequenceGeneratorModal: React.FC<SequenceGeneratorModalProps> = ({
  open,
  onClose,
  onGenerate,
  personas,
}) => {
  const [sequence, setSequence] = useState<Persona[]>([]);

  const handleAddPersona = (persona: Persona) => {
    setSequence((prev) => [...prev, persona]);
  };

  const handleClearSequence = () => {
    setSequence([]);
  };

  const handleGenerate = () => {
    if (sequence.length > 0) {
      onGenerate(sequence.map((p) => p.id));
      handleClose();
    }
  };

  const handleClose = () => {
    setSequence([]);
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">Sequence Generator</Typography>
          <IconButton onClick={handleClose} size="small">
            <CloseIcon />
          </IconButton>
        </Box>
      </DialogTitle>
      
      <DialogContent dividers>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Click personas below to add them to the generation sequence. Messages will be generated in the exact order you specify.
        </Typography>

        <Box sx={{ my: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
          {personas.map((persona) => (
            <Button
              key={persona.id}
              variant="outlined"
              size="small"
              onClick={() => handleAddPersona(persona)}
            >
              + {persona.name}
            </Button>
          ))}
        </Box>

        <Typography variant="subtitle2" sx={{ mt: 3, mb: 1 }}>
          Current Sequence:
        </Typography>
        
        <Box
          sx={{
            p: 2,
            border: '1px dashed',
            borderColor: 'divider',
            borderRadius: 1,
            minHeight: 80,
            display: 'flex',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: 1,
            bgcolor: 'var(--background-paper)',
          }}
        >
          {sequence.length === 0 ? (
            <Typography variant="body2" color="text.secondary" sx={{ fontStyle: 'italic', width: '100%', textAlign: 'center' }}>
              Sequence is empty. Add personas to build the sequence.
            </Typography>
          ) : (
            sequence.map((p, index) => (
              <React.Fragment key={`${p.id}-${index}`}>
                <Chip label={p.name} color="primary" />
                {index < sequence.length - 1 && <ArrowForwardIcon fontSize="small" color="disabled" />}
              </React.Fragment>
            ))
          )}
        </Box>
      </DialogContent>

      <DialogActions sx={{ px: 3, py: 2 }}>
        <Button onClick={handleClearSequence} color="inherit" disabled={sequence.length === 0}>
          Clear
        </Button>
        <Box sx={{ flexGrow: 1 }} />
        <Button onClick={handleClose} color="inherit">
          Cancel
        </Button>
        <Button
          onClick={handleGenerate}
          variant="contained"
          color="primary"
          disabled={sequence.length === 0}
        >
          Generate Sequence
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default SequenceGeneratorModal;
