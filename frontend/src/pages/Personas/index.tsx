import { useState, useEffect } from 'react';
import { Grid, Container } from '@mui/material';
import PersonaList from './components/PersonaList';
import PersonaDetails from './components/PersonaDetails';
import CreatePersonaModal from './components/CreatePersonaModal';
import DerivePersonaModal from './components/DerivePersonaModal';
import type { Persona } from '../../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function PersonasPage() {
    const [personas, setPersonas] = useState<Persona[]>([]);
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [editingPersona, setEditingPersona] = useState<Persona | null>(null);
    const [isDeriveModalOpen, setIsDeriveModalOpen] = useState(false);
    const [derivingPersona, setDerivingPersona] = useState<Persona | null>(null);

    const fetchPersonas = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/personas/`);
            if (response.ok) {
                const data = await response.json();
                setPersonas(data);
            }
        } catch (error) {
            console.error('Failed to fetch personas:', error);
        }
    };

    useEffect(() => {
        fetchPersonas();
    }, []);

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
            const response = await fetch(`${API_BASE_URL}/personas/${persona.id}/regenerate`, {
                method: 'POST',
            });

            if (response.ok) {
                await fetchPersonas();
                // If the regenerated persona was selected, update the selection details
                if (selectedId === persona.id) {
                     // trigger re-render of details by fetching fresh list which we did
                }
            } else {
                console.error('Failed to regenerate persona');
                alert('Failed to regenerate persona. Ensure it has thoughts.');
            }
        } catch (error) {
            console.error('Error regenerating persona:', error);
            alert('Error regenerating persona.');
        }
    };

    const handleSuccess = () => {
        fetchPersonas();
        setEditingPersona(null);
        setDerivingPersona(null);
    };

    const selectedPersona = personas.find(p => p.id === selectedId) || null;

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
                    onSuccess={handleSuccess}
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
                    onSuccess={handleSuccess}
                    sourcePersonaId={derivingPersona.id}
                    sourcePersonaName={derivingPersona.name}
                />
            )}
        </Container>
    );
}
