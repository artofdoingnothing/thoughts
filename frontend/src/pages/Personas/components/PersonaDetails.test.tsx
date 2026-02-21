import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import PersonaDetails from './PersonaDetails';

describe('PersonaDetails', () => {
    it('renders without crashing', () => {
        const props = { persona: null, open: false, handleClose: () => {}, handlePersonaUpdated: () => {} } as any;
        const { container } = render(<PersonaDetails {...props} />);
        expect(container).toBeInTheDocument();
    });
});
