import { useState } from 'react';
import { Grid, Container, CircularProgress, Box, Typography } from '@mui/material';
import PersonaList from './components/PersonaList';
import PersonaDetails from './components/PersonaDetails';
import CreatePersonaModal from './components/CreatePersonaModal';
import DerivePersonaModal from './components/DerivePersonaModal';
import AddCharactersModal from './components/AddCharactersModal';
import type { Persona } from '../../types';
import { usePersonas, useRegeneratePersona, useDeletePersona } from '../../hooks/usePersonas';

export default function PersonasPage() {
    const { data: personas = [], isLoading, isError } = usePersonas();
    const regenerateMutation = useRegeneratePersona();
    const deleteMutation = useDeletePersona();
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [editingPersona, setEditingPersona] = useState<Persona | null>(null);
    const [isDeriveModalOpen, setIsDeriveModalOpen] = useState(false);
    const [derivingPersona, setDerivingPersona] = useState<Persona | null>(null);
    const [isAddCharactersOpen, setIsAddCharactersOpen] = useState(false);
    const [addingToPersona, setAddingToPersona] = useState<Persona | null>(null);

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

    const handleDelete = async (persona: Persona) => {
        if (!window.confirm(`Are you sure you want to delete ${persona.name}? This will also delete all associated messages and thoughts.`)) {
            return;
        }

        try {
            await deleteMutation.mutateAsync(persona.id);
            if (selectedId === persona.id) {
                setSelectedId(null);
            }
        } catch (error) {
            console.error('Error deleting persona:', error);
            alert('Error deleting persona.');
        }
    };

    const handleAddCharacters = (persona: Persona) => {
        setAddingToPersona(persona);
        setIsAddCharactersOpen(true);
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
                        onDelete={handleDelete}
                    />
                </Grid>
                <Grid size={{ xs: 12, md: 8 }} sx={{ height: '100%' }}>
                    <PersonaDetails persona={selectedPersona} onAddCharacters={handleAddCharacters} />
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

            {isAddCharactersOpen && addingToPersona && (
                <AddCharactersModal
                    open={isAddCharactersOpen}
                    onClose={() => {
                        setIsAddCharactersOpen(false);
                        setAddingToPersona(null);
                    }}
                    persona={addingToPersona}
                />
            )}
        </Container>
    );
}
