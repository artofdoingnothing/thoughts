import { useState } from 'react';
import { Grid, Container, CircularProgress, Box, Typography } from '@mui/material';
import PersonaList from './components/PersonaList';
import PersonaDetails from './components/PersonaDetails';
import CreatePersonaModal from './components/CreatePersonaModal';
import DerivePersonaModal from './components/DerivePersonaModal';
import type { Persona } from '../../types';
import { usePersonas, useRegeneratePersona } from '../../hooks/usePersonas';

export default function PersonasPage() {
    const { data: personas = [], isLoading, isError } = usePersonas();
    const regenerateMutation = useRegeneratePersona();
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [editingPersona, setEditingPersona] = useState<Persona | null>(null);
    const [isDeriveModalOpen, setIsDeriveModalOpen] = useState(false);
    const [derivingPersona, setDerivingPersona] = useState<Persona | null>(null);

    const handleCreate = () => {
        setEditingPersona(null);
        setIsCreateModalOpen(true);
    };

    const handleEdit = (persona: Persona) => {
        setEditingPersona(persona);
        setIsCreateModalOpen(true);
    };

    const handleDerive = (persona: Persona) => {
        setDerivingPersona(persona);
        setIsDeriveModalOpen(true);
    };

    const handleRegenerate = async (persona: Persona) => {
        if (!window.confirm(`Are you sure you want to regenerate the profile for ${persona.name}? This will overwrite existing profile data.`)) {
            return;
        }

        try {
            await regenerateMutation.mutateAsync(persona.id);
        } catch (error) {
            console.error('Error regenerating persona:', error);
            alert('Error regenerating persona.');
        }
    };

    const selectedPersona = personas.find(p => p.id === selectedId) || null;

    if (isLoading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" height="calc(100vh - 100px)">
                <CircularProgress />
            </Box>
        );
    }

    if (isError) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" height="calc(100vh - 100px)">
                <Typography color="error">Failed to load personas.</Typography>
            </Box>
        );
    }

    return (
        <Container maxWidth="xl" sx={{ mt: 4, mb: 4, height: 'calc(100vh - 100px)' }}>
            <Grid container spacing={3} sx={{ height: '100%' }}>
                <Grid size={{ xs: 12, md: 4 }} sx={{ height: '100%' }}>
                    <PersonaList
                        personas={personas}
                        selectedId={selectedId}
                        onSelect={setSelectedId}
                        onAdd={handleCreate}
                        onEdit={handleEdit}
                        onDerive={handleDerive}
                        onRegenerate={handleRegenerate}
                    />
                </Grid>
                <Grid size={{ xs: 12, md: 8 }} sx={{ height: '100%' }}>
                    <PersonaDetails persona={selectedPersona} />
                </Grid>
            </Grid>

            {isCreateModalOpen && (
                <CreatePersonaModal
                    open={isCreateModalOpen}
                    onClose={() => {
                        setIsCreateModalOpen(false);
                        setEditingPersona(null);
                    }}
                    initialData={editingPersona}
                />
            )}

            {isDeriveModalOpen && derivingPersona && (
                <DerivePersonaModal
                    open={isDeriveModalOpen}
                    onClose={() => {
                        setIsDeriveModalOpen(false);
                        setDerivingPersona(null);
                    }}
                    sourcePersonaId={derivingPersona.id}
                    sourcePersonaName={derivingPersona.name}
                />
            )}
        </Container>
    );
}
