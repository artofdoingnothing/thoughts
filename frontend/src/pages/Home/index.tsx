import React from 'react';
import { Box, Typography, Container } from '@mui/material';

const HomePage: React.FC = () => {
    return (
        <Container maxWidth="md">
            <Box sx={{ mt: 8, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                <Typography variant="h2" component="h1" gutterBottom sx={{ color: 'primary.main', fontWeight: 700 }}>
                    Thought Aggregator
                </Typography>
                <Typography variant="h5" color="text.secondary" paragraph align="center">
                    Welcome. Select an option from the menu to begin.
                </Typography>
            </Box>
        </Container>
    );
};

export default HomePage;
