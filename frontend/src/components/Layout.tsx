import React from 'react';
import {
    Box,
    AppBar,
    Toolbar,
    Button,
    Container,
    Typography
} from '@mui/material';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import HomeIcon from '@mui/icons-material/Home';
import NotesIcon from '@mui/icons-material/Notes';
import PersonIcon from '@mui/icons-material/Person';
import CreateIcon from '@mui/icons-material/Create';
import ArticleIcon from '@mui/icons-material/Article';
import { Link as RouterLink, useLocation } from 'react-router-dom';

interface LayoutProps {
    children: React.ReactNode;
    onNewThought: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, onNewThought }) => {
    const location = useLocation();

    const showNewThoughtButton = location.pathname === '/' || location.pathname === '/thoughts';

    const navItems = [
        { text: 'Home', icon: <HomeIcon />, path: '/' },
        { text: 'Thoughts', icon: <NotesIcon />, path: '/thoughts' },
        { text: 'Personas', icon: <PersonIcon />, path: '/personas' },
        { text: 'Generate', icon: <CreateIcon />, path: '/generate' },
        { text: 'Essay', icon: <ArticleIcon />, path: '/essay' },
    ];

    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: 'background.default' }}>
            <AppBar position="sticky" color="inherit" elevation={1}>
                <Container maxWidth="xl">
                    <Toolbar disableGutters>
                        <AutoAwesomeIcon sx={{ display: { xs: 'none', md: 'flex' }, mr: 1, color: 'primary.main' }} />
                        <Typography
                            variant="h6"
                            noWrap
                            component={RouterLink}
                            to="/"
                            sx={{
                                mr: 2,
                                display: { xs: 'none', md: 'flex' },
                                fontFamily: 'monospace',
                                fontWeight: 700,
                                letterSpacing: '.3rem',
                                color: 'primary.main',
                                textDecoration: 'none',
                                flexGrow: 0
                            }}
                        >
                            THOUGHT AGGREGATOR
                        </Typography>

                        <Box sx={{ flexGrow: 1, display: 'flex', gap: 1 }}>
                            {navItems.map((item) => (
                                <Button
                                    key={item.text}
                                    component={RouterLink}
                                    to={item.path}
                                    startIcon={item.icon}
                                    sx={{
                                        my: 2,
                                        color: location.pathname === item.path ? 'primary.main' : 'text.primary',
                                        display: 'flex'
                                    }}
                                >
                                    {item.text}
                                </Button>
                            ))}
                        </Box>

                        {showNewThoughtButton && (
                            <Button
                                variant="contained"
                                onClick={onNewThought}
                                startIcon={<AutoAwesomeIcon />}
                                sx={{ ml: 2 }}
                            >
                                New Thought
                            </Button>
                        )}
                    </Toolbar>
                </Container>
            </AppBar>

            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3,
                    width: '100%',
                }}
            >
                 <Container maxWidth="xl">
                    {children}
                </Container>
            </Box>
        </Box>
    );
};

export default Layout;
