import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import ThoughtGenerator from './index';

describe('ThoughtGenerator Page', () => {
    it('renders without crashing', () => {
        const { container } = render(
            <MemoryRouter>
                <ThoughtGenerator />
            </MemoryRouter>
        );
        expect(container).toBeInTheDocument();
    });
});
