import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    Box,
    Grid,
    Typography,
    TextField,
    Button,
    Paper,
    List,
    ListItem,
    ListItemText,
    ListItemSecondaryAction,
    IconButton,
    Card,
    CardContent,
    CardActions,
    Divider,
    CircularProgress,
    Chip,
    Alert
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import { useMovieCharacters } from '../../hooks/useMovieCharacters';
import { useGeneratePersonaFromMovieCharacters } from '../../hooks/usePersonas';
import type { MovieCharacter } from '../../types';

const MovieCharacterSearch: React.FC = () => {
    const navigate = useNavigate();

    // Search states
    const [titlePart, setTitlePart] = useState('');
    const [genre, setGenre] = useState('');
    const [minRating, setMinRating] = useState('');
    const [year, setYear] = useState('');

    // Query parameters state
    const [queryParams, setQueryParams] = useState({
        title: '',
        genre: '',
        min_rating: undefined as number | undefined,
        year: ''
    });

    // Selected characters state
    const [selectedCharacters, setSelectedCharacters] = useState<MovieCharacter[]>([]);

    const { data: searchData, isLoading, isError, error } = useMovieCharacters(queryParams);
    const generateMutation = useGeneratePersonaFromMovieCharacters();

    const handleSearch = () => {
        setQueryParams({
            title: titlePart,
            genre: genre,
            min_rating: minRating ? parseFloat(minRating) : undefined,
            year: year
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

    const handleGenerate = () => {
        if (selectedCharacters.length === 0) return;
        
        const characterIds = selectedCharacters.map(c => c.character_id);
        generateMutation.mutate({ character_ids: characterIds }, {
            onSuccess: () => {
                setSelectedCharacters([]);
                setTimeout(() => {
                    navigate('/personas');
                }, 2000); // Redirect after small delay
            }
        });
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            <Typography variant="h4" fontWeight="bold" gutterBottom sx={{ mb: 4 }}>
                Movie Character Search
            </Typography>

            <Grid container spacing={4}>
                {/* Left Column: Selected Characters */}
                <Grid size={{ xs: 12, md: 4 }}>
                    <Paper elevation={3} sx={{ p: 3, height: '100%', minHeight: '600px', display: 'flex', flexDirection: 'column' }}>
                        <Typography variant="h6" gutterBottom fontWeight="bold">
                            Selected Roster ({selectedCharacters.length})
                        </Typography>
                        <Divider sx={{ mb: 2 }} />
                        
                        <List sx={{ flexGrow: 1, overflow: 'auto' }}>
                            {selectedCharacters.length === 0 ? (
                                <Typography color="text.secondary" variant="body2" sx={{ textAlign: 'center', mt: 4 }}>
                                    No characters selected yet. Search and add characters to generate a persona.
                                </Typography>
                            ) : (
                                selectedCharacters.map((char) => (
                                    <ListItem key={char.character_id} sx={{ bgcolor: 'background.default', mb: 1, borderRadius: 1 }}>
                                        <ListItemText
                                            primary={
                                                <Typography fontWeight="medium">{char.character_name}</Typography>
                                            }
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
                            {generateMutation.isError && (
                                <Alert severity="error" sx={{ mb: 2 }}>
                                    Error generating persona.
                                </Alert>
                            )}
                            {generateMutation.isSuccess && (
                                <Alert severity="success" sx={{ mb: 2 }}>
                                    Persona generation started securely! Redirecting to Personas page...
                                </Alert>
                            )}
                            <Button
                                fullWidth
                                variant="contained"
                                color="primary"
                                size="large"
                                onClick={handleGenerate}
                                disabled={selectedCharacters.length === 0 || generateMutation.isPending || generateMutation.isSuccess}
                                startIcon={generateMutation.isPending ? <CircularProgress size={20} /> : <AutoAwesomeIcon />}
                            >
                                {generateMutation.isPending ? 'Generating Background Job...' : 'Generate Persona'}
                            </Button>
                        </Box>
                    </Paper>
                </Grid>

                {/* Right Column: Search & Results */}
                <Grid size={{ xs: 12, md: 8 }}>
                    <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                        <Typography variant="h6" gutterBottom fontWeight="bold">
                            Search Filters
                        </Typography>
                        <Grid container spacing={2} alignItems="center">
                            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                <TextField
                                    fullWidth
                                    label="Movie Title"
                                    variant="outlined"
                                    size="small"
                                    value={titlePart}
                                    onChange={(e) => setTitlePart(e.target.value)}
                                    placeholder="e.g. matrix"
                                />
                            </Grid>
                            <Grid size={{ xs: 12, sm: 6, md: 3 }}>
                                <TextField
                                    fullWidth
                                    label="Genre"
                                    variant="outlined"
                                    size="small"
                                    value={genre}
                                    onChange={(e) => setGenre(e.target.value)}
                                    placeholder="e.g. action"
                                />
                            </Grid>
                            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
                                <TextField
                                    fullWidth
                                    label="Min. Rating"
                                    variant="outlined"
                                    size="small"
                                    type="number"
                                    inputProps={{ min: 0, max: 10, step: 0.1 }}
                                    value={minRating}
                                    onChange={(e) => setMinRating(e.target.value)}
                                    placeholder="e.g. 7.5"
                                />
                            </Grid>
                            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
                                <TextField
                                    fullWidth
                                    label="Year"
                                    variant="outlined"
                                    size="small"
                                    value={year}
                                    onChange={(e) => setYear(e.target.value)}
                                    placeholder="e.g. 1999"
                                />
                            </Grid>
                            <Grid size={{ xs: 12, md: 2 }}>
                                <Button
                                    fullWidth
                                    variant="contained"
                                    onClick={handleSearch}
                                    startIcon={<SearchIcon />}
                                    sx={{ height: '40px' }}
                                >
                                    Search
                                </Button>
                            </Grid>
                        </Grid>
                    </Paper>

                    <Box sx={{ width: '100%' }}>
                        <Typography variant="h6" gutterBottom fontWeight="bold">
                            Results {searchData?.results ? `(${searchData.results.length})` : ''}
                        </Typography>
                        
                        {isLoading && (
                            <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
                                <CircularProgress />
                            </Box>
                        )}
                        
                        {isError && (
                            <Alert severity="error">
                                Error fetching movie characters: {(error as any)?.message}
                            </Alert>
                        )}

                        {!isLoading && !isError && searchData?.results && (
                            <Grid container spacing={2}>
                                {searchData.results.map((char) => {
                                    const isSelected = !!selectedCharacters.find(c => c.character_id === char.character_id);
                                    return (
                                        <Grid size={{ xs: 12, sm: 6, md: 4 }} key={char.character_id}>
                                            <Card 
                                                variant="outlined" 
                                                sx={{ 
                                                    height: '100%', 
                                                    display: 'flex', 
                                                    flexDirection: 'column',
                                                    borderColor: isSelected ? 'primary.main' : 'divider',
                                                    borderWidth: isSelected ? 2 : 1
                                                }}
                                            >
                                                <CardContent sx={{ flexGrow: 1 }}>
                                                    <Typography variant="h6" component="div" noWrap title={char.character_name}>
                                                        {char.character_name}
                                                    </Typography>
                                                    <Typography sx={{ mb: 1.5 }} color="text.secondary" variant="body2" noWrap title={char.movie_title}>
                                                        {char.movie_title} ({char.movie_year})
                                                    </Typography>
                                                    
                                                    <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                                        <Chip label={`IMDB: ${char.movie_imdb_rating}`} size="small" variant="outlined" />
                                                        {char.movie_genres.slice(0, 2).map(g => (
                                                            <Chip key={g} label={g} size="small" color="primary" variant="outlined" />
                                                        ))}
                                                    </Box>
                                                </CardContent>
                                                <CardActions>
                                                    <Button 
                                                        size="small" 
                                                        fullWidth 
                                                        variant={isSelected ? "outlined" : "contained"}
                                                        onClick={() => isSelected ? handleRemoveCharacter(char.character_id) : handleAddCharacter(char)}
                                                        startIcon={isSelected ? <DeleteIcon /> : <AddIcon />}
                                                        color={isSelected ? "error" : "primary"}
                                                    >
                                                        {isSelected ? 'Remove' : 'Add to Roster'}
                                                    </Button>
                                                </CardActions>
                                            </Card>
                                        </Grid>
                                    );
                                })}
                                {searchData.results.length === 0 && (
                                    <Grid size={{ xs: 12 }}>
                                        <Typography color="text.secondary" sx={{ textAlign: 'center', p: 4 }}>
                                            No characters found matching your filters.
                                        </Typography>
                                    </Grid>
                                )}
                            </Grid>
                        )}
                    </Box>
                </Grid>
            </Grid>
        </Box>
    );
};

export default MovieCharacterSearch;
