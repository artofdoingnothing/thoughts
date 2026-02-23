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
    Divider,
    CircularProgress,
    Alert
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import SearchIcon from '@mui/icons-material/Search';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import { useMovieCharacters, useRandomMovieCharacters } from '../../hooks/useMovieCharacters';
import { useGeneratePersonaFromMovieCharacters } from '../../hooks/usePersonas';
import type { MovieCharacter } from '../../types';

const MovieCharacterSearch: React.FC = () => {
    const navigate = useNavigate();

    // Search states
    const [titlePart, setTitlePart] = useState('');
    const [genre, setGenre] = useState('');
    const [minRating, setMinRating] = useState('');
    const [year, setYear] = useState('');
    const [charName, setCharName] = useState('');

    // Query parameters state
    const [queryParams, setQueryParams] = useState({
        title: '',
        genre: '',
        min_rating: undefined as number | undefined,
        year: '',
        character_name: ''
    });

    // Selected characters state
    const [selectedCharacters, setSelectedCharacters] = useState<MovieCharacter[]>([]);

    const [randomSeed, setRandomSeed] = useState<number | null>(null);

    const { data: searchData, isLoading: isSearchLoading, isError: isSearchError, error: searchError } = useMovieCharacters(queryParams);
    const { data: randomData, isLoading: isRandomLoading, isError: isRandomError, error: randomError } = useRandomMovieCharacters(randomSeed);

    const generateMutation = useGeneratePersonaFromMovieCharacters();

    const handleSearch = () => {
        setRandomSeed(null);
        setQueryParams({
            title: titlePart,
            genre: genre,
            min_rating: minRating ? parseFloat(minRating) : undefined,
            year: year,
            character_name: charName
        });
    };

    const handleFetchRandom = () => {
        setRandomSeed(Date.now());
    };

    const handleMovieClick = (movieTitle: string) => {
        setRandomSeed(null);
        setTitlePart(movieTitle);
        setCharName('');
        setGenre('');
        setMinRating('');
        setYear('');
        
        setQueryParams({
            title: movieTitle,
            genre: '',
            min_rating: undefined,
            year: '',
            character_name: ''
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
                    <Paper elevation={3} sx={{ p: 3, height: 'fit-content', minHeight: '600px', display: 'flex', flexDirection: 'column' }}>
                        <Typography variant="h6" gutterBottom fontWeight="bold">
                            Selected Roster ({selectedCharacters.length})
                        </Typography>
                        <Divider sx={{ mb: 2 }} />
                        
                        <List sx={{ flexGrow: 1 }}>
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
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                            <Typography variant="h6" fontWeight="bold">
                                Search Filters
                            </Typography>
                            <Button 
                                variant="outlined" 
                                color="secondary" 
                                onClick={handleFetchRandom}
                                startIcon={<AutoAwesomeIcon />}
                            >
                                Fetch Random Characters
                            </Button>
                        </Box>
                        <Grid container spacing={2} alignItems="center">
                            <Grid size={{ xs: 12, sm: 12, md: 4 }}>
                                <TextField
                                    fullWidth
                                    label="Character Name"
                                    variant="outlined"
                                    size="small"
                                    value={charName}
                                    onChange={(e) => setCharName(e.target.value)}
                                    placeholder="e.g. Neo"
                                />
                            </Grid>
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
                            <Grid size={{ xs: 12, sm: 6, md: 2 }}>
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
                            <Grid size={{ xs: 12, sm: 6, md: 1 }}>
                                <TextField
                                    fullWidth
                                    label="Rating"
                                    variant="outlined"
                                    size="small"
                                    type="number"
                                    inputProps={{ min: 0, max: 10, step: 0.1 }}
                                    value={minRating}
                                    onChange={(e) => setMinRating(e.target.value)}
                                />
                            </Grid>
                            <Grid size={{ xs: 12, sm: 6, md: 1 }}>
                                <TextField
                                    fullWidth
                                    label="Year"
                                    variant="outlined"
                                    size="small"
                                    value={year}
                                    onChange={(e) => setYear(e.target.value)}
                                />
                            </Grid>
                            <Grid size={{ xs: 12, md: 1 }}>
                                <Button
                                    fullWidth
                                    variant="contained"
                                    onClick={handleSearch}
                                    startIcon={<SearchIcon />}
                                    sx={{ height: '40px' }}
                                >
                                    Go
                                </Button>
                            </Grid>
                        </Grid>
                    </Paper>

                    <Box sx={{ width: '100%' }}>
                        <Typography variant="h6" gutterBottom fontWeight="bold">
                            Results {randomSeed && randomData?.results ? `(${randomData.results.length} random)` : searchData?.results ? `(${searchData.results.length})` : ''}
                        </Typography>
                        
                        {(isSearchLoading || isRandomLoading) && (
                            <Box sx={{ display: 'flex', justifyContent: 'center', p: 5 }}>
                                <CircularProgress />
                            </Box>
                        )}
                        
                        {(isSearchError || isRandomError) && (
                            <Alert severity="error">
                                Error fetching movie characters: {((searchError || randomError) as any)?.message}
                            </Alert>
                        )}

                        {!(isSearchLoading || isRandomLoading) && !(isSearchError || isRandomError) && (randomSeed ? randomData?.results : searchData?.results) && (
                            <Box sx={{ overflowX: 'auto' }}>
                                <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                    <thead>
                                        <tr style={{ borderBottom: '2px solid #ccc' }}>
                                            <th style={{ padding: '8px' }}>Character Name</th>
                                            <th style={{ padding: '8px' }}>Movie Title</th>
                                            <th style={{ padding: '8px' }}>Genres</th>
                                            <th style={{ padding: '8px' }}>Year</th>
                                            <th style={{ padding: '8px' }}>Rating</th>
                                            <th style={{ padding: '8px' }}>Action</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {(randomSeed ? randomData!.results : searchData!.results).map((char) => {
                                            const isSelected = !!selectedCharacters.find(c => c.character_id === char.character_id);
                                            return (
                                                <tr key={char.character_id} style={{ borderBottom: '1px solid #eee', backgroundColor: isSelected ? 'rgba(25, 118, 210, 0.08)' : 'transparent' }}>
                                                    <td style={{ padding: '12px 8px', fontWeight: 'bold' }}>{char.character_name}</td>
                                                    <td style={{ padding: '12px 8px' }}>
                                                        <Button 
                                                            variant="text" 
                                                            onClick={() => handleMovieClick(char.movie_title)}
                                                            sx={{ 
                                                                textTransform: 'none', 
                                                                p: 0, 
                                                                minWidth: 0, 
                                                                textAlign: 'left',
                                                                color: 'primary.main',
                                                                '&:hover': { textDecoration: 'underline', bgcolor: 'transparent' }
                                                            }}
                                                        >
                                                            {char.movie_title}
                                                        </Button>
                                                    </td>
                                                    <td style={{ padding: '12px 8px' }}>{char.movie_genres.join(', ')}</td>
                                                    <td style={{ padding: '12px 8px' }}>{char.movie_year}</td>
                                                    <td style={{ padding: '12px 8px' }}>{char.movie_imdb_rating}</td>
                                                    <td style={{ padding: '12px 8px' }}>
                                                        <IconButton 
                                                            size="small" 
                                                            onClick={() => isSelected ? handleRemoveCharacter(char.character_id) : handleAddCharacter(char)}
                                                            color={isSelected ? "error" : "primary"}
                                                        >
                                                            {isSelected ? <DeleteIcon /> : <AddIcon />}
                                                        </IconButton>
                                                    </td>
                                                </tr>
                                            );
                                        })}
                                        {(randomSeed ? randomData!.results : searchData!.results).length === 0 && (
                                            <tr>
                                                <td colSpan={5} style={{ textAlign: 'center', padding: '24px', color: 'gray' }}>
                                                    No characters found matching your filters.
                                                </td>
                                            </tr>
                                        )}
                                    </tbody>
                                </table>
                            </Box>
                        )}
                    </Box>
                </Grid>
            </Grid>
        </Box>
    );
};

export default MovieCharacterSearch;
