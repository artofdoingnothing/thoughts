import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CreatePersonaModal from './CreatePersonaModal';

describe('CreatePersonaModal', () => {
    it('renders without crashing', () => {
        const queryClient = new QueryClient();
        const props = { open: true, handleClose: () => {}, handlePersonaCreated: () => {} } as any;
        const { container } = render(
            <QueryClientProvider client={queryClient}>
                <CreatePersonaModal {...props} />
            </QueryClientProvider>
        );
        expect(container).toBeInTheDocument();
    });
});
