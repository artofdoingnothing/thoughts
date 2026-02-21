import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ConversationList from './ConversationList';

describe('ConversationList', () => {
    it('renders without crashing', () => {
        const props = { conversations: [], selectedId: null, onSelect: () => {}, onCreateNew: () => {} } as any;
        const { container } = render(<ConversationList {...props} />);
        expect(container).toBeInTheDocument();
    });
});
