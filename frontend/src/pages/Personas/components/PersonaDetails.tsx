import {
    Paper, Typography, Box, Chip, Stack,
    Table, TableBody, TableCell, TableContainer, TableRow
} from '@mui/material';
import type { Persona } from '../../../types';

interface PersonaDetailsProps {
    persona: Persona | null;
}

export default function PersonaDetails({ persona }: PersonaDetailsProps) {
    if (!persona) {
        return (
            <Paper elevation={3} sx={{ height: '100%', p: 3, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Typography color="text.secondary">Select a persona to view details</Typography>
            </Paper>
        );
    }

    return (
        <Paper elevation={3} sx={{ height: '100%', p: 3, overflowY: 'auto' }}>
            <Typography variant="h4" gutterBottom>{persona.name}</Typography>
            <Stack direction="row" spacing={2} sx={{ mb: 3 }}>
                <Chip label={`Age: ${persona.age}`} />
                <Chip label={`Gender: ${persona.gender}`} />
            </Stack>

            {persona.additional_info && Object.keys(persona.additional_info).length > 0 && (
                <Box sx={{ mb: 4 }}>
                    <Typography variant="h6" gutterBottom>Additional Information</Typography>
                    <TableContainer component={Paper} variant="outlined">
                        <Table size="small">
                            <TableBody>
                                {Object.entries(persona.additional_info).map(([key, value]) => (
                                    <TableRow key={key}>
                                        <TableCell component="th" scope="row" sx={{ fontWeight: 'bold', width: '30%' }}>
                                            {key}
                                        </TableCell>
                                        <TableCell>{String(value)}</TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </Box>
            )}

            {persona.profile && (
                <Box>
                    <Typography variant="h6" gutterBottom>Profile Analysis</Typography>
                    
                    {persona.profile.thought_patterns && (
                        <Box sx={{ mb: 2 }}>
                            <Typography variant="subtitle1" fontWeight="bold">Thought Patterns</Typography>
                            <Typography variant="body2">{persona.profile.thought_patterns}</Typography>
                        </Box>
                    )}

                    {persona.profile.topics && (
                        <Box sx={{ mb: 2 }}>
                            <Typography variant="subtitle1" fontWeight="bold">Topics & Emotions</Typography>
                            {persona.profile.topics.map((topic, idx) => (
                                <Box key={idx} sx={{ ml: 2, mb: 1 }}>
                                    <Typography variant="body2" fontWeight="bold">- {topic.name}</Typography>
                                    <Typography variant="caption" color="text.secondary">
                                        Emotions: {topic.emotions.join(', ')}
                                    </Typography>
                                </Box>
                            ))}
                        </Box>
                    )}
                </Box>
            )}
        </Paper>
    );
}
