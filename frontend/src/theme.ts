import { createTheme } from '@mui/material/styles';

declare module '@mui/material/styles' {
    interface Palette {
        deepBlue: Palette['primary'];
        mediumBlue: Palette['primary'];
        lightBlue: Palette['primary'];
        deepRed: Palette['primary'];
        mediumRed: Palette['primary'];
        lightRed: Palette['primary'];
    }
    interface PaletteOptions {
        deepBlue?: PaletteOptions['primary'];
        mediumBlue?: PaletteOptions['primary'];
        lightBlue?: PaletteOptions['primary'];
        deepRed?: PaletteOptions['primary'];
        mediumRed?: PaletteOptions['primary'];
        lightRed?: PaletteOptions['primary'];
    }
}

const theme = createTheme({
    palette: {
        primary: {
            main: '#2563eb', // medium-blue as primary
            light: '#dbeafe', // light-blue
            dark: '#1e3a8a', // deep-blue
            contrastText: '#ffffff',
        },
        secondary: {
            main: '#6b7280', // grey-medium
            light: '#f3f4f6', // grey-light
            dark: '#374151', // grey-dark
            contrastText: '#ffffff',
        },
        error: {
            main: '#dc2626', // medium-red
            light: '#fee2e2', // light-red
            dark: '#991b1b', // deep-red
            contrastText: '#ffffff',
        },
        background: {
            default: '#f9fafb', // surface
            paper: '#ffffff', // background
        },
        text: {
            primary: '#1a1a1a',
            secondary: '#4a4a4a',
            disabled: '#6b7280', // text-muted
        },
        deepBlue: {
            main: '#1e3a8a',
            light: '#2563eb',
            contrastText: '#ffffff',
        },
        mediumBlue: {
            main: '#2563eb',
            light: '#dbeafe',
            contrastText: '#ffffff',
        },
        lightBlue: {
            main: '#dbeafe',
            contrastText: '#1e3a8a',
        },
        deepRed: {
            main: '#991b1b',
            contrastText: '#ffffff',
        },
        mediumRed: {
            main: '#dc2626',
            light: '#fee2e2',
            contrastText: '#ffffff',
        },
        lightRed: {
            main: '#fee2e2',
            contrastText: '#991b1b',
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontWeight: 700,
            fontSize: '2.5rem',
            letterSpacing: '-0.02em',
            color: '#1e3a8a', // deep-blue
        },
        h2: {
            fontWeight: 700,
            letterSpacing: '-0.01em',
            color: '#1e3a8a',
        },
        h3: {
            fontWeight: 600,
            color: '#1e3a8a',
        },
        h4: {
            fontWeight: 600,
            letterSpacing: '0.01em',
            color: '#1e3a8a',
        },
        h5: {
            fontWeight: 600,
            color: '#1e3a8a',
        },
        h6: {
            fontWeight: 600,
            color: '#1e3a8a',
        },
        button: {
            fontWeight: 600,
            textTransform: 'none',
            borderRadius: '8px',
        },
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: '8px',
                    padding: '8px 20px',
                    boxShadow: 'none',
                    textTransform: 'none',
                    fontWeight: 600,
                    transition: 'all 0.2s ease-in-out',
                    '&:hover': {
                        transform: 'translateY(-1px)',
                        boxShadow: 'none',
                    },
                },
                containedPrimary: {
                    background: '#2563eb', // medium-blue
                    color: '#ffffff',
                    '&:hover': {
                        background: '#1d4ed8', // blue-hover
                        boxShadow: 'none',
                    },
                },
                containedSecondary: {
                    background: '#6b7280', // grey-bg
                    color: '#ffffff',
                    '&:hover': {
                         background: '#4b5563', // grey-hover-bg
                         boxShadow: 'none',
                    },
                },
                containedError: {
                    background: '#dc2626', // medium-red
                    color: '#ffffff',
                    '&:hover': {
                        background: '#b91c1c', // red-hover
                        boxShadow: 'none',
                    },
                },
                outlinedPrimary: {
                    borderColor: '#2563eb',
                    color: '#1e40af',
                    '&:hover': {
                        background: '#dbeafe',
                        borderColor: '#2563eb',
                    },
                },
                outlinedSecondary: {
                    borderColor: '#9ca3af',
                    color: '#4a4a4a',
                    '&:hover': {
                        background: '#f3f4f6',
                        borderColor: '#9ca3af',
                    },
                },
                outlinedError: {
                    borderColor: '#dc2626',
                    color: '#b91c1c',
                    '&:hover': {
                        background: '#fee2e2',
                        borderColor: '#dc2626',
                    },
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: '16px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03)',
                    border: '1px solid #e5e7eb', // border color
                    transition: 'all 0.2s ease-in-out',
                    backgroundColor: '#ffffff',
                    '&:hover': {
                        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.03)',
                        borderColor: '#dbeafe', // light-blue
                    },
                },
            },
        },
        MuiPaper: {
            styleOverrides: {
                root: {
                    backgroundImage: 'none',
                },
            },
        },
        MuiAppBar: {
            styleOverrides: {
                root: {
                    backgroundColor: '#ffffff',
                    color: '#1e3a8a',
                    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                },
            },
        },
        MuiDrawer: {
            styleOverrides: {
                paper: {
                    backgroundColor: '#1e3a8a', // deep-blue
                    color: '#ffffff',
                },
            },
        },
    },
});

export default theme;
