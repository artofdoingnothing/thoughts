# PDF Header & Participant Legend

**Status:** COMPLETED

## Context / Current State

The exported PDFs for the Conversation Management domain currently display the title, context, and date in a standard, unstyled layout. The new UI specifications demand a highly polished, dense layout for the header and a new "Participant Legend" to map Personas to colors.

## Action Items

- [x] Implement the first-page Header layout in the newly extracted PDF utility.
  - Title: 18pt bold, color `#1A1A1A`.
  - Context: 9pt regular, `#6B6B6B`, wrapping naturally below the title.
  - Metadata row: 8pt `#9E9E9E`, with Export date left-aligned and Participant count right-aligned, positioned below the context.
  - Separator: Add a 1px rule in `#E0E0E0` below the header (occupying roughly 48px baseline vertical space).
- [x] Implement the Participant Legend directly below the header.
  - Fixed accessible palette for dots: `#4A90D9`, `#E07B3A`, `#6DB87A`, `#A063C6`, `#D95F5F`, `#4ABFBF`.
  - Format: Horizontal flow strip, wrapping if necessary. Contains 8px circular colored dots alongside the Persona's display name in 8pt medium `#444`.

## Additional Notes

- **DDD Reference:** Presentation Layer / Conversation Management (`Conversation` and `Persona` entities).
- Ensure the dot colors assigned in the legend are stored and consistently used for the message blocks later.
