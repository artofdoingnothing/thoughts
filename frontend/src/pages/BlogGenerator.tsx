import { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, Stack } from '@mui/material';
import type { Persona } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function BlogGenerator() {
    const [personas, setPersonas] = useState<Persona[]>([]);
    const [url, setUrl] = useState('');
    const [selectedPersona, setSelectedPersona] = useState<string>('');
    const [message, setMessage] = useState('');

    useEffect(() => {
        axios.get<Persona[]>(`${API_BASE_URL}/personas/`).then(res => setPersonas(res.data)).catch(console.error);
    }, []);

    const handleSubmit = async () => {
        try {
            await axios.post(`${API_BASE_URL}/generate-thoughts/`, {
                url,
                persona_id: parseInt(selectedPersona)
            });
            setMessage('Generation started! Check the Thoughts page shortly.');
            setUrl('');
            setSelectedPersona('');
        } catch (err) {
            console.error(err);
            setMessage('Error starting generation.');
        }
    };

    return (
        <Box maxWidth="sm">
            <Typography variant="h4" sx={{ mb: 4, color: 'primary.main', fontWeight: 'bold' }}>Generate Thoughts from Blog</Typography>

            {message && <Alert severity="info" sx={{ mb: 2 }}>{message}</Alert>}

            <Stack spacing={3}>
                <TextField label="Blog URL" fullWidth value={url} onChange={e => setUrl(e.target.value)} />

                <FormControl fullWidth>
                    <InputLabel>Persona</InputLabel>
                    <Select value={selectedPersona} label="Persona" onChange={e => setSelectedPersona(e.target.value)}>
                        {personas.map(p => (
                            <MenuItem key={p.id} value={p.id.toString()}>{p.name}</MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <Button variant="contained" size="large" onClick={handleSubmit} disabled={!url || !selectedPersona}>
                    Generate Thoughts
                </Button>
            </Stack>
        </Box>
    );
}
