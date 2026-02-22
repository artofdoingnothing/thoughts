# Frontend Persona Management Tickets

---

id: STORY-106
title: Delete Persona Action UI
type: feature
priority: high
status: open
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: Presentation
estimated_effort: S
depends_on: [STORY-101]
blocks: none

---

## User Story

As a user, I want to click a button to delete a persona, so that I can remove identities I no longer need.

## Background and Context

A user needs a UI interaction to permanently delete a persona. Because this action cascades and removes messages and thoughts, it requires a confirmation step.

## Acceptance Criteria

1. Given the persona list or detail view, when viewing a persona, then a "Delete" action is visible.
2. Given the user clicks "Delete", when the action is triggered, then a confirmation dialog warns the user about cascading deletion of messages and thoughts.
3. Given the confirmation dialog, when the user confirms, then the persona is deleted and removed from the UI.

## DDD References

- Bounded Context: Presentation overlaying Persona Management.

## Out of Scope

- Bulk deletion of multiple personas.

## Open Questions

- None.

## Definition of Done

- [ ] All acceptance criteria are verified by a stakeholder or QA.
- [ ] The feature behaves consistently across affected platform parts.
- [ ] Relevant documentation or user-facing content is updated.
- [ ] Ticket status updated to `done`.

---

id: STORY-107
title: Display Persona Source Type
type: feature
priority: medium
status: open
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: Presentation
estimated_effort: XS
depends_on: [STORY-102]
blocks: none

---

## User Story

As a user, I want to see the origin of a persona displayed visually, so that I instantly know if it was manually created, derived, or generated from a movie.

## Background and Context

The system tracks the provenance of Personas. The UI needs to visually differentiate these types on the persona listing and detail pages.

## Acceptance Criteria

1. Given a list of personas, when the list is rendered, then each persona displays a badge, icon, or text indicating its source (Created, Derived, Movie-Generated).
2. Given a persona details view, when the page is loaded, then the source type is clearly visible.

## DDD References

- Bounded Context: Presentation.

## Out of Scope

- Filtering or sorting personas by source type.

## Open Questions

- None.

## Definition of Done

- [ ] All acceptance criteria are verified by a stakeholder or QA.
- [ ] The feature behaves consistently across affected platform parts.
- [ ] Relevant documentation or user-facing content is updated.
- [ ] Ticket status updated to `done`.

---

id: STORY-109
title: Modal to Add Characters to Generated Persona
type: feature
priority: high
status: open
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: Presentation
estimated_effort: M
depends_on: [STORY-104, STORY-108]
blocks: none

---

## User Story

As a user, I want to modify a movie-generated persona by adding more characters via a search modal, so that I can easily expand their personality traits.

## Background and Context

Users need the ability to edit an existing movie-generated persona. The interaction model should be a modal window where they can search for new characters by name (using wildcard search) and append them to the current persona.

## Acceptance Criteria

1. Given a movie-generated persona's detail view, when the user initiates an edit, then an "Add Characters" button is available.
2. Given the user clicks "Add Characters", when the action fires, then a modal opens containing a character search interface.
3. Given the search interface, when the user finds and selects characters, then they can submit the additions.
4. Given a successful submission, when the modal closes, then the UI properly indicates that the persona is being updated/regenerated.

## DDD References

- Bounded Context: Presentation.

## Out of Scope

- Removing existing characters through this specific modal constraint.

## Open Questions

- None.

## Definition of Done

- [ ] All acceptance criteria are verified by a stakeholder or QA.
- [ ] The feature behaves consistently across affected platform parts.
- [ ] Relevant documentation or user-facing content is updated.
- [ ] Ticket status updated to `done`.
