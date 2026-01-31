import { createTheme } from '@mui/material/styles';

declare module '@mui/material/styles' {
    interface Palette {
        paleOak: Palette['primary'];
        ashGrey: Palette['primary'];
        mutedTeal: Palette['primary'];
        slateGrey: Palette['primary'];
        dustyGrape: Palette['primary'];
    }
    interface PaletteOptions {
        paleOak?: PaletteOptions['primary'];
        ashGrey?: PaletteOptions['primary'];
        mutedTeal?: PaletteOptions['primary'];
        slateGrey?: PaletteOptions['primary'];
        dustyGrape?: PaletteOptions['primary'];
    }
}

const theme = createTheme({
    palette: {
        primary: {
            main: '#545775', // dusty-grape
            light: '#718f94', // slate-grey (using as light var for now, or just auto)
            contrastText: '#ffffff',
        },
        secondary: {
            main: '#90b494', // muted-teal
            contrastText: '#ffffff',
        },
        background: {
            default: '#fdfbf7', // Very light version of pale-oak
            paper: '#ffffff',
        },
        paleOak: {
            main: '#dbcfb0',
        },
        ashGrey: {
            main: '#bfc8ad',
        },
        mutedTeal: {
            main: '#90b494',
        },
        slateGrey: {
            main: '#718f94',
        },
        dustyGrape: {
            main: '#545775',
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontWeight: 700,
            fontSize: '2.5rem',
            letterSpacing: '-0.02em',
            color: '#545775', // dusty-grape
        },
        h4: {
            fontWeight: 600,
            letterSpacing: '0.05em',
            color: '#718f94', // slate-grey
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
                    borderRadius: '12px',
                    padding: '10px 24px',
                    boxShadow: 'none',
                    '&:hover': {
                        boxShadow: '0 4px 12px rgba(84, 87, 117, 0.2)', // dusty-grape shadow
                    },
                },
                containedPrimary: {
                    background: 'linear-gradient(135deg, #545775 0%, #718f94 100%)', // dusty-grape to slate-grey
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: '16px',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
                    border: '1px solid rgba(219, 207, 176, 0.3)', // pale-oak border
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
    },
});

export default theme;
