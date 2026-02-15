import {
    List, ListItemButton, ListItemText, ListItemAvatar, Avatar, Typography, Paper, Box, Button
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import AddIcon from '@mui/icons-material/Add';
import type { Persona } from '../../../types';

interface PersonaListProps {
    personas: Persona[];
    selectedId: number | null;
    onSelect: (id: number) => void;
    onAdd: () => void;
}

export default function PersonaList({ personas, selectedId, onSelect, onAdd }: PersonaListProps) {
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
                    </ListItemButton>
                ))}
            </List>
        </Paper>
    );
}
