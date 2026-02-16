import { useState } from 'react';
import {
    Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
    Typography, Slider, Box
} from '@mui/material';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface DerivePersonaModalProps {
    open: boolean;
    onClose: () => void;
    onSuccess: () => void;
    sourcePersonaId: number | null;
    sourcePersonaName: string;
}

export default function DerivePersonaModal({ open, onClose, onSuccess, sourcePersonaId, sourcePersonaName }: DerivePersonaModalProps) {
    const [nameAdjective, setNameAdjective] = useState('');
    const [percentage, setPercentage] = useState(30);

    const handleSubmit = async () => {
        if (!sourcePersonaId) return;

        try {
            const response = await fetch(`${API_BASE_URL}/personas/derive`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    source_persona_id: sourcePersonaId,
                    name_adjective: nameAdjective,
                    percentage: percentage
                }),
            });

            if (response.ok) {
                onSuccess();
                onClose();
            } else {
                console.error('Failed to derive persona');
            }
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
