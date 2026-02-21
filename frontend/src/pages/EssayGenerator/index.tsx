import { useState } from 'react';
import { Box, Typography, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, Stack, CircularProgress, Paper } from '@mui/material';
import { usePersonas } from '../../hooks/usePersonas';
import { useEssayStatus, useGenerateEssay } from '../../hooks/useEssay';

export default function EssayGenerator() {
    const { data: personas = [] } = usePersonas();
    const [selectedPersona, setSelectedPersona] = useState<string>('');
    const [startingText, setStartingText] = useState<string>('');
    const [jobId, setJobId] = useState<string | null>(null);

    const { mutate, isPending: isStartingGeneration, error: generationError } = useGenerateEssay();
    const { data: essayStatus, isError: isStatusError } = useEssayStatus(jobId);

    const isGenerating = isStartingGeneration || (jobId && essayStatus?.status !== 'finished' && essayStatus?.status !== 'failed');
    const hasFailed = essayStatus?.status === 'failed' || isStatusError || generationError;
    const generatedEssay = essayStatus?.status === 'finished' ? essayStatus.result : null;

    const handleGenerate = () => {
        if (!selectedPersona || !startingText.trim()) return;

        setJobId(null);

        mutate({
            starting_text: startingText,
            persona_id: parseInt(selectedPersona)
        }, {
            onSuccess: (data) => {
                setJobId(data.job_id);
            }
        });
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

                    {hasFailed && <Alert severity="error">Error starting or checking generation.</Alert>}
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
