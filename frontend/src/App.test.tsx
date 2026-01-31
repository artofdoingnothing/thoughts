import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import App from './App'

describe('App', () => {
    it('renders the title', () => {
        render(<App />)
        expect(screen.getByText(/Thought Aggregator/i)).toBeInTheDocument()
    })

    it('shows empty state message', () => {
        render(<App />)
        expect(screen.getByText(/No thoughts found/i)).toBeInTheDocument()
    })
})
