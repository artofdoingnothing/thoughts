# PDF Message Layout

**Status:** COMPLETED

## Context / Current State

Currently, `Message` entities belonging to the `Conversation` aggregate are rendered in the PDF sequentially without logical grouping or advanced typesetting. The new UI specifications require distinct visual spacing, strict typography rules, and grouping of consecutive messages from the same sender within a 5-minute window.

## Action Items

- [x] Implement the message spacing:
  - 4px vertical gap between consecutive messages from different senders.
  - 2px vertical gap between consecutive messages from the same sender.
- [x] Develop the single message block layout:
  - Sender dot: 7px circle in the `Persona`'s accessible assigned color (from the legend), vertically centered to the first line of the sender name.
  - Sender name: 8pt semibold, `#2C2C2C`, left-aligned.
  - Timestamp: 7.5pt `#AAAAAA`, positioned to the right on the same line as the sender name.
  - Message body: 9pt regular, `#3A3A3A`, line-height 1.4, left-indented 14px to align under the sender name.
- [x] Implement consecutive message grouping logic:
  - If a message is from the same sender AND within 5 minutes of the previous message, omit the sender name and dot row.
  - Just continue the body text with a 2px gap.
  - If more than 5 minutes have passed but it's the same sender, only show a small timestamp on the right margin instead of repeating the sender name.
- [x] Ensure natural line wrapping across multiple lines without background bubbles (flat text layout).

## Additional Notes

- **DDD Reference:** Presentation Layer / Conversation Management (processing `Message` and `Persona` entities).
- Calculate horizontal constraints accurately to wrap the 9pt text properly before checking for page breaks.
