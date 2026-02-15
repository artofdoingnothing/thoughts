import { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, Stack, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import type { Persona } from '../../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function BlogGenerator() {
    const [personas, setPersonas] = useState<Persona[]>([]);
    const [urls, setUrls] = useState<string[]>(['', '', '', '', '']);
    const [selectedPersona, setSelectedPersona] = useState<string>('');
    const [message, setMessage] = useState('');

    useEffect(() => {
        axios.get<Persona[]>(`${API_BASE_URL}/personas/`).then(res => setPersonas(res.data)).catch(console.error);
    }, []);

    const handleUrlChange = (index: number, value: string) => {
        const newUrls = [...urls];
        newUrls[index] = value;
        setUrls(newUrls);
    };

    const addUrlField = () => {
        setUrls([...urls, '']);
    };

    const removeUrlField = (index: number) => {
        const newUrls = urls.filter((_, i) => i !== index);
        setUrls(newUrls.length ? newUrls : ['']);
    };

    const handleSubmit = async () => {
        try {
            const validUrls = urls.filter(u => u.trim() !== '');
            if (validUrls.length === 0) return;

            await axios.post(`${API_BASE_URL}/generate-thoughts/`, {
                urls: validUrls,
                persona_id: parseInt(selectedPersona)
            });
            setMessage('Generation started! Check the Thoughts page shortly.');
            setUrls(['']);
            setSelectedPersona('');
        } catch (err) {
            console.error(err);
            setMessage('Error starting generation.');
        }
    };

    return (
        <Box maxWidth="sm">
            {message && <Alert severity="info" sx={{ mb: 2 }}>{message}</Alert>}

            <Stack spacing={3}>
                {urls.map((url, index) => (
                    <Box key={index} sx={{ display: 'flex', gap: 1 }}>
                        <TextField
                            label={`Blog URL ${index + 1}`}
                            fullWidth
                            value={url}
                            onChange={e => handleUrlChange(index, e.target.value)}
                        />
                        <IconButton onClick={() => removeUrlField(index)} color="error" disabled={urls.length === 1 && !urls[0]}>
                            <DeleteIcon />
                        </IconButton>
                    </Box>
                ))}

                <Button startIcon={<AddIcon />} onClick={addUrlField} variant="outlined">
                    Add another URL
                </Button>

                <FormControl fullWidth>
                    <InputLabel>Persona</InputLabel>
                    <Select value={selectedPersona} label="Persona" onChange={e => setSelectedPersona(e.target.value)}>
                        {personas.map(p => (
                            <MenuItem key={p.id} value={p.id.toString()}>{p.name}</MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <Button variant="contained" size="large" onClick={handleSubmit} disabled={!urls.some(u => u.trim()) || !selectedPersona}>
                    Generate Thoughts
                </Button>
            </Stack>
        </Box>
    );
}
