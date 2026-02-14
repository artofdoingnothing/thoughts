import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Box, Typography, Button, Grid } from '@mui/material';
import type { Persona } from '../types';
import CreatePersonaModal from '../components/CreatePersonaModal';
import PersonaCard from '../components/PersonaCard';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Personas() {
    const [personas, setPersonas] = useState<Persona[]>([]);
    const [open, setOpen] = useState(false);

    const fetchPersonas = useCallback(async () => {
        try {
            const res = await axios.get<Persona[]>(`${API_BASE_URL}/personas/`);
            setPersonas(res.data);
        } catch (err) { console.error(err); }
    }, []);

    useEffect(() => {
        // eslint-disable-next-line react-hooks/exhaustive-deps
        fetchPersonas();
    }, [fetchPersonas]);

    const handleDelete = async (id: number) => {
        if (!window.confirm("Are you sure you want to delete this persona and all their thoughts?")) return;
        try {
            await axios.delete(`${API_BASE_URL}/personas/${id}`);
            fetchPersonas();
        } catch (err) { console.error(err); }
    };

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
                <Typography variant="h4" sx={{ color: 'primary.main', fontWeight: 'bold' }}>PERSONAS</Typography>
                <Button variant="contained" onClick={() => setOpen(true)}>Add Persona</Button>
            </Box>

            <CreatePersonaModal
                open={open}
                onClose={() => setOpen(false)}
                onPersonaCreated={fetchPersonas}
                currentPersonas={personas}
            />

            <Grid container spacing={2}>
                {personas.map(p => (
                    <Grid size={{ xs: 12, sm: 6, md: 4 }} key={p.id}>
                        <PersonaCard persona={p} onDelete={handleDelete} />
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
}
