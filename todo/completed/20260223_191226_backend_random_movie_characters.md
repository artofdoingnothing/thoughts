---
id: STORY-1
title: Fetch random movie characters seeded by timestamp
type: feature
priority: medium
status: open
created_by: product-owner-agent
created_at: 2026-02-23T19:12:26+01:00
assignee: unassigned
bounded_context: Dataset Management
estimated_effort: S
depends_on: none
blocks: [STORY-2]
---

## User Story

As a user, I want to fetch a random set of 50 movie characters, so that I can discover interesting character combinations without having to search manually.

## Background and Context

The Persona generation workflow requires movie characters to serve as a base. Currently, characters can be searched, but we need an endpoint to return exactly 50 randomly selected movie characters to enhance discoverability. The randomness must be seeded by a timestamp provided by the client, ensuring predictable randomness and consistent behavior across a session when re-rendering or retrying.

## Acceptance Criteria

1. Given a client requests random characters with a timestamp seed, when the backend processes the request, then it returns exactly 50 randomly selected movie characters derived from the given seed.
2. Given a client requests random characters without a seed, when the backend processes the request, then it defaults to using the server's current timestamp as the seed.
3. Given the same timestamp seed is provided in multiple requests, when the backend processes the requests, then it returns the exact same list of 50 characters.

## DDD References

Bounded context: Dataset Management
Concepts: Movie Character Dataset

## Out of Scope

- Frontend UI changes for searching and displaying characters.
- Complex state management in the UI.

## Open Questions

- Should the maximum number of characters be fixed at 50 or configurable per request up to a limit? (Assume fixed at 50 for now).

## Definition of Done

- [x] All acceptance criteria are verified by a stakeholder or QA.
- [x] The feature behaves consistently across affected platform parts.
- [x] Relevant documentation or user-facing content is updated.
- [x] Ticket status updated to `done`.
