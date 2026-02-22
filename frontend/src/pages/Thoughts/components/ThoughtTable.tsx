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
    Collapse,
    Menu,
    MenuItem,
    Checkbox,
    FormControlLabel,
    Tooltip
} from '@mui/material';
import ViewColumnIcon from '@mui/icons-material/ViewColumn';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import DeleteIcon from '@mui/icons-material/Delete';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import PersonIcon from '@mui/icons-material/Person';
import type { Thought } from '../../../types';

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
    visibleColumns: Set<string>;
}> = ({ thought, isExpanded, toggleExpand, onDelete, visibleColumns }) => {
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
                {visibleColumns.has('id') && (
                    <TableCell component="th" scope="row" sx={{ fontWeight: 600 }}>
                        {thought.id}
                    </TableCell>
                )}
                {visibleColumns.has('content') && (
                    <TableCell sx={{ fontWeight: 500, cursor: 'pointer', maxWidth: 400 }} onClick={toggleExpand}>
                        <Typography variant="body2" color="text.primary" noWrap display="block">
                            {thought.content}
                        </Typography>
                    </TableCell>
                )}
                {visibleColumns.has('status') && (
                    <TableCell>
                        <Chip
                            label={thought.status}
                            size="small"
                            sx={{ fontWeight: 'bold', textTransform: 'uppercase', fontSize: '0.7rem' }}
                        />
                    </TableCell>
                )}
                {visibleColumns.has('source') && (
                    <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                            {thought.is_generated ? (
                                <Chip icon={<SmartToyIcon sx={{ fontSize: 16 }} />} label={thought.persona ? thought.persona.name : "AI"} size="small" variant="outlined" />
                            ) : (
                                <Chip icon={<PersonIcon sx={{ fontSize: 16 }} />} label="User" size="small" variant="outlined" />
                            )}
                        </Box>
                    </TableCell>
                )}
                {visibleColumns.has('type') && (
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
                )}
                {visibleColumns.has('action') && (
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
                )}
                {visibleColumns.has('emotions') && (
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
                )}
                {visibleColumns.has('topics') && (
                    <TableCell>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {thought.topics && thought.topics.map(t => (
                                <Chip key={t.name} label={t.name} size="small" variant="outlined" color="primary" sx={{ fontSize: '0.7rem' }} />
                            ))}
                        </Box>
                    </TableCell>
                )}
                {visibleColumns.has('tags') && (
                    <TableCell>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                            {thought.tags.map(t => (
                                <Chip key={t.name} label={t.name} size="small" sx={{ bgcolor: 'text.primary', color: 'background.paper', fontSize: '0.7rem' }} />
                            ))}
                        </Box>
                    </TableCell>
                )}
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
                <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={visibleColumns.size + 2}>
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

const COLUMNS = [
    { id: 'id', label: 'ID' },
    { id: 'content', label: 'CONTENT' },
    { id: 'status', label: 'STATUS' },
    { id: 'source', label: 'SRC' },
    { id: 'type', label: 'TYPE' },
    { id: 'action', label: 'ACTION' },
    { id: 'emotions', label: 'EMOTIONS' },
    { id: 'topics', label: 'TOPICS' },
    { id: 'tags', label: 'TAGS' },
] as const;

const ThoughtTable: React.FC<ThoughtTableProps> = ({ thoughts, expandedThoughtIds, toggleExpand, onDelete }) => {
    const [visibleColumns, setVisibleColumns] = React.useState<Set<string>>(new Set(COLUMNS.map(c => c.id)));
    const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

    const handleMenuOpen = (event: React.MouseEvent<HTMLButtonElement>) => {
        setAnchorEl(event.currentTarget);
    };

    const handleMenuClose = () => {
        setAnchorEl(null);
    };

    const toggleColumn = (id: string) => {
        const newVisible = new Set(visibleColumns);
        if (newVisible.has(id)) {
            if (newVisible.size > 1) { // Prevent hiding all columns
                newVisible.delete(id);
            }
        } else {
            newVisible.add(id);
        }
        setVisibleColumns(newVisible);
    };

    return (
        <Box sx={{ position: 'relative' }}>
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 1 }}>
                <Tooltip title="Column Visibility">
                    <IconButton onClick={handleMenuOpen} size="small" color="primary" sx={{ border: 1, borderColor: 'divider', borderRadius: 1 }}>
                        <ViewColumnIcon />
                        <Typography variant="caption" sx={{ ml: 1, fontWeight: 'bold' }}>COLUMNS</Typography>
                    </IconButton>
                </Tooltip>
                <Menu
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleMenuClose}
                    slotProps={{ paper: { sx: { width: 220, p: 1 } } }}
                >
                    <Typography variant="overline" sx={{ px: 2, fontWeight: 'bold', color: 'text.secondary' }}>
                        Toggle Columns
                    </Typography>
                    {COLUMNS.map((col) => (
                        <MenuItem key={col.id} dense onClick={() => toggleColumn(col.id)}>
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        size="small"
                                        checked={visibleColumns.has(col.id)}
                                        onClick={(e) => e.stopPropagation()}
                                        onChange={() => toggleColumn(col.id)}
                                    />
                                }
                                label={col.label}
                                onClick={(e) => e.stopPropagation()}
                                sx={{ pointerEvents: 'none', width: '100%' }}
                            />
                        </MenuItem>
                    ))}
                </Menu>
            </Box>
            <TableContainer component={Paper} elevation={0} sx={{ border: 1, borderColor: 'divider', borderRadius: 2 }}>
                <Table sx={{ minWidth: 650 }} aria-label="thought table">
                    <TableHead sx={{ bgcolor: 'action.hover' }}>
                        <TableRow>
                            <TableCell sx={{ width: 40 }} />
                            {visibleColumns.has('id') && <TableCell sx={{ fontWeight: 'bold' }}>ID</TableCell>}
                            {visibleColumns.has('content') && <TableCell sx={{ fontWeight: 'bold' }}>CONTENT</TableCell>}
                            {visibleColumns.has('status') && <TableCell sx={{ fontWeight: 'bold' }}>STATUS</TableCell>}
                            {visibleColumns.has('source') && <TableCell sx={{ fontWeight: 'bold' }}>SRC</TableCell>}
                            {visibleColumns.has('type') && <TableCell sx={{ fontWeight: 'bold' }}>TYPE</TableCell>}
                            {visibleColumns.has('action') && <TableCell sx={{ fontWeight: 'bold' }}>ACTION</TableCell>}
                            {visibleColumns.has('emotions') && <TableCell sx={{ fontWeight: 'bold' }}>EMOTIONS</TableCell>}
                            {visibleColumns.has('topics') && <TableCell sx={{ fontWeight: 'bold' }}>TOPICS</TableCell>}
                            {visibleColumns.has('tags') && <TableCell sx={{ fontWeight: 'bold' }}>TAGS</TableCell>}
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
                                visibleColumns={visibleColumns}
                            />
                        ))}
                        {thoughts.length === 0 && (
                            <TableRow>
                                <TableCell colSpan={visibleColumns.size + 2} align="center" sx={{ py: 8 }}>
                                    <Typography variant="body1" color="text.secondary" fontStyle="italic">
                                        No thoughts found. Start by creating one.
                                    </Typography>
                                </TableCell>
                            </TableRow>
                        )}
                    </TableBody>
                </Table>
            </TableContainer>
        </Box>
    );
};

export default ThoughtTable;
