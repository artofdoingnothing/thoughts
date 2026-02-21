import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import CreateConversationModal from './CreateConversationModal';

describe('CreateConversationModal', () => {
    it('renders without crashing', () => {
        const props = { open: true, onClose: () => {}, onCreate: () => {}, personas: [] } as any;
        const { container } = render(<CreateConversationModal {...props} />);
        expect(container).toBeInTheDocument();
    });
});
