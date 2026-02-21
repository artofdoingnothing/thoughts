import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import CreateThoughtModal from './CreateThoughtModal';

describe('CreateThoughtModal', () => {
    it('renders without crashing', () => {
        const props = { open: true, onClose: () => {}, onSuccess: () => {}, apiBaseUrl: '' } as any;
        const { container } = render(<CreateThoughtModal {...props} />);
        expect(container).toBeInTheDocument();
    });
});
