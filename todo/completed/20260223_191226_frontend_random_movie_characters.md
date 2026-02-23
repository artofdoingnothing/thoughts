---
id: STORY-2
title: Random character selection and vertically expanding list
type: feature
priority: medium
status: open
created_by: product-owner-agent
created_at: 2026-02-23T19:12:26+01:00
assignee: unassigned
bounded_context: Persona Management
estimated_effort: S
depends_on: [STORY-1]
blocks: none
---

## User Story

As a user, I want to fetch 50 random movie characters, view them in a table, and add them to a vertically expanding selected list, so that I can easily browse and collect interesting characters for persona generation.

## Background and Context

The persona generation workflow relies on users selecting movie characters. To make this process smoother and more explorative, users need a way to generate a random list of characters (seeded by the current timestamp) and manually add them to their selection list. The selected list should not have a fixed scrolling height or horizontal expansion limitation, but rather naturally expand downwards as more characters are added.

## Acceptance Criteria

1. Given the user is on the movie character selection page, when they trigger the "Fetch Random Characters" action, then the frontend requests 50 random characters from the backend using the current timestamp as the seed.
2. Given the fetched characters are loading or loaded, when displayed, then they appear in a table format with a "plus" icon next to each character.
3. Given the user clicks the "plus" icon on a character in the table, when it is processed, then the character is added to the "selected characters" list.
4. Given the selected characters list has multiple items, when it is rendered, then it visually expands vertically based strictly on the number of selected characters, avoiding horizontal scroll or fixed overflow containers.

## DDD References

Bounded context: Persona Management
Concepts: Movie Character selection UI, Persona Generation UI.

## Out of Scope

- Changes to the backend random character endpoint logic.
- Changes to how thoughts or dialogues are generated from characters.

## Open Questions

None.

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.
