import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import Personas from './index';

describe('Personas Page', () => {
    it('renders without crashing', () => {
        const { container } = render(
            <MemoryRouter>
                <Personas />
            </MemoryRouter>
        );
        expect(container).toBeInTheDocument();
    });
});
