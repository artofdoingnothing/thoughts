import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import ConversationGenerator from './index';

describe('ConversationGenerator Page', () => {
    it('renders without crashing', () => {
        const { container } = render(
            <MemoryRouter>
                <ConversationGenerator />
            </MemoryRouter>
        );
        expect(container).toBeInTheDocument();
    });
});
