import React, { useState } from 'react';
import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
    Box,
    Chip,
    Typography,
    CircularProgress
} from '@mui/material';
import axios from 'axios';

interface CreateThoughtModalProps {
    open: boolean;
    onClose: () => void;
    onSuccess: () => void;
    apiBaseUrl: string;
}

const AVAILABLE_EMOTIONS = ['Happy', 'Sad', 'Angry', 'Anxious', 'Excited', 'Calm'];

const CreateThoughtModal: React.FC<CreateThoughtModalProps> = ({ open, onClose, onSuccess, apiBaseUrl }) => {
    const [content, setContent] = useState('');
    const [selectedEmotions, setSelectedEmotions] = useState<string[]>([]);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e?: React.FormEvent) => {
        if (e) e.preventDefault();
        if (!content) return;

        setLoading(true);
        try {
            await axios.post(`${apiBaseUrl}/thoughts/`, {
                content,
                emotions: selectedEmotions
            });
            setContent('');
            setSelectedEmotions([]);
            onSuccess();
            onClose();
        } catch (error) {
            console.error('Error creating thought:', error);
            // Ideally show error toast
        } finally {
            setLoading(false);
        }
    };

    const toggleEmotion = (emotion: string) => {
        setSelectedEmotions(prev =>
            prev.includes(emotion) ? prev.filter(e => e !== emotion) : [...prev, emotion]
        );
    };

    return (
        <Dialog open={open} onClose={onClose} fullWidth maxWidth="sm">
            <DialogTitle sx={{ fontWeight: 700, color: 'primary.main' }}>NEW THOUGHT</DialogTitle>
            <DialogContent>
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label="Content"
                        fullWidth
                        required
                        multiline
                        rows={4}
                        value={content}
                        onChange={(e) => setContent(e.target.value)}
                        placeholder="What's on your mind?"
                        disabled={loading}
                    />

                    <Box>
                        <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>EMOTIONS</Typography>
                        <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                            {AVAILABLE_EMOTIONS.map((emotion) => (
                                <Chip
                                    key={emotion}
                                    label={emotion}
                                    clickable
                                    onClick={() => toggleEmotion(emotion)}
                                    color={selectedEmotions.includes(emotion) ? 'primary' : 'default'}
                                    variant={selectedEmotions.includes(emotion) ? 'filled' : 'outlined'}
                                    disabled={loading}
                                />
                            ))}
                        </Box>
                    </Box>
                </Box>
            </DialogContent>
            <DialogActions sx={{ p: 3 }}>
                <Button onClick={onClose} disabled={loading} color="inherit">Cancel</Button>
                <Button
                    onClick={() => handleSubmit()}
                    disabled={loading || !content}
                    variant="contained"
                    color="primary"
                >
                    {loading ? <CircularProgress size={24} /> : 'Save Thought'}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default CreateThoughtModal;
