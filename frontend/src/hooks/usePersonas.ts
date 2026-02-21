import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../api';
import type { Persona } from '../types';

export function usePersonas() {
    return useQuery<Persona[]>({
        queryKey: ['personas'],
        queryFn: async () => {
            const { data } = await api.get('/personas/');
            return data;
        },
    });
}

export function useCreatePersona() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (payload: any) => {
            const { data } = await api.post('/personas/', payload);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['personas'] });
        },
    });
}

export function useUpdatePersona() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async ({ id, payload }: { id: number; payload: any }) => {
            const { data } = await api.put(`/personas/${id}`, payload);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['personas'] });
        },
    });
}

export function useDerivePersona() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (payload: { source_persona_id: number; name_adjective: string; percentage: number }) => {
            const { data } = await api.post('/personas/derive', payload);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['personas'] });
        },
    });
}

export function useRegeneratePersona() {
    const queryClient = useQueryClient();
    return useMutation({
        mutationFn: async (id: number) => {
            const { data } = await api.post(`/personas/${id}/regenerate`);
            return data;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['personas'] });
        },
    });
}
