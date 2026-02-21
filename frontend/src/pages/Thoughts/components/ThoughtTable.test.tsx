import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import ThoughtTable from './ThoughtTable';

describe('ThoughtTable', () => {
    it('renders without crashing', () => {
        const props = { thoughts: [], fetchThoughts: () => {} } as any;
        const { container } = render(<ThoughtTable {...props} />);
        expect(container).toBeInTheDocument();
    });
});
