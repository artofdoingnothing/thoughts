---
id: STORY-2002
title: Include persona origin and summary in conversation PDFs
type: feature
priority: medium
status: done
created_by: product-owner-agent
created_at: 2026-02-23T19:58:37+01:00
assignee: unassigned
bounded_context: Conversation/PDF
estimated_effort: S
depends_on: [backend-persona-origin]
blocks: []
---

## User Story

As a user, I want the conversation PDF to include short persona summaries and origin details, so that I can easily identify their backgrounds when reading printed or exported conversations.

## Background and Context

The current PDF export is clean but lacks context about who the personas are beyond their names. We now have `profile.thought_patterns` (summary) and `origin_description` (movie details) available in the backend. These should be surfaced in the PDF.

## Acceptance Criteria

1. Given a conversation is being exported to PDF, when the document is generated, then a short summary of each participant (from `profile.thought_patterns`) must be included.
2. Given a persona in the conversation is from the movie dataset, when the PDF is generated, then the origin string (e.g., 'Character from Movie(Year)(Rating)') must be displayed alongside their summary.

## DDD References

- Bounded Context: Conversation
- Domain Concepts: `PDF Export` (User Interface service)

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.

---

id: STORY-2003
title: Display movie genres in the character search list
type: feature
priority: low
status: done
created_by: product-owner-agent
created_at: 2026-02-23T19:58:37+01:00
assignee: unassigned
bounded_context: Persona-Generation
estimated_effort: XS
depends_on: []

---

## User Story

As a user, I want to see the movie genres in the character search results table, so that I can better filter and select characters based on their cinematic archetypes.

## Acceptance Criteria

1. Given a character search is performed, when results are displayed in the table, then an additional column for "Genres" must be visible.
2. Given a character belongs to multiple genres, when displayed, then all genres should be listed (comma-separated).

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.

---

id: STORY-2004
title: Load all characters from a movie when name is clicked
type: feature
priority: medium
status: done
created_by: product-owner-agent
created_at: 2026-02-23T19:58:37+01:00
assignee: unassigned
bounded_context: Persona-Generation
estimated_effort: S
depends_on: []

---

## User Story

As a user, I want to easily explore all characters from a specific movie by clicking its name, so that I can quickly build a persona out of multiple characters from the same story.

## Acceptance Criteria

1. Given a movie name is visible in the search results, when I click it, then the search results should refresh to show all characters from that movie.
2. Given the movie-specific list is loaded, when I select characters, then they should be added to the selection list without clearing previous selections from other movies.

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.
