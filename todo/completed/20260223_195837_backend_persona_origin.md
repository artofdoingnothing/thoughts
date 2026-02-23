---
id: STORY-2001
title: Store movie character origin details for personas
type: feature
priority: medium
status: done
created_by: product-owner-agent
created_at: 2026-02-23T19:58:37+01:00
assignee: unassigned
bounded_context: Persona
estimated_effort: S
depends_on: none
blocks: [STORY-2002]
---

## User Story

As a user, I want the system to remember the specific movie context a persona was created from, so that I can reference this origin information later when exporting conversations or viewing persona details.

## Background and Context

When personas are generated from the movie dataset, we lose the specific context (movie name, year, rating) once the persona is saved. We need to store this origin information (e.g., 'character from movie(year)(rating)') explicitly within the Persona aggregate so it can be surfaced in the UI and exports.

## Acceptance Criteria

1. Given a persona is being created from a movie character, when the persona is saved, then the origin string in the format "{character} from {movie}({year})({rating})" must be stored securely with the persona.
2. Given a saved persona with a movie origin, when its details are fetched, then this origin string must be returned in the response payload.

## DDD References

- Bounded Context: Persona
- Domain Concepts: `Persona` aggregate requires a new attribute to hold the 'origin string' or 'source description' metadata.

## Out of Scope

- Displaying this information on the UI (handled by frontend tickets).

## Open Questions

- Should this string be stored in an existing profile/background field, or a dedicated `origin_description` field? -> Backend engineer to decide based on current schema.

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.
