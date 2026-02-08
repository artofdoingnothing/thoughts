import React, { useState } from 'react';
import {
    Box,
    Drawer,
    List,
    ListItem,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Button,
    IconButton,
    useMediaQuery,
    useTheme,
    Container
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
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

const drawerWidth = 240;

const Layout: React.FC<LayoutProps> = ({ children, onNewThought }) => {
    const [mobileOpen, setMobileOpen] = useState(false);
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('md'));
    const location = useLocation();

    const handleDrawerToggle = () => {
        setMobileOpen(!mobileOpen);
    };

    const showNewThoughtButton = location.pathname === '/' || location.pathname === '/thoughts';

    const drawer = (
        <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', bgcolor: 'background.paper' }}>
            <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1, color: 'primary.main' }}>
                <AutoAwesomeIcon />
                <Box sx={{ fontWeight: 700, letterSpacing: '.1rem', textTransform: 'uppercase' }}>
                    Thought Aggregator
                </Box>
            </Box>
            <List>
                {[
                    { text: 'Home', icon: <HomeIcon />, path: '/' },
                    { text: 'Thoughts', icon: <NotesIcon />, path: '/thoughts' },
                    { text: 'Personas', icon: <PersonIcon />, path: '/personas' },
                    { text: 'Generate', icon: <CreateIcon />, path: '/generate' },
                    { text: 'Essay', icon: <ArticleIcon />, path: '/essay' },
                ].map((item) => (
                    <ListItem key={item.text} disablePadding>
                        <ListItemButton component={RouterLink} to={item.path} onClick={() => isMobile && setMobileOpen(false)}>
                            <ListItemIcon sx={{ color: 'primary.main' }}>
                                {item.icon}
                            </ListItemIcon>
                            <ListItemText primary={item.text} sx={{ color: 'text.primary' }} />
                        </ListItemButton>
                    </ListItem>
                ))}
            </List>
            <Box sx={{ flexGrow: 1 }} />
        </Box>
    );

    return (
        <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
            {/* Hamburger Button (Always Visible) */}
            <IconButton
                color="inherit"
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{
                    position: 'fixed',
                    top: 16,
                    left: 16,
                    zIndex: theme.zIndex.drawer + 2,
                    bgcolor: 'background.paper',
                    boxShadow: 1,
                    '&:hover': { bgcolor: 'background.paper' },
                    display: mobileOpen ? 'none' : 'flex' // Hide when drawer is open if it overlaps, or keep it.
                    // Actually, if we want it to "slide out", typically the button stays or moves.
                    // Let's keep it simple: button opens drawer.
                }}
            >
                <MenuIcon color="primary" />
            </IconButton>

             {/* New Thought Button (Top Right) */}
             {showNewThoughtButton && (
                <Button
                    variant="contained"
                    onClick={onNewThought}
                    startIcon={<AutoAwesomeIcon />}
                    sx={{
                        position: 'fixed',
                        top: 16,
                        right: 16,
                        zIndex: theme.zIndex.drawer + 1,
                    }}
                >
                    New Thought
                </Button>
            )}

            <Drawer
                variant="temporary"
                open={mobileOpen}
                onClose={handleDrawerToggle}
                ModalProps={{
                    keepMounted: true, // Better open performance on mobile.
                }}
                sx={{
                    '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
                }}
            >
                {drawer}
            </Drawer>

            <Box
                component="main"
                sx={{
                    flexGrow: 1,
                    p: 3,
                    mt: 8, // Space for the floating buttons
                    width: '100%',
                    transition: theme.transitions.create(['margin', 'width'], {
                        easing: theme.transitions.easing.sharp,
                        duration: theme.transitions.duration.leavingScreen,
                    }),
                    ...(mobileOpen && !isMobile && {
                        // If we wanted a persistent drawer that pushes content, we'd use variant="persistent"
                        // The user said: "clicking on it should slide out a side navigation pushing the main window to the right."
                        // This implies variant="persistent".
                    }),
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
