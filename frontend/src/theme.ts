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
            main: '#8b0000', // dusty-grape
            light: '#c10000', // slate-grey
            contrastText: '#ffffff',
        },
        secondary: {
            main: '#ff4949', // muted-teal
            contrastText: '#ffffff',
        },
        background: {
            default: '#eeeeee', // pale-oak
            paper: '#ffffff',
        },
        paleOak: {
            main: '#eeeeee',
        },
        ashGrey: {
            main: '#dedede',
        },
        mutedTeal: {
            main: '#ff4949',
        },
        slateGrey: {
            main: '#c10000',
        },
        dustyGrape: {
            main: '#8b0000',
        },
    },
    typography: {
        fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontWeight: 700,
            fontSize: '2.5rem',
            letterSpacing: '-0.02em',
            color: '#8b0000', // dusty-grape
        },
        h4: {
            fontWeight: 600,
            letterSpacing: '0.05em',
            color: '#c10000', // slate-grey
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
                        boxShadow: '0 4px 12px rgba(139, 0, 0, 0.2)', // dusty-grape shadow
                    },
                },
                containedPrimary: {
                    background: 'linear-gradient(135deg, #8b0000 0%, #c10000 100%)', // dusty-grape to slate-grey
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: '16px',
                    boxShadow: '0 4px 20px rgba(0,0,0,0.05)',
                    border: '1px solid rgba(238, 238, 238, 0.5)', // pale-oak border
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
