import { useState } from 'react';
import { Box, Pagination, Typography, CircularProgress, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import ThoughtTable from './components/ThoughtTable';
import FilterBar from './components/FilterBar';
import { usePersonas } from '../../hooks/usePersonas';
import { useThoughts, useDeleteThought } from '../../hooks/useThoughts';

export default function Thoughts() {
    const [selectedTag, setSelectedTag] = useState<string>('');
    const [selectedEmotion, setSelectedEmotion] = useState<string>('');
    const [selectedPersona, setSelectedPersona] = useState<string>('');
    const [page, setPage] = useState(1);

    const { data: personas = [] } = usePersonas();
    const { data, isLoading: loading } = useThoughts({ 
        page, 
        tag: selectedTag, 
        emotion: selectedEmotion, 
        persona_id: selectedPersona 
    });

    const deleteMutation = useDeleteThought();

    const thoughts = data?.items || [];
    const totalPages = data ? Math.ceil(data.total / data.limit) : 1;

    // Expanded Rows State
    const [expandedThoughtIds, setExpandedThoughtIds] = useState<Set<number>>(new Set());

    const handleDelete = (id: number) => {
        if (!window.confirm("Delete this thought?")) return;
        deleteMutation.mutate(id);
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
