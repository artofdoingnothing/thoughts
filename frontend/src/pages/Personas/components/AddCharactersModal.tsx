import { useState } from 'react';
import {
    Dialog, DialogTitle, DialogContent, DialogActions,
    Box, Typography, TextField, Button, List, ListItem,
    ListItemText, ListItemSecondaryAction, IconButton, Card,
    CardContent, CardActions, Divider, CircularProgress, Alert, Grid
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import SearchIcon from '@mui/icons-material/Search';
import GroupAddIcon from '@mui/icons-material/GroupAdd';
import { useMovieCharacters } from '../../../hooks/useMovieCharacters';
import { useEnrichPersonaFromMovieCharacters } from '../../../hooks/usePersonas';
import type { MovieCharacter, Persona } from '../../../types';

interface AddCharactersModalProps {
    open: boolean;
    onClose: () => void;
    persona: Persona;
}

export default function AddCharactersModal({ open, onClose, persona }: AddCharactersModalProps) {
    const [titlePart, setTitlePart] = useState('');
    const [genre, setGenre] = useState('');
    const [minRating, setMinRating] = useState('');
    const [year, setYear] = useState('');
    const [charName, setCharName] = useState('');

    const [queryParams, setQueryParams] = useState({
        title: '',
        genre: '',
        min_rating: undefined as number | undefined,
        year: '',
        character_name: ''
    });

    const [selectedCharacters, setSelectedCharacters] = useState<MovieCharacter[]>([]);

    const { data: searchData, isLoading, isError, error } = useMovieCharacters(queryParams);
    const enrichMutation = useEnrichPersonaFromMovieCharacters();

    const handleSearch = () => {
        setQueryParams({
            title: titlePart,
            genre: genre,
            min_rating: minRating ? parseFloat(minRating) : undefined,
            year: year,
            character_name: charName
        });
    };

    const handleAddCharacter = (character: MovieCharacter) => {
        if (!selectedCharacters.find(c => c.character_id === character.character_id)) {
            setSelectedCharacters([...selectedCharacters, character]);
        }
    };

    const handleRemoveCharacter = (characterId: string) => {
        setSelectedCharacters(selectedCharacters.filter(c => c.character_id !== characterId));
    };

    const handleEnrich = () => {
        if (selectedCharacters.length === 0) return;
        
        const characterIds = selectedCharacters.map(c => c.character_id);
        enrichMutation.mutate({ personaId: persona.id, characterIds }, {
            onSuccess: () => {
                setSelectedCharacters([]);
                setTimeout(() => {
                    onClose();
                }, 2000); // Close after showing success
            }
        });
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="xl" fullWidth>
            <DialogTitle>Add Characters to {persona.name}</DialogTitle>
            <DialogContent dividers>
                <Grid container spacing={3}>
                    {/* Left Column: Selected Characters */}
                    <Grid size={{ xs: 12, md: 4 }}>
                        <Box sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column', border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
                            <Typography variant="h6" gutterBottom fontWeight="bold">
                                Selected Roster ({selectedCharacters.length})
                            </Typography>
                            <Divider sx={{ mb: 2 }} />
                            
                            <List sx={{ flexGrow: 1, overflow: 'auto', maxHeight: '500px' }}>
                                {selectedCharacters.length === 0 ? (
                                    <Typography color="text.secondary" variant="body2" sx={{ textAlign: 'center', mt: 4 }}>
                                        Search and add characters to expand this persona.
                                    </Typography>
                                ) : (
                                    selectedCharacters.map((char) => (
                                        <ListItem key={char.character_id} sx={{ bgcolor: 'background.default', mb: 1, borderRadius: 1 }}>
                                            <ListItemText
                                                primary={<Typography fontWeight="medium">{char.character_name}</Typography>}
                                                secondary={`${char.movie_title} (${char.movie_year})`}
                                            />
                                            <ListItemSecondaryAction>
                                                <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveCharacter(char.character_id)} color="error">
                                                    <DeleteIcon />
                                                </IconButton>
                                            </ListItemSecondaryAction>
                                        </ListItem>
                                    ))
                                )}
                            </List>

                            <Box sx={{ mt: 3 }}>
                                {enrichMutation.isError && (
                                    <Alert severity="error" sx={{ mb: 2 }}>
                                        Error adding characters.
                                    </Alert>
                                )}
                                {enrichMutation.isSuccess && (
                                    <Alert severity="success" sx={{ mb: 2 }}>
                                        Enrichment started! Updating persona...
                                    </Alert>
                                )}
                                <Button
                                    fullWidth
                                    variant="contained"
                                    color="secondary"
                                    onClick={handleEnrich}
                                    disabled={selectedCharacters.length === 0 || enrichMutation.isPending || enrichMutation.isSuccess}
                                    startIcon={enrichMutation.isPending ? <CircularProgress size={20} /> : <GroupAddIcon />}
                                >
                                    {enrichMutation.isPending ? 'Starting Task...' : 'Add Characters'}
                                </Button>
                            </Box>
                        </Box>
                    </Grid>

                    {/* Right Column: Search & Results */}
                    <Grid size={{ xs: 12, md: 8 }}>
                        <Box sx={{ mb: 4 }}>
                            <Grid container spacing={2} alignItems="center">
                                <Grid size={{ xs: 12, sm: 4 }}>
                                    <TextField fullWidth label="Character" size="small" value={charName} onChange={(e) => setCharName(e.target.value)} />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 3 }}>
                                    <TextField fullWidth label="Movie" size="small" value={titlePart} onChange={(e) => setTitlePart(e.target.value)} />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 2 }}>
                                    <TextField fullWidth label="Genre" size="small" value={genre} onChange={(e) => setGenre(e.target.value)} />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 1 }}>
                                    <TextField fullWidth label="Rat." size="small" type="number" inputProps={{ min: 0, max: 10, step: 0.1 }} value={minRating} onChange={(e) => setMinRating(e.target.value)} />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 1 }}>
                                    <TextField fullWidth label="Year" size="small" value={year} onChange={(e) => setYear(e.target.value)} />
                                </Grid>
                                <Grid size={{ xs: 12, sm: 1 }}>
                                    <Button fullWidth variant="contained" onClick={handleSearch} sx={{ minWidth: 0, px: 1 }}>
                                        <SearchIcon />
                                    </Button>
                                </Grid>
                            </Grid>
                        </Box>

                        <Box sx={{ minHeight: '400px', maxHeight: '500px', overflowY: 'auto' }}>
                            {isLoading && <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}><CircularProgress /></Box>}
                            {isError && <Alert severity="error">Error fetching characters: {(error as any)?.message || 'Unknown error'}</Alert>}

                            {!isLoading && !isError && searchData?.results && (
                                <Grid container spacing={2}>
                                    {searchData.results.map((char) => {
                                        const isSelected = !!selectedCharacters.find(c => c.character_id === char.character_id);
                                        return (
                                            <Grid size={{ xs: 12, sm: 6, md: 4 }} key={char.character_id}>
                                                <Card variant="outlined" sx={{ height: '100%', display: 'flex', flexDirection: 'column', borderColor: isSelected ? 'secondary.main' : 'divider', borderWidth: isSelected ? 2 : 1 }}>
                                                    <CardContent sx={{ flexGrow: 1, p: 1.5, '&:last-child': { pb: 1.5 } }}>
                                                        <Typography variant="subtitle1" component="div" noWrap title={char.character_name}>
                                                            {char.character_name}
                                                        </Typography>
                                                        <Typography sx={{ mb: 1 }} color="text.secondary" variant="body2" noWrap title={char.movie_title}>
                                                            {char.movie_title} ({char.movie_year})
                                                        </Typography>
                                                    </CardContent>
                                                    <CardActions sx={{ p: 1, pt: 0 }}>
                                                        <Button 
                                                            size="small" fullWidth variant={isSelected ? "outlined" : "contained"}
                                                            onClick={() => isSelected ? handleRemoveCharacter(char.character_id) : handleAddCharacter(char)}
                                                            color={isSelected ? "error" : "secondary"}
                                                        >
                                                            {isSelected ? 'Remove' : 'Add'}
                                                        </Button>
                                                    </CardActions>
                                                </Card>
                                            </Grid>
                                        );
                                    })}
                                    {searchData.results.length === 0 && (
                                        <Grid size={{ xs: 12 }}>
                                            <Typography color="text.secondary" sx={{ textAlign: 'center', p: 4 }}>
                                                No characters found.
                                            </Typography>
                                        </Grid>
                                    )}
                                </Grid>
                            )}
                        </Box>
                    </Grid>
                </Grid>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Close</Button>
            </DialogActions>
        </Dialog>
    );
}
