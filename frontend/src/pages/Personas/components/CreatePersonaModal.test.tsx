import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import CreatePersonaModal from './CreatePersonaModal';

describe('CreatePersonaModal', () => {
    it('renders without crashing', () => {
        const props = { open: true, handleClose: () => {}, handlePersonaCreated: () => {} } as any;
        const { container } = render(<CreatePersonaModal {...props} />);
        expect(container).toBeInTheDocument();
    });
});
