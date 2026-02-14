import { useState } from 'react';
import axios from 'axios';
import {
    Box, Typography, TextField, Button,
    Dialog, DialogTitle, DialogContent, DialogActions, Tabs, Tab,
    FormControl, InputLabel, Select, MenuItem, Slider
} from '@mui/material';
import type { Persona } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface CreatePersonaModalProps {
    open: boolean;
    onClose: () => void;
    onPersonaCreated: () => void;
    currentPersonas: Persona[];
}

export default function CreatePersonaModal({ open, onClose, onPersonaCreated, currentPersonas }: CreatePersonaModalProps) {
    const [tabIndex, setTabIndex] = useState(0);

    // Create Form State
    const [newItem, setNewItem] = useState({ name: '', age: '', gender: '' });

    // Derive Form State
    const [deriveSource, setDeriveSource] = useState('');
    const [deriveAdjective, setDeriveAdjective] = useState('');
    const [derivePercentage, setDerivePercentage] = useState<number>(50);

    const handleCreate = async () => {
        if (!newItem.name || !newItem.age || !newItem.gender) return;
        try {
            await axios.post(`${API_BASE_URL}/personas/`, {
                name: newItem.name,
                age: parseInt(newItem.age),
                gender: newItem.gender
            });
            setNewItem({ name: '', age: '', gender: '' });
            onPersonaCreated();
            onClose();
        } catch (err) { console.error(err); }
    };

    const handleDerive = async () => {
        if (!deriveSource || !deriveAdjective) return;
        try {
            await axios.post(`${API_BASE_URL}/personas/derive`, {
                source_persona_id: parseInt(deriveSource),
                name_adjective: deriveAdjective,
                percentage: derivePercentage
            });
            setDeriveSource('');
            setDeriveAdjective('');
            setDerivePercentage(50);
            onPersonaCreated();
            onClose();
        } catch (err) { console.error(err); }
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>Add New Persona</DialogTitle>
            <DialogContent>
                <Tabs value={tabIndex} onChange={(_, v) => setTabIndex(v)} sx={{ mb: 2 }}>
                    <Tab label="Create New" />
                    <Tab label="Derive" />
                </Tabs>

                {tabIndex === 0 && (
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                        <TextField label="Name" fullWidth value={newItem.name} onChange={e => setNewItem({ ...newItem, name: e.target.value })} />
                        <TextField label="Age" type="number" fullWidth value={newItem.age} onChange={e => setNewItem({ ...newItem, age: e.target.value })} />
                        <TextField label="Gender" fullWidth value={newItem.gender} onChange={e => setNewItem({ ...newItem, gender: e.target.value })} />
                    </Box>
                )}

                {tabIndex === 1 && (
                    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                        <FormControl fullWidth>
                            <InputLabel>Source Persona</InputLabel>
                            <Select value={deriveSource} label="Source Persona" onChange={e => setDeriveSource(e.target.value as string)}>
                                {currentPersonas.map(p => (
                                    <MenuItem key={p.id} value={p.id}>{p.name}</MenuItem>
                                ))}
                            </Select>
                        </FormControl>
                        <TextField label="Name Variation (Adjective)" fullWidth value={deriveAdjective} onChange={e => setDeriveAdjective(e.target.value)} helperText="e.g. 'Dark', 'Happy', 'Alternative'" />

                        <Typography gutterBottom>Percentage of Thoughts to Inherit ({derivePercentage}%)</Typography>
                        <Slider value={derivePercentage} onChange={(_, v) => setDerivePercentage(v as number)} min={1} max={100} valueLabelDisplay="auto" />
                    </Box>
                )}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button variant="contained" onClick={tabIndex === 0 ? handleCreate : handleDerive}>
                    {tabIndex === 0 ? 'Create' : 'Derive'}
                </Button>
            </DialogActions>
        </Dialog>
    );
}
