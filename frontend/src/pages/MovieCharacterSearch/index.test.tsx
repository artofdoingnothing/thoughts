import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MovieCharacterSearch from './index';

describe('MovieCharacterSearch Page', () => {
    it('renders without crashing', () => {
        const queryClient = new QueryClient({
            defaultOptions: {
                queries: {
                    retry: false,
                },
            },
        });
        const { container } = render(
            <QueryClientProvider client={queryClient}>
                <MemoryRouter>
                    <MovieCharacterSearch />
                </MemoryRouter>
            </QueryClientProvider>
        );
        expect(container).toBeInTheDocument();
    });
});
