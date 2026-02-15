import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Box, Pagination, Typography, CircularProgress, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import ThoughtTable from './components/ThoughtTable';
import FilterBar from './components/FilterBar';
import type { Thought, Persona } from '../../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function Thoughts({ refreshKey }: { refreshKey: number }) {
    const [thoughts, setThoughts] = useState<Thought[]>([]);
    const [loading, setLoading] = useState(true);

    // Pagination
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);

    // Filters
    const [selectedTag, setSelectedTag] = useState<string>('');
    const [selectedEmotion, setSelectedEmotion] = useState<string>('');
    const [personas, setPersonas] = useState<Persona[]>([]);
    const [selectedPersona, setSelectedPersona] = useState<string>('');

    // Expanded Rows State
    const [expandedThoughtIds, setExpandedThoughtIds] = useState<Set<number>>(new Set());

    const fetchThoughts = useCallback(async () => {
        setLoading(true);
        try {
            const params: any = { page, limit: 50 };
            if (selectedTag) params.tag = selectedTag;
            if (selectedEmotion) params.emotion = selectedEmotion;
            if (selectedPersona) params.persona_id = selectedPersona;

            const res = await axios.get<{ items: Thought[], total: number, page: number, limit: number }>(`${API_BASE_URL}/thoughts/`, { params });
            setThoughts(res.data.items);
            setTotalPages(Math.ceil(res.data.total / res.data.limit));
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    }, [page, selectedTag, selectedEmotion, selectedPersona]);

    useEffect(() => {
        axios.get<Persona[]>(`${API_BASE_URL}/personas/`).then(res => setPersonas(res.data)).catch(console.error);
    }, []);

    useEffect(() => {
        fetchThoughts();
    }, [fetchThoughts, refreshKey]);

    const handleDelete = async (id: number) => {
        if (!window.confirm("Delete this thought?")) return;
        try {
            await axios.delete(`${API_BASE_URL}/thoughts/${id}`);
            fetchThoughts();
        } catch (err) { console.error(err); }
    };

    const toggleExpand = (id: number) => {
        const newExpanded = new Set(expandedThoughtIds);
        if (newExpanded.has(id)) {
            newExpanded.delete(id);
        } else {
            newExpanded.add(id);
        }
        setExpandedThoughtIds(newExpanded);
    };

    return (
        <Box>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h4" sx={{ color: 'primary.main', fontWeight: 'bold' }}>THOUGHTS</Typography>
                <FilterBar
                    searchTag={selectedTag}
                    setSearchTag={setSelectedTag}
                    searchEmotion={selectedEmotion}
                    setSearchEmotion={setSelectedEmotion}
                />
            </Box>

            <Box sx={{ mb: 3 }}>
                <FormControl sx={{ minWidth: 200 }}>
                    <InputLabel>Filter by Persona</InputLabel>
                    <Select
                        value={selectedPersona}
                        label="Filter by Persona"
                        onChange={(e) => {
                            setSelectedPersona(e.target.value);
                            setPage(1);
                        }}
                    >
                        <MenuItem value=""><em>All Personas</em></MenuItem>
                        {personas.map(p => (
                            <MenuItem key={p.id} value={p.id.toString()}>{p.name}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
            </Box>

            {loading ? (
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
                    <CircularProgress />
                </Box>
            ) : (
                <>
                    <ThoughtTable 
                        thoughts={thoughts} 
                        onDelete={handleDelete}
                        expandedThoughtIds={expandedThoughtIds}
                        toggleExpand={toggleExpand}
                    />
                    
                    <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
                        <Pagination count={totalPages} page={page} onChange={(_, p) => setPage(p)} color="primary" />
                    </Box>
                </>
            )}
        </Box>
    );
}
