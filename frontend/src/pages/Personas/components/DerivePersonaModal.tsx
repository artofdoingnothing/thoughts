import { useState } from 'react';
import { useDerivePersona } from '../../../hooks/usePersonas';
import {
    Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
    Typography, Slider, Box
} from '@mui/material';



interface DerivePersonaModalProps {
    open: boolean;
    onClose: () => void;
    sourcePersonaId: number | null;
    sourcePersonaName: string;
}

export default function DerivePersonaModal({ open, onClose, sourcePersonaId, sourcePersonaName }: DerivePersonaModalProps) {
    const [nameAdjective, setNameAdjective] = useState('');
    const [percentage, setPercentage] = useState(30);

    const deriveMutation = useDerivePersona();

    const handleSubmit = async () => {
        if (!sourcePersonaId) return;

        try {
            await deriveMutation.mutateAsync({
                source_persona_id: sourcePersonaId,
                name_adjective: nameAdjective,
                percentage: percentage
            });
            onClose();
        } catch (error) {
            console.error('Error deriving persona:', error);
        }
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>Derive New Persona from {sourcePersonaName}</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    label="Adjective for Name (e.g. Angry, Creative)"
                    fullWidth
                    value={nameAdjective}
                    onChange={(e) => setNameAdjective(e.target.value)}
                />
                
                <Box sx={{ mt: 3 }}>
                    <Typography id="thought-percentage" gutterBottom>
                        Percentage of Thoughts to Sample ({percentage}%)
                    </Typography>
                    <Slider
                        value={percentage}
                        onChange={(_, newValue) => setPercentage(newValue as number)}
                        aria-labelledby="thought-percentage"
                        valueLabelDisplay="auto"
                        step={10}
                        marks
                        min={10}
                        max={100}
                    />
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={handleSubmit} variant="contained" disabled={!nameAdjective}>
                    Derive
                </Button>
            </DialogActions>
        </Dialog>
    );
}
