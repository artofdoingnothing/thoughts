import { useState, useEffect } from 'react';
import {
    Dialog, DialogTitle, DialogContent, DialogActions, Button, TextField,
    Box, IconButton, Typography, Stack
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import AddIcon from '@mui/icons-material/Add';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface CreatePersonaModalProps {
    open: boolean;
    onClose: () => void;
    onSuccess: () => void;
    initialData?: any; // For edit mode
}

export default function CreatePersonaModal({ open, onClose, onSuccess, initialData }: CreatePersonaModalProps) {
    const [name, setName] = useState('');
    const [age, setAge] = useState<number | string>('');
    const [gender, setGender] = useState('');
    const [additionalInfo, setAdditionalInfo] = useState<{ key: string; value: string }[]>([]);
    const [isGenerating, setIsGenerating] = useState(false);

    useEffect(() => {
        if (open) {
            if (initialData) {
                setName(initialData.name);
                setAge(initialData.age);
                setGender(initialData.gender);
                if (initialData.additional_info) {
                    const info = Object.entries(initialData.additional_info).map(([key, value]) => ({
                        key,
                        value: String(value)
                    }));
                    setAdditionalInfo(info);
                } else {
                    setAdditionalInfo([]);
                }
            } else {
                // Reset form
                setName('');
                setAge('');
                setGender('');
                setAdditionalInfo([]);
            }
        }
    }, [open, initialData]);

    const handleGenerateName = async () => {
        setIsGenerating(true);
        try {
            const response = await fetch(`${API_BASE_URL}/personas/generate-name`, {
                method: 'POST',
            });
            if (response.ok) {
                const data = await response.json();
                setName(data.name);
            }
        } catch (error) {
            console.error('Failed to generate name:', error);
        } finally {
            setIsGenerating(false);
        }
    };

    const handleAddInfo = () => {
        setAdditionalInfo([...additionalInfo, { key: '', value: '' }]);
    };

    const handleInfoChange = (index: number, field: 'key' | 'value', value: string) => {
        const newInfo = [...additionalInfo];
        newInfo[index][field] = value;
        setAdditionalInfo(newInfo);
    };

    const handleRemoveInfo = (index: number) => {
        const newInfo = [...additionalInfo];
        newInfo.splice(index, 1);
        setAdditionalInfo(newInfo);
    };

    const handleSubmit = async () => {
        const infoObject = additionalInfo.reduce((acc, curr) => {
            if (curr.key.trim()) {
                acc[curr.key.trim()] = curr.value;
            }
            return acc;
        }, {} as Record<string, any>);

        const payload = {
            name,
            age: Number(age),
            gender,
            additional_info: infoObject
        };

        try {
            const url = initialData 
                ? `${API_BASE_URL}/personas/${initialData.id}`
                : `${API_BASE_URL}/personas/`;
            
            const method = initialData ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                onSuccess();
                onClose();
            } else {
                console.error('Failed to save persona');
            }
        } catch (error) {
            console.error('Error saving persona:', error);
        }
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
            <DialogTitle>{initialData ? 'Edit Persona' : 'Create New Persona'}</DialogTitle>
            <DialogContent>
                <Stack spacing={2} sx={{ mt: 1 }}>
                    <Box sx={{ display: 'flex', gap: 1 }}>
                        <TextField
                            autoFocus
                            label="Name"
                            fullWidth
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                        <Button
                            variant="outlined"
                            onClick={handleGenerateName}
                            disabled={isGenerating}
                            startIcon={<AutoFixHighIcon />}
                        >
                            Generate
                        </Button>
                    </Box>
                    <TextField
                        label="Age"
                        type="number"
                        fullWidth
                        value={age}
                        onChange={(e) => setAge(e.target.value)}
                    />
                    <TextField
                        label="Gender"
                        fullWidth
                        value={gender}
                        onChange={(e) => setGender(e.target.value)}
                    />

                    <Typography variant="subtitle1" sx={{ mt: 2 }}>
                        Additional Information
                    </Typography>
                    {additionalInfo.map((info, index) => (
                        <Box key={index} sx={{ display: 'flex', gap: 1 }}>
                            <TextField
                                label="Key"
                                size="small"
                                value={info.key}
                                onChange={(e) => handleInfoChange(index, 'key', e.target.value)}
                                sx={{ flex: 1 }}
                            />
                            <TextField
                                label="Value"
                                size="small"
                                value={info.value}
                                onChange={(e) => handleInfoChange(index, 'value', e.target.value)}
                                sx={{ flex: 1 }}
                            />
                            <IconButton onClick={() => handleRemoveInfo(index)} color="error">
                                <DeleteIcon />
                            </IconButton>
                        </Box>
                    ))}
                    <Button startIcon={<AddIcon />} onClick={handleAddInfo} size="small">
                        Add Field
                    </Button>
                </Stack>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>Cancel</Button>
                <Button onClick={handleSubmit} variant="contained">
                    Save
                </Button>
            </DialogActions>
        </Dialog>
    );
}
