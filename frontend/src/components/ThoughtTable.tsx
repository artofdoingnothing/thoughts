import React from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    IconButton,
    Chip,
    Box,
    Typography,
    Collapse
} from '@mui/material';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import DeleteIcon from '@mui/icons-material/Delete';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import type { Thought } from '../types';

interface ThoughtTableProps {
    thoughts: Thought[];
    expandedThoughtIds: Set<number>;
    toggleExpand: (id: number) => void;
    onDelete: (id: number) => void;
}

const Row: React.FC<{
    thought: Thought;
    isExpanded: boolean;
    toggleExpand: () => void;
    onDelete: () => void;
}> = ({ thought, isExpanded, toggleExpand, onDelete }) => {
    return (
        <>
            <TableRow
                hover
                sx={{ '& > *': { borderBottom: 'unset' }, bgcolor: isExpanded ? 'action.hover' : 'inherit' }}
            >
                <TableCell>
                    <IconButton
                        aria-label="expand row"
                        size="small"
                        onClick={toggleExpand}
                    >
                        {isExpanded ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
                    </IconButton>
                </TableCell>
                <TableCell component="th" scope="row" sx={{ fontWeight: 600 }}>
                    {thought.id}
                </TableCell>
                <TableCell sx={{ fontWeight: 500, cursor: 'pointer', maxWidth: 400 }} onClick={toggleExpand}>
                    <Typography variant="body2" color="text.primary" noWrap display="block">
                        {thought.content}
                    </Typography>
                </TableCell>
                <TableCell>
                    <Chip
                        label={thought.status}
                        size="small"
                        sx={{ fontWeight: 'bold', textTransform: 'uppercase', fontSize: '0.7rem' }}
                    />
                </TableCell>
                <TableCell>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                        {thought.is_generated ? (
                            <Chip icon={<SmartToyIcon sx={{ fontSize: 16 }} />} label={thought.persona ? thought.persona.name : "AI"} size="small" variant="outlined" />
                        ) : (
                            <Chip icon={<PersonIcon sx={{ fontSize: 16 }} />} label="User" size="small" variant="outlined" />
                        )}
                    </Box>
                </TableCell>
                <TableCell>
                    {thought.thought_type && (
                        <Chip
                            label={thought.thought_type}
                            size="small"
                            variant="outlined"
                            color="primary"
                            sx={{ fontWeight: 'bold', fontSize: '0.7rem' }}
                        />
                    )}
                </TableCell>
                <TableCell>
                    {thought.action_orientation && (
                        <Chip
                            label={thought.action_orientation}
                            size="small"
                            variant="outlined"
                            color="info"
                            sx={{ fontWeight: 'bold', fontSize: '0.7rem' }}
                        />
                    )}
                </TableCell>
                <TableCell>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {thought.emotions.map(e => (
                            <Chip
                                key={e.name}
                                label={e.name}
                                size="small"
                                variant={e.is_generated ? 'outlined' : 'filled'}
                                color={e.is_generated ? 'default' : 'secondary'}
                                sx={{ fontSize: '0.7rem' }}
                            />
                        ))}
                    </Box>
                </TableCell>
                <TableCell>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {thought.tags.map(t => (
                            <Chip key={t.name} label={t.name} size="small" sx={{ bgcolor: 'text.primary', color: 'background.paper', fontSize: '0.7rem' }} />
                        ))}
                    </Box>
                </TableCell>
                <TableCell align="right">
                    <IconButton
                        size="small"
                        color="error"
                        onClick={(e) => { e.stopPropagation(); onDelete(); }}
                    >
                        <DeleteIcon fontSize="small" />
                    </IconButton>
                </TableCell>
            </TableRow>
            <TableRow>
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={9}>
                    <Collapse in={isExpanded} timeout="auto" unmountOnExit>
                        <Box sx={{ margin: 2, p: 2, bgcolor: 'background.paper', borderRadius: 2, border: 1, borderColor: 'divider' }}>
                            <Typography variant="caption" sx={{ fontWeight: 'bold', color: 'text.secondary', display: 'block', mb: 1 }}>
                                CONTENT
                            </Typography>
                            <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', fontFamily: 'serif', mb: 2 }}>
                                {thought.content}
                            </Typography>

                            {thought.links && thought.links.length > 0 && (
                                <Box sx={{ mt: 2 }}>
                                    <Typography variant="caption" sx={{ fontWeight: 'bold', color: 'text.secondary', display: 'block', mb: 0.5 }}>
                                        LINKED THOUGHTS
                                    </Typography>
                                    <Box sx={{ display: 'flex', gap: 1 }}>
                                        {thought.links.map(linkId => (
                                            <Chip key={linkId} label={`#${linkId}`} size="small" variant="outlined" />
                                        ))}
                                    </Box>
                                </Box>
                            )}
                        </Box>
                    </Collapse>
                </TableCell>
            </TableRow>
        </>
    );
};

const ThoughtTable: React.FC<ThoughtTableProps> = ({ thoughts, expandedThoughtIds, toggleExpand, onDelete }) => {
    return (
        <TableContainer component={Paper} elevation={0} sx={{ border: 1, borderColor: 'divider', borderRadius: 2 }}>
            <Table sx={{ minWidth: 650 }} aria-label="thought table">
                <TableHead sx={{ bgcolor: 'action.hover' }}>
                    <TableRow>
                        <TableCell sx={{ width: 40 }} />
                        <TableCell sx={{ fontWeight: 'bold' }}>ID</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>CONTENT</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>STATUS</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>SRC</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>TYPE</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>ACTION</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>EMOTIONS</TableCell>
                        <TableCell sx={{ fontWeight: 'bold' }}>TAGS</TableCell>
                        <TableCell align="right" sx={{ fontWeight: 'bold' }}>ACTIONS</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {thoughts.map((thought) => (
                        <Row
                            key={thought.id}
                            thought={thought}
                            isExpanded={expandedThoughtIds.has(thought.id)}
                            toggleExpand={() => toggleExpand(thought.id)}
                            onDelete={() => onDelete(thought.id)}
                        />
                    ))}
                    {thoughts.length === 0 && (
                        <TableRow>
                            <TableCell colSpan={9} align="center" sx={{ py: 8 }}>
                                <Typography variant="body1" color="text.secondary" fontStyle="italic">
                                    No thoughts found. Start by creating one.
                                </Typography>
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default ThoughtTable;
