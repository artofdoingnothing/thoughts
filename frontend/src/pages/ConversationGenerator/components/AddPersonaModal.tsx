import React, { useState } from 'react';
import { Modal, Box, Typography, Button, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import type { Persona } from '../../../types';

interface AddPersonaModalProps {
  open: boolean;
  onClose: () => void;
  onAdd: (personaId: number) => void;
  personas: Persona[];
  currentPersonaIds: number[];
}

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
  display: 'flex',
  flexDirection: 'column',
  gap: 2,
};

const AddPersonaModal: React.FC<AddPersonaModalProps> = ({ open, onClose, onAdd, personas, currentPersonaIds }) => {
  const [selectedPersonaId, setSelectedPersonaId] = useState<number | ''>('');

  const availablePersonas = personas.filter(p => !currentPersonaIds.includes(p.id));

  const handleAdd = () => {
    if (selectedPersonaId) {
      onAdd(Number(selectedPersonaId));
      setSelectedPersonaId('');
      onClose();
    }
  };

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography variant="h6" component="h2">
          Add Persona to Conversation
        </Typography>
        
        <FormControl fullWidth>
            <InputLabel>Select Persona</InputLabel>
            <Select
                value={selectedPersonaId}
                label="Select Persona"
                onChange={(e) => setSelectedPersonaId(Number(e.target.value))}
            >
                {availablePersonas.map((persona) => (
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
                onClick={handleAdd} 
                disabled={!selectedPersonaId}
            >
                Add
            </Button>
        </Box>
      </Box>
    </Modal>
  );
};

export default AddPersonaModal;
