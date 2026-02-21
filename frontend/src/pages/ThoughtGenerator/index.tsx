import { useState } from 'react';
import { Box, TextField, Button, MenuItem, Select, FormControl, InputLabel, Alert, Stack, IconButton, CircularProgress } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import { usePersonas } from '../../hooks/usePersonas';
import { useGenerateThoughts } from '../../hooks/useGenerateThoughts';

export default function BlogGenerator() {
    const { data: personas = [] } = usePersonas();
    const { mutate, isPending, isSuccess, isError, reset } = useGenerateThoughts();

    const [urls, setUrls] = useState<string[]>(['', '', '', '', '']);
    const [selectedPersona, setSelectedPersona] = useState<string>('');

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

    const handleSubmit = () => {
        const validUrls = urls.filter(u => u.trim() !== '');
        if (validUrls.length === 0) return;

        mutate({
            urls: validUrls,
            persona_id: parseInt(selectedPersona)
        }, {
            onSuccess: () => {
                setUrls(['']);
                setSelectedPersona('');
            }
        });
    };

    return (
        <Box maxWidth="sm">
            {isSuccess && <Alert severity="success" sx={{ mb: 2 }} onClose={reset}>Generation started! Check the Thoughts page shortly.</Alert>}
            {isError && <Alert severity="error" sx={{ mb: 2 }} onClose={reset}>Error starting generation.</Alert>}

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

                <Button variant="contained" size="large" onClick={handleSubmit} disabled={!urls.some(u => u.trim()) || !selectedPersona || isPending}>
                    {isPending ? <CircularProgress size={24} /> : 'Generate Thoughts'}
                </Button>
            </Stack>
        </Box>
    );
}
