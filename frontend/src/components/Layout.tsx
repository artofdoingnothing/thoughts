import React from 'react';
import { AppBar, Toolbar, Typography, Container, Box, Button } from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import { Link as RouterLink } from 'react-router-dom';

interface LayoutProps {
    children: React.ReactNode;
    onNewThought: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, onNewThought }) => {
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: 'background.default' }}>
            <AppBar position="sticky" elevation={0} sx={{
                bgcolor: 'background.paper',
                borderBottom: 1,
                borderColor: 'divider',
                color: 'text.primary'
            }}>
                <Container maxWidth="xl">
                    <Toolbar disableGutters sx={{ justifyContent: 'space-between' }}>
                        <Box sx={{ display: 'flex', items: 'center', gap: 1 }}>
                            <AutoAwesomeIcon sx={{ color: 'primary.main' }} />
                            <Typography
                                variant="h6"
                                noWrap
                                component="div"
                                sx={{
                                    fontWeight: 700,
                                    letterSpacing: '.1rem',
                                    color: 'primary.main',
                                    textDecoration: 'none',
                                    textTransform: 'uppercase'
                                }}
                            >
                                Thought Aggregator
                            </Typography>
                        </Box>

                        <Box sx={{ display: 'flex', gap: 2 }}>
                            <Button color="inherit" component={RouterLink} to="/" sx={{ color: 'primary.main' }}>Thoughts</Button>
                            <Button color="inherit" component={RouterLink} to="/personas" sx={{ color: 'primary.main' }}>Personas</Button>
                            <Button color="inherit" component={RouterLink} to="/generate" sx={{ color: 'primary.main' }}>Generate</Button>
                        </Box>

                        <Button
                            variant="contained"
                            onClick={onNewThought}
                            startIcon={<AutoAwesomeIcon />}
                        >
                            New Thought
                        </Button>
                    </Toolbar>
                </Container>
            </AppBar>

            <Container maxWidth="xl" component="main" sx={{ flexGrow: 1, py: 4 }}>
                {children}
            </Container>
        </Box>
    );
};

export default Layout;
