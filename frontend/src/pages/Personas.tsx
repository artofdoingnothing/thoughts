import { useState, useEffect } from 'react';
import axios from 'axios';
import { Box, Typography, Card, CardContent, Grid, TextField, Button } from '@mui/material';
import type { Persona } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Personas() {
    const [personas, setPersonas] = useState<Persona[]>([]);
    const [newItem, setNewItem] = useState({ name: '', age: '', gender: '' });

    useEffect(() => {
        fetchPersonas();
    }, []);

    const fetchPersonas = async () => {
        try {
            const res = await axios.get<Persona[]>(`${API_BASE_URL}/personas/`);
            setPersonas(res.data);
        } catch (err) { console.error(err); }
    };

    const handleCreate = async () => {
        if (!newItem.name || !newItem.age || !newItem.gender) return;
        try {
            await axios.post(`${API_BASE_URL}/personas/`, {
                name: newItem.name,
                age: parseInt(newItem.age),
                gender: newItem.gender
            });
            setNewItem({ name: '', age: '', gender: '' });
            fetchPersonas();
        } catch (err) { console.error(err); }
    };

    return (
        <Box>
            <Typography variant="h4" sx={{ mb: 4, color: 'primary.main', fontWeight: 'bold' }}>Personas</Typography>

            <Box component="form" sx={{ mb: 4, display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
                <TextField label="Name" size="small" value={newItem.name} onChange={e => setNewItem({ ...newItem, name: e.target.value })} />
                <TextField label="Age" size="small" type="number" value={newItem.age} onChange={e => setNewItem({ ...newItem, age: e.target.value })} />
                <TextField label="Gender" size="small" value={newItem.gender} onChange={e => setNewItem({ ...newItem, gender: e.target.value })} />
                <Button variant="contained" onClick={handleCreate}>Add Persona</Button>
            </Box>

            <Grid container spacing={2}>
                {personas.map(p => (
                    <Grid size={{ xs: 12, sm: 6, md: 4 }} key={p.id}>
                        <Card>
                            <CardContent>
                                <Typography variant="h6">{p.name}</Typography>
                                <Typography color="text.secondary">Age: {p.age}</Typography>
                                <Typography color="text.secondary">Gender: {p.gender}</Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                ))}
            </Grid>
        </Box>
    );
}
