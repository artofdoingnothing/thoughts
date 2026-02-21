import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import type { Thought } from '../types';

export function useThoughts(params: { page: number; limit?: number; tag?: string; emotion?: string; persona_id?: string }) {
    return useQuery({
        queryKey: ['thoughts', params],
        queryFn: async () => {
            const queryParams: Record<string, any> = { page: params.page, limit: params.limit || 50 };
            if (params.tag) queryParams.tag = params.tag;
            if (params.emotion) queryParams.emotion = params.emotion;
            if (params.persona_id) queryParams.persona_id = params.persona_id;

            const { data } = await api.get<{ items: Thought[], total: number, page: number, limit: number }>('/thoughts/', { params: queryParams });
            return data;
        },
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateThought() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (payload: { content: string; emotions?: string[] }) => {
            const { data } = await api.post('/thoughts/', payload);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['thoughts'] });
        },
    });
}

export function useDeleteThought() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (id: number) => {
            const { data } = await api.delete(`/thoughts/${id}`);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['thoughts'] });
        },
    });
}
