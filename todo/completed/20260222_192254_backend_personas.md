# Backend Persona Management Tickets

---

id: STORY-101
title: Delete Persona and Cascading Data
type: feature
priority: high
status: done
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: Persona Management
estimated_effort: S
depends_on: none
blocks: [STORY-102]

---

## User Story

As a user, I want to delete a persona, so that I can remove unwanted identities and their associated data from the system.

## Background and Context

Currently, the system lacks a way to cleanly remove a Persona. Deleting a persona must also clean up the domain entities that depend on it. This operation falls primarily within Persona Management but spans into Conversation Management and Thought Management boundaries through cascading deletions or domain events.

## Acceptance Criteria

1. Given an existing persona when a deletion request is made then the persona is removed from the system.
2. Given a persona is deleted when checking conversations then all messages authored by that persona are deleted.
3. Given a persona is deleted when checking thoughts then all thoughts attributed to that persona are deleted.

## DDD References

- Bounded Context: Persona Management
- Affected domains: Conversation Management (Messages), Thought Management (Thoughts).
- Consider using Domain Events (e.g. `PersonaDeletedEvent`) to trigger cleanup in other bounded contexts, or rely on database cascading if aggregates share the same persistence scope.

## Out of Scope

- Archiving or soft-deleting personas.

## Open Questions

- Should conversations with zero remaining messages be deleted automatically? (Ask Product Manager)

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.

---

id: STORY-102
title: Track Persona Creation Source
type: feature
priority: medium
status: done
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: Persona Management
estimated_effort: S
depends_on: none
blocks: [STORY-107]

---

## User Story

As a user, I want to know how a persona was created, so that I can distinguish between manually created, derived, and movie-character-generated personas.

## Background and Context

The system creates Personas in several ways (manual, derived from another persona, generated from movie datasets). We need to track this provenance at the domain level so the UI can later accurately represent the persona's origin.

## Acceptance Criteria

1. Given a new persona is created manually when inspecting its state then the source indicates it was created by the user.
2. Given a persona is derived from an existing one when inspecting its state then the source indicates it is derived.
3. Given a persona is generated from movie characters when inspecting its state then the source indicates it is movie-generated.

## DDD References

- Bounded Context: Persona Management.
- Consider adding a value object or enum to the Persona aggregate root.

## Out of Scope

- Complex lineage tracking.

## Open Questions

- None.

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.

---

id: STORY-103
title: Scale Up Movie Character Thought Generation
type: feature
priority: medium
status: done
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: AI Processing
estimated_effort: S
depends_on: none
blocks: none

---

## User Story

As a user, I want personas generated from movie characters to have a deeper initial profile, so that their responses and behaviors are more rich and accurate.

## Background and Context

The worker logic responsible for gathering movie dialogues and generating thoughts needs to be scaled up. We must fetch 500 dialogues distributed evenly across the selected characters and generate 50 thoughts from these dialogues.

## Acceptance Criteria

1. Given a persona generation request with N characters, when dialogues are fetched, then exactly 500 dialogues are retrieved globally, distributed equally among the N characters (e.g., 500 / N per character).
2. Given 500 fetched dialogues, when the generation process runs, then exactly 50 thoughts are produced and attributed to the new persona.

## DDD References

- Bounded Context: AI Processing, Persona Management.

## Out of Scope

- Changes to the underlying LLM prompt structure.

## Open Questions

- What if a single selected character has less than (500/N) dialogues available? (Ask Product Manager)

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.

---

id: STORY-104
title: Add Movie Characters to Existing Persona
type: feature
priority: high
status: done
created_by: product-owner-agent
created_at: 2026-02-22T19:22:54Z
assignee: unassigned
bounded_context: Persona Management
estimated_effort: M
depends_on: none
blocks: [STORY-109]

---

## User Story

As a user, I want to enrich an existing movie-generated persona with additional character traits, so that I can continually evolve their personality.

## Background and Context

Users need to be able to append traits from additional movie characters to a persona that has already been generated. This requires an API endpoint to accept an existing persona ID along with a list of new movie character identifiers to trigger further thought generation and profile updates.

## Acceptance Criteria

1. Given an existing movie-generated persona, when a request is made providing new character IDs, then the system initiates the dialogue fetching and thought generation process for these new characters.
2. Given the new thoughts are generated, when the process completes, then the new thoughts are associated with the existing persona and its profile is regenerated.

## DDD References

- Bounded Context: Persona Management, AI Processing.

## Out of Scope

- Removing specific movie characters from a composite persona after they have been added.

## Open Questions

- Should the newly generated 50 thoughts replace the old ones or just be appended? (Assumption: Appended)

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.
