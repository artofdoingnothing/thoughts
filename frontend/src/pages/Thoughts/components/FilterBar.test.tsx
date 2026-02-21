import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import FilterBar from './FilterBar';

describe('FilterBar', () => {
    it('renders without crashing', () => {
        const props = { filterTag: '', filterEmotion: '', filterPersonaId: '', setFilterTag: () => {}, setFilterEmotion: () => {}, setFilterPersonaId: () => {}, fetchThoughts: () => {} } as any;
        const { container } = render(<FilterBar {...props} />);
        expect(container).toBeInTheDocument();
    });
});
