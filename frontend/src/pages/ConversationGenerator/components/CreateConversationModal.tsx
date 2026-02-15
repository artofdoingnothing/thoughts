import React, { useState } from 'react';
import { Modal, Box, Typography, TextField, Button, Select, MenuItem, Chip, OutlinedInput, InputLabel, FormControl } from '@mui/material';
import type { SelectChangeEvent } from '@mui/material';
import type { Persona } from '../../../types';

interface CreateConversationModalProps {
  open: boolean;
  onClose: () => void;
  onCreate: (title: string, context: string, personaIds: number[]) => void;
  personas: Persona[];
}

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 500,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
  display: 'flex',
  flexDirection: 'column',
  gap: 2,
};

const CreateConversationModal: React.FC<CreateConversationModalProps> = ({ open, onClose, onCreate, personas }) => {
  const [title, setTitle] = useState('');
  const [context, setContext] = useState('');
  const [selectedPersonaIds, setSelectedPersonaIds] = useState<number[]>([]);

  const handlePersonaChange = (event: SelectChangeEvent<number[]>) => {
    const {
      target: { value },
    } = event;
    setSelectedPersonaIds(
      // On autofill we get a stringified value.
      typeof value === 'string' ? value.split(',').map(Number) : value,
    );
  };

  const handleCreate = () => {
      if (title && context && selectedPersonaIds.length >= 2) {
          onCreate(title, context, selectedPersonaIds);
          // Reset
          setTitle('');
          setContext('');
          setSelectedPersonaIds([]);
          onClose();
      }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography variant="h6" component="h2">
          Create New Conversation
        </Typography>
        <TextField
          label="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          fullWidth
        />
        <TextField
          label="Context / Starting Point"
          value={context}
          onChange={(e) => setContext(e.target.value)}
          multiline
          rows={3}
          fullWidth
          helperText="Provide a paragraph as a starting point for the conversation."
        />
        <FormControl fullWidth>
            <InputLabel>Select Personas (Min 2)</InputLabel>
            <Select
                multiple
                value={selectedPersonaIds}
                onChange={handlePersonaChange}
                input={<OutlinedInput label="Select Personas (Min 2)" />}
                renderValue={(selected) => (
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => {
                        const persona = personas.find(p => p.id === value);
                        return <Chip key={value} label={persona?.name} />;
                    })}
                    </Box>
                )}
            >
                {personas.map((persona) => (
                    <MenuItem key={persona.id} value={persona.id}>
                        {persona.name}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
        <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 1, mt: 2 }}>
            <Button onClick={onClose}>Cancel</Button>
            <Button 
                variant="contained" 
                onClick={handleCreate} 
                disabled={!title || !context || selectedPersonaIds.length < 2}
            >
                Create
            </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default CreateConversationModal;
