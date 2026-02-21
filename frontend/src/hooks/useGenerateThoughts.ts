import { useMutation } from '@tanstack/react-query';
import { api } from '../api';

interface GenerateThoughtsPayload {
    urls: string[];
    persona_id: number;
}

export function useGenerateThoughts() {
    return useMutation({
        mutationFn: async (payload: GenerateThoughtsPayload) => {
            const { data } = await api.post('/generate-thoughts/', payload);
            return data;
        },
    });
}
