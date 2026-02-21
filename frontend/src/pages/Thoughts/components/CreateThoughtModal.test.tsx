import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CreateThoughtModal from './CreateThoughtModal';

describe('CreateThoughtModal', () => {
    it('renders without crashing', () => {
        const props = { open: true, onClose: () => {}, onSuccess: () => {} } as any;
        const queryClient = new QueryClient();
        const { container } = render(
            <QueryClientProvider client={queryClient}>
                <CreateThoughtModal {...props} />
            </QueryClientProvider>
        );
        expect(container).toBeInTheDocument();
    });
});
