# Domain Event Bus

## Overview

A critical part of our decoupled Domain-Driven Design (DDD) framework is the Domain Event Bus. It allows the core domains to communicate implicitly via an Event-Driven Architecture rather than making tightly coupled function calls between boundaries.

The primary event handlers and routing infrastructure are located in `libs/events/`.

## The Event-Driven Architecture

The Domain Event Bus is a lightweight in-memory system that processes domain-related actions asynchronously.

- **`libs/events/bus.py`**: Contains the core logic for the lightweight internal event pub/sub system. It manages subscriptions and triggers handlers upon publishing an event payload.
- **`libs/events/handlers.py`**: Defines isolated logic blocks that react to specific state changes emitted by domains. This acts as the "glue" that triggers cross-domain mutations (e.g. generating an essay, extracting tags) without the original domain knowing anything about the consumers.

## Decoupling Domain Contexts

Domain entities broadcast semantic events (e.g., `ThoughtCreated`, `ConversationEnded`) through the Event Bus without tying themselves to external dependencies.

**Example**: When a user creates a thought, `ThoughtService` might persist it in its local DB and publish a `ThoughtCreated` event to the bus.

Other parts of the system handle the rest:

- `SentimentAnalyzerHandler` receives `ThoughtCreated` and calculates sentiment.
- `CognitiveDistortionHandler` receives `ThoughtCreated` and analyzes it.
- **Result**: The `ThoughtService` avoids being overly coupled to the `AI Processing` and Worker logic.
