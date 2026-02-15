import { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, Stack, CircularProgress, Paper } from '@mui/material';
import type { Persona } from '../../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function EssayGenerator() {
    const [personas, setPersonas] = useState<Persona[]>([]);
    const [selectedPersona, setSelectedPersona] = useState<string>('');
    const [startingText, setStartingText] = useState<string>('');
    const [isGenerating, setIsGenerating] = useState(false);
    const [jobId, setJobId] = useState<string | null>(null);
    const [generatedEssay, setGeneratedEssay] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        axios.get<Persona[]>(`${API_BASE_URL}/personas/`).then(res => setPersonas(res.data)).catch(console.error);
    }, []);

    useEffect(() => {
        let interval: number;
        if (jobId) {
            interval = window.setInterval(async () => {
                try {
                    const res = await axios.get(`${API_BASE_URL}/essay/status/${jobId}`);
                    if (res.data.status === 'finished') {
                        setGeneratedEssay(res.data.result);
                        setIsGenerating(false);
                        setJobId(null);
                    } else if (res.data.status === 'failed') {
                        setError('Generation failed.');
                        setIsGenerating(false);
                        setJobId(null);
                    }
                } catch (err) {
                    console.error(err);
                    setError('Error checking status.');
                    setIsGenerating(false);
                    setJobId(null);
                }
            }, 2000);
        }
        return () => clearInterval(interval);
    }, [jobId]);

    const handleGenerate = async () => {
        if (!selectedPersona || !startingText.trim()) return;

        setIsGenerating(true);
        setError(null);
        setGeneratedEssay(null);

        try {
            const res = await axios.post(`${API_BASE_URL}/essay/generate`, {
                starting_text: startingText,
                persona_id: parseInt(selectedPersona)
            });
            setJobId(res.data.job_id);
        } catch (err) {
            console.error(err);
            setError('Error starting generation.');
            setIsGenerating(false);
        }
    };

    return (
        <Box maxWidth="md" sx={{ mx: 'auto' }}>
            <Typography variant="h4" sx={{ mb: 4, color: 'primary.main', fontWeight: 'bold' }}>ESSAY GENERATOR</Typography>

            <Paper sx={{ p: 4, mb: 4 }}>
                <Stack spacing={3}>
                    <FormControl fullWidth>
                        <InputLabel>Persona</InputLabel>
                        <Select value={selectedPersona} label="Persona" onChange={e => setSelectedPersona(e.target.value)}>
                            {personas.map(p => (
                                <MenuItem key={p.id} value={p.id.toString()}>{p.name}</MenuItem>
                            ))}
                        </Select>
                    </FormControl>

                    <TextField
                        label="Starting Text"
                        multiline
                        rows={4}
                        value={startingText}
                        onChange={e => setStartingText(e.target.value)}
                        fullWidth
                        placeholder="Once upon a time..."
                    />

                    <Button
                        variant="contained"
                        size="large"
                        onClick={handleGenerate}
                        disabled={isGenerating || !selectedPersona || !startingText.trim()}
                    >
                        {isGenerating ? <CircularProgress size={24} color="inherit" /> : 'Generate Essay'}
                    </Button>

                    {error && <Alert severity="error">{error}</Alert>}
                </Stack>
            </Paper>

            {generatedEssay && (
                <Box>
                    <Typography variant="h5" sx={{ mb: 2 }}>Generated Essay</Typography>
                    <Paper sx={{ p: 4, whiteSpace: 'pre-wrap' }}>
                        <Typography variant="body1" sx={{ fontFamily: 'Georgia, serif', lineHeight: 1.8 }}>
                            {startingText}
                            <span style={{ backgroundColor: '#e3f2fd' }}>{generatedEssay}</span>
                        </Typography>
                    </Paper>
                </Box>
            )}
        </Box>
    );
}
