import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Thoughts from './index';

describe('Thoughts Page', () => {
    it('renders without crashing', () => {
        const { container } = render(
            <MemoryRouter>
                <Thoughts refreshKey={0} />
            </MemoryRouter>
        );
        expect(container).toBeInTheDocument();
    });
});
