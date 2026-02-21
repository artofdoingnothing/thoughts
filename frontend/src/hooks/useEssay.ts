import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from '../api';

export function useEssayStatus(jobId: string | null) {
    return useQuery({
        queryKey: ['essayStatus', jobId],
        queryFn: async () => {
            const { data } = await api.get(`/essay/status/${jobId}`);
            return data;
        },
        enabled: !!jobId,
        refetchInterval: (query) => {
            const data = query.state.data;
            if (data?.status === 'finished' || data?.status === 'failed') {
                return false;
            }
            return 2000;
        },
    });
}

interface GenerateEssayPayload {
    starting_text: string;
    persona_id: number;
}

export function useGenerateEssay() {
    return useMutation({
        mutationFn: async (payload: GenerateEssayPayload) => {
            const { data } = await api.post('/essay/generate', payload);
            return data;
        },
    });
}
