import { useQuery } from '@tanstack/react-query';
import { api } from '../api';
import type { MovieSearchResponse } from '../types';

interface SearchMovieCharactersParams {
    title?: string;
    genre?: string;
    min_rating?: number;
    year?: string;
}

export function useMovieCharacters(params: SearchMovieCharactersParams) {
    return useQuery<MovieSearchResponse>({
        queryKey: ['movieCharacters', params],
        queryFn: async () => {
            const { data } = await api.get('/dataset/characters', { params });
            return data;
        },
        // We might not want to automatically refetch or fetch when empty, 
        // but given it's a search, we can let the user control it or fetch if params exist
        enabled: true,
    });
}
