import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import PersonaList from './PersonaList';

describe('PersonaList', () => {
    it('renders without crashing', () => {
        const props = { personas: [], handleOpenPersona: () => {}, setDerivingPersonaId: () => {}, fetchPersonas: () => {} } as any;
        const { container } = render(<PersonaList {...props} />);
        expect(container).toBeInTheDocument();
    });
});
