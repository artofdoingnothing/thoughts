import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import EssayGenerator from './index';

describe('EssayGenerator Page', () => {
    it('renders without crashing', () => {
        const { container } = render(
            <MemoryRouter>
                <EssayGenerator />
            </MemoryRouter>
        );
        expect(container).toBeInTheDocument();
    });
});
