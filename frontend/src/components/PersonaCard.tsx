import { useState } from 'react';
import {
    Box, Typography, Card, CardContent, IconButton, Collapse, Chip, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { styled } from '@mui/material/styles';
import type { IconButtonProps } from '@mui/material/IconButton';
import type { Persona } from '../types';

interface ExpandMoreProps extends IconButtonProps {
    expand: boolean;
}

const ExpandMore = styled((props: ExpandMoreProps) => {
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    const { expand, ...other } = props;
    return <IconButton {...other} />;
})(({ theme, expand }) => ({
    transform: !expand ? 'rotate(0deg)' : 'rotate(180deg)',
    marginLeft: 'auto',
    transition: theme.transitions.create('transform', {
        duration: theme.transitions.duration.shortest,
    }),
}));

interface PersonaCardProps {
    persona: Persona;
    onDelete: (id: number) => void;
}

export default function PersonaCard({ persona, onDelete }: PersonaCardProps) {
    const [expanded, setExpanded] = useState(false);

    const handleExpandClick = () => {
        setExpanded(!expanded);
    };

    return (
        <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
            <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                    <Typography variant="h6">{persona.name}</Typography>
                    <Box>
                        <ExpandMore
                            expand={expanded}
                            onClick={handleExpandClick}
                            aria-expanded={expanded}
                            aria-label="show more"
                        >
                            <ExpandMoreIcon />
                        </ExpandMore>
                        <IconButton size="small" color="error" onClick={() => onDelete(persona.id)}>
                            <DeleteIcon />
                        </IconButton>
                    </Box>
                </Box>
                <Typography color="text.secondary" gutterBottom>Age: {persona.age} | Gender: {persona.gender}</Typography>
            </CardContent>
            <Collapse in={expanded} timeout="auto" unmountOnExit>
                <CardContent>
                    {persona.profile && (
                        <Box sx={{ mt: 2 }}>
                            {persona.profile.thought_patterns && (
                                <Typography variant="body2" color="text.secondary" sx={{ mb: 2, fontStyle: 'italic' }}>
                                    "{persona.profile.thought_patterns}"
                                </Typography>
                            )}
                            
                            <Typography variant="subtitle2" sx={{ fontWeight: 'bold', mb: 1 }}>Generalized Topics:</Typography>
                             <TableContainer component={Paper} variant="outlined">
                                <Table size="small" aria-label="topics table">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>Topic</TableCell>
                                            <TableCell>Emotions</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {persona.profile.topics?.map((topic, i) => (
                                            <TableRow key={i}>
                                                <TableCell component="th" scope="row">
                                                    {topic.name}
                                                </TableCell>
                                                <TableCell>
                                                    {topic.emotions?.map((emotion, j) => (
                                                        <Chip key={j} label={emotion} size="small" sx={{ mr: 0.5, mb: 0.5 }} />
                                                    ))}
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </Box>
                    )}
                </CardContent>
            </Collapse>
        </Card>
    );
}
