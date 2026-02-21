import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import ThoughtGenerator from './index';

describe('ThoughtGenerator Page', () => {
    it('renders without crashing', () => {
        const queryClient = new QueryClient();
        const { container } = render(
            <QueryClientProvider client={queryClient}>
                <MemoryRouter>
                    <ThoughtGenerator />
                </MemoryRouter>
            </QueryClientProvider>
        );
        expect(container).toBeInTheDocument();
    });
});
