import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import AddPersonaModal from './AddPersonaModal';

describe('AddPersonaModal', () => {
    it('renders without crashing', () => {
        const props = { open: true, onClose: () => {}, onAdd: () => {}, personas: [], currentPersonaIds: [] } as any;
        const { container } = render(<AddPersonaModal {...props} />);
        expect(container).toBeInTheDocument();
    });
});
