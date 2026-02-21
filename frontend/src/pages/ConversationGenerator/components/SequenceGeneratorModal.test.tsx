import { render } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import SequenceGeneratorModal from './SequenceGeneratorModal';

describe('SequenceGeneratorModal', () => {
    it('renders without crashing', () => {
        const props = { open: true, onClose: () => {}, onGenerate: () => {}, personas: [] } as any;
        const { container } = render(<SequenceGeneratorModal {...props} />);
        expect(container).toBeInTheDocument();
    });
});
