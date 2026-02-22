# Frontend Thoughts Management Tickets

---

id: STORY-110
title: Thought Table Column Visibility Toggle
type: feature
priority: medium
status: done
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: Presentation
estimated_effort: S
depends_on: none
blocks: none

---

## User Story

As a user, I want to hide or show columns on the Thoughts page table, so that I can avoid horizontal scrolling and focus only on the data I care about.

## Background and Context

The current Thoughts data table is too wide, causing horizontal scrolling. The user needs a client-side mechanism to toggle column visibility on or off without triggering network requests or refetching data.

## Acceptance Criteria

1. Given the Thoughts page table, when viewing the page, then a control (e.g., dropdown or popover) exists to select visible columns.
2. Given the column visibility control, when a user deselects a column, then the column immediately disappears from the table without network request.
3. Given the column visibility control, when a user changes selections, then no API refetch is triggered.

## DDD References

- Bounded Context: Presentation (Thought Management views).

## Out of Scope

- Persisting column visibility settings across sessions (user local storage or backend pref) unless trivial.

## Open Questions

- None.

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.
