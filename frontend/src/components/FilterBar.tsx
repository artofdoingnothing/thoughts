import React from 'react';
import { Box, TextField, InputAdornment } from '@mui/material';
import TagIcon from '@mui/icons-material/Tag';
import EmojiEmotionsIcon from '@mui/icons-material/EmojiEmotions';

interface FilterBarProps {
    searchTag: string;
    setSearchTag: (value: string) => void;
    searchEmotion: string;
    setSearchEmotion: (value: string) => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ searchTag, setSearchTag, searchEmotion, setSearchEmotion }) => {
    return (
        <Box sx={{ display: 'flex', gap: 2, mb: 4, flexWrap: 'wrap' }}>
            <TextField
                label="Filter by Tag"
                variant="outlined"
                size="small"
                value={searchTag}
                onChange={(e) => setSearchTag(e.target.value)}
                sx={{ bgcolor: 'background.paper', minWidth: 200 }}
                slotProps={{
                    input: {
                        startAdornment: (
                            <InputAdornment position="start">
                                <TagIcon color="action" />
                            </InputAdornment>
                        ),
                    },
                }}
            />
            <TextField
                label="Filter by Emotion"
                variant="outlined"
                size="small"
                value={searchEmotion}
                onChange={(e) => setSearchEmotion(e.target.value)}
                sx={{ bgcolor: 'background.paper', minWidth: 200 }}
                slotProps={{
                    input: {
                        startAdornment: (
                            <InputAdornment position="start">
                                <EmojiEmotionsIcon color="action" />
                            </InputAdornment>
                        ),
                    },
                }}
            />
        </Box>
    );
};

export default FilterBar;
