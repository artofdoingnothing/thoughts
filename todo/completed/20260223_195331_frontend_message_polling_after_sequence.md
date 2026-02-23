---
id: TASK-1001
title: Implement progressive polling for message loading after sequence generation
type: feature
priority: medium
status: done
created_by: task-creator-agent
created_at: 2026-02-23T19:53:31+01:00
assignee: unassigned
bounded_context: Conversation
layer: interface
estimated_effort: S
depends_on: none
blocks: none
---

## Summary

When a user triggers the conversation sequence generator, the application currently invalidates the conversations query. This task replaces that behavior with an intelligent polling mechanism that checks for new messages at an increasing interval, providing immediate feedback without overwhelming the server.

## Background and Context

Currently, the `useGenerateSequence` mutation in `frontend/src/hooks/useConversations.ts` invalidates the `conversations` query upon success. Since sequence generation is an asynchronous backend process, a single invalidation often misses the generated messages. A progressive polling mechanism (e.g., polling after 1s, then 2s, then 4s, up to a max limit or until generation completes) is needed to seamlessly surface new messages to the user.

## Acceptance Criteria

1. When `useGenerateSequence` is successfully called, the frontend must begin polling the conversation details/messages.
2. The polling interval must start small (e.g., 1000ms) and increase over time (e.g., exponentially to 2s, 4s, 8s, etc., up to a max cap).
3. The polling must stop once new messages cease arriving for a sustained period, a timeout is reached, or the conversation status indicates completion.
4. The user interface should visibly indicate (via a loading spinner or typing indicator) while the generation/polling is active.

## DDD Considerations

- This change strictly affects the `interface` layer (React frontend). The underlying domain models and aggregate boundaries for `Conversation` are untouched.
- The polling logic must rely on existing REST API endpoints, keeping the infrastructure isolated from the backend domain.

## Documentation Requirements

- Update inline documentation for any changes to `useConversations` or `useGenerateSequence` hooks.

## Out of Scope

- Modifying the backend to support WebSockets or SSE (this task explicitly relies on HTTP polling).
- Adjusting polling for single message generation; focus strictly on sequence generation.

## Open Questions

- Is there a definitive way for the frontend to know when the backend sequence generation has finished? (If not, we may need to rely on a timeout or message count threshold). -> Assignee to verify endpoint capabilities.

## Definition of Done

- [x] All acceptance criteria are met.
- [x] Tests are added or updated (if applicable to hooks or components).
- [x] Documentation requirements are fulfilled.
- [x] Code review approved by at least one domain expert.
- [x] No broken bounded context contracts.
- [x] Task status updated to `done`.
