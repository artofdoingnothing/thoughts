# PDF Inline Elements & Footer

**Status:** COMPLETED

## Context / Current State

The exported PDFs currently lack page numbers, proper footers, and rich inline text rendering for elements like code blocks or system timestamps. The final aspect of the Conversation PDF UI specs involves adding these complex inline rendering rules and a consistent page footer.

## Action Items

- [x] Implement cross-day jump timestamps.
  - If a message occurs on a different day than the previous one, render a centered divider with a 0.5pt rule on each side and a date label in 7.5pt `#AAAAAA` (e.g., `— Monday, Feb 19 —`).
- [x] Add support for quoted/reply references within `Message` bodies.
  - Rendered with a 1.5pt left border in the sender's assigned color.
  - Indented block, 7.5pt italic `#7A7A7A` text, 4px top/bottom padding.
- [x] Add support for inline markdown/code elements in `Message` bodies.
  - Code spans: monospace 8pt, color `#C0392B` on `#F7F7F7` background with 1px `#E8E8E8` border, 2px horizontal padding.
  - Code blocks: monospace 7.5pt, color `#2C2C2C` on `#F4F4F4`, full-width with 6px padding, 1pt `#DEDEDE` border.
- [x] Implement the Page Footer on all pages.
  - Typography: 8pt `#BDBDBD`.
  - Left-aligned: Conversation title truncated to 40 chars.
  - Right-aligned: `Page X of Y`.
  - Separated from the page content by a 0.5pt `#E8E8E8` rule.

## Additional Notes

- **DDD Reference:** Presentation Layer / Conversation Management.
- You might need to parse simple markdown or regex match for quotes/code blocks before rendering the text via `jsPDF`.
- Ensure multi-page generation accurately tracks "Page X of Y", which might require generating the content to calculate total pages before writing the footers.
