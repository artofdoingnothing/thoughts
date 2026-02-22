# PDF Generator Architecture & Setup

**Status:** COMPLETED

## Context / Current State

Currently, the PDF generation for the Conversation Management domain is handled by a monolithic `handleDownloadPdf` function inside `frontend/src/pages/ConversationGenerator/index.tsx`. It uses basic `jsPDF` commands that do not align with the new, highly specific UI specifications for the Conversation PDF.

As a Product Owner, I need the PDF generation logic decoupled from the UI component to improve maintainability and strictly conform to the new design standards.

## Action Items

- [x] Extract the PDF generation logic from `ConversationGenerator/index.tsx` into a dedicated service/utility (e.g., `frontend/src/utils/pdfGenerator.ts`).
- [x] Configure the PDF document for A4 size (210 × 297mm).
- [x] Set page margins specifically to 16mm for top/bottom and 14mm for left/right.
- [x] Ensure the font family used by `jsPDF` is set to "Inter" or a system sans-serif fallback (Helvetica Neue, Arial). You may need to load a custom font file or use standard fallbacks.
- [x] Update the UI button in the Presentation Layer to use this new utility and pass the required domain entities (`Conversation` aggregate, `Message` entities, and `Persona` entities).

## Additional Notes

- **DDD Reference:** Presentation Layer / Conversation Management.
- This is the foundational PR. Do not implement all the UI layout details yet; just ensure the new service can generate a blank PDF with the correct sizing/fonts and is properly wired up to the frontend button.
