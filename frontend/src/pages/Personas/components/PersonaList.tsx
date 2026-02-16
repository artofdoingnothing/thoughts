import {
    List, ListItemButton, ListItemText, ListItemAvatar, Avatar, Typography, Paper, Box, Button
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import AddIcon from '@mui/icons-material/Add';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import type { Persona } from '../../../types';

interface PersonaListProps {
    personas: Persona[];
    selectedId: number | null;
    onSelect: (id: number) => void;
    onAdd: () => void;
    onEdit: (persona: Persona) => void;
    onDerive: (persona: Persona) => void;
    onRegenerate: (persona: Persona) => void;
}

export default function PersonaList({ personas, selectedId, onSelect, onAdd, onEdit, onDerive, onRegenerate }: PersonaListProps) {
    return (
        <Paper elevation={3} sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <Typography variant="h6" component="div">
                    Personas
                </Typography>
                <Button startIcon={<AddIcon />} variant="contained" size="small" onClick={onAdd}>
                    Add
                </Button>
            </Box>
            <List sx={{ flexGrow: 1, overflowY: 'auto' }}>
                {personas.map((persona) => (
                    <ListItemButton
                        key={persona.id}
                        selected={selectedId === persona.id}
                        onClick={() => onSelect(persona.id)}
                    >
                        <ListItemAvatar>
                            <Avatar>
                                <PersonIcon />
                            </Avatar>
                        </ListItemAvatar>
                        <ListItemText
                            primary={persona.name}
                            secondary={`${persona.age} • ${persona.gender}`}
                        />
                        <Box>
                            <Button size="small" onClick={(e) => { e.stopPropagation(); onEdit(persona); }}>
                                Edit
                            </Button>
                            <Button size="small" onClick={(e) => { e.stopPropagation(); onDerive(persona); }}>
                                Derive
                            </Button>
                            <Button size="small" onClick={(e) => { e.stopPropagation(); onRegenerate(persona); }} title="Regenerate based on thoughts">
                                <AutorenewIcon fontSize="small" />
                            </Button>
                        </Box>
                    </ListItemButton>
                ))}
            </List>
        </Paper>
    );
}
