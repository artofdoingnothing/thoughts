import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import type { Conversation } from '../types';

export function useConversations(refetchInterval: number | false = false) {
    return useQuery<Conversation[]>({
        queryKey: ['conversations'],
        queryFn: async () => {
            const { data } = await api.get('/conversations/');
            return data;
        },
        refetchInterval,
    });
}

export function useCreateConversation() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (payload: { title: string; context: string; persona_ids: number[] }) => {
            const { data } = await api.post('/conversations/', payload);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['conversations'] });
        },
    });
}

export function useGenerateMessage() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async ({ conversationId, personaId }: { conversationId: number; personaId: number }) => {
            const { data } = await api.post(`/conversations/${conversationId}/generate`, { persona_id: personaId });
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['conversations'] });
        },
    });
}

export function useAddPersonaToConversation() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async ({ conversationId, personaId }: { conversationId: number; personaId: number }) => {
            const { data } = await api.post(`/conversations/${conversationId}/personas`, { persona_id: personaId });
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['conversations'] });
        },
    });
}

export function useGenerateSequence() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async ({ conversationId, personaIds }: { conversationId: number; personaIds: number[] }) => {
            const { data } = await api.post(`/conversations/${conversationId}/generate_sequence`, { persona_ids: personaIds });
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['conversations'] });
        },
    });
}

export function useEndConversation() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (conversationId: number) => {
            const { data } = await api.post(`/conversations/${conversationId}/end`);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['conversations'] });
        },
    });
}
