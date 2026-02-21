import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'

describe('App', () => {
    it('renders the title', () => {
        const queryClient = new QueryClient()
        render(
            <QueryClientProvider client={queryClient}>
                <App />
            </QueryClientProvider>
        )
        const titles = screen.getAllByText(/Thought Aggregator/i)
        expect(titles.length).toBeGreaterThan(0)
        expect(titles[0]).toBeInTheDocument()
    })

    it('shows welcome message', () => {
        const queryClient = new QueryClient()
        render(
            <QueryClientProvider client={queryClient}>
                <App />
            </QueryClientProvider>
        )
        expect(screen.getByText(/Welcome/i)).toBeInTheDocument()
    })
})
