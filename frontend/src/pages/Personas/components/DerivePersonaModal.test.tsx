import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import DerivePersonaModal from './DerivePersonaModal';

describe('DerivePersonaModal', () => {
    it('renders without crashing', () => {
        const queryClient = new QueryClient();
        const props = { open: true, onClose: () => {}, sourcePersonaId: null, isGenMode: false } as any;
        const { container } = render(
            <QueryClientProvider client={queryClient}>
                <DerivePersonaModal {...props} />
            </QueryClientProvider>
        );
        expect(container).toBeInTheDocument();
    });
});
