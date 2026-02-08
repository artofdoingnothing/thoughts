import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
    it('renders the title', () => {
        render(<App />)
        const titles = screen.getAllByText(/Thought Aggregator/i)
        expect(titles.length).toBeGreaterThan(0)
        expect(titles[0]).toBeInTheDocument()
    })

    it('shows welcome message', () => {
        render(<App />)
        expect(screen.getByText(/Welcome/i)).toBeInTheDocument()
    })
})
