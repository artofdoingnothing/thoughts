import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ConversationGenerator from './index';

describe('ConversationGenerator Page', () => {
    it('renders without crashing', () => {
        const queryClient = new QueryClient();
        const { container } = render(
            <QueryClientProvider client={queryClient}>
                <MemoryRouter>
                    <ConversationGenerator />
                </MemoryRouter>
            </QueryClientProvider>
        );
        expect(container).toBeInTheDocument();
    });
});
