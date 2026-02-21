import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import DerivePersonaModal from './DerivePersonaModal';

describe('DerivePersonaModal', () => {
    it('renders without crashing', () => {
        const props = { open: true, onClose: () => {}, onSuccess: () => {}, sourcePersonaId: null, isGenMode: false } as any;
        const { container } = render(<DerivePersonaModal {...props} />);
        expect(container).toBeInTheDocument();
    });
});
