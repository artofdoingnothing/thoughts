# Conversation Management Domain

## Overview

The Conversation Management domain governs interactions between multiple Personas. It acts as an orchestrator, allowing agents (Personas) to deliberate, generate contextually relevant messages, and eventually summarize their interaction into long-term memory (Thoughts).

## Core Entities & Value Objects

### Conversation (Aggregate Root)

Represents an ongoing interaction session.

- **Attributes**:
  - `id`: Unique identifier
  - `title`: A human-readable title summarizing the conversation
  - `context`: High-level prompt or contextual guidelines for the interaction
  - `created_at`: Timestamp
- **Relationships**:
  - `personas`: Many-to-Many association with participating `Persona` entities.
  - `messages`: One-to-Many mapping to the individual `Message` entities generated within the conversation.

### Message

An individual utterance or statement made by a Persona within a Conversation.

- **Attributes**:
  - `id`: Unique identifier
  - `content`: The text content of the message
  - `is_generated`: Boolean flag to indicate whether the AI generated this message or it was manually injected.
  - `created_at`: Timestamp
- **Relationships**:
  - `conversation_id`: The conversation to which it belongs.
  - `persona_id`: The specific persona that authored the message.

## Key Services and Operations

- **Conversation Setup**: Creating a new conversation session and mapping the participating Personas. Personas can be added to an existing conversation dynamically.
- **Message Generation**: The domain relies on the AI Processing domain (and the recent message history / overall context) to auto-generate the next logical message from a specific Persona.
- **Ending Conversations (Thought Consolidation)**: When a conversation is marked as "ended," all the individual `Message` entities inside it are processed. They are converted into standalone `Thought` entities linked back to the respective Personas, becoming part of their long-term knowledge base.

## Domain Boundaries

- **Interacts heavily with**: Persona Management (Personas are participants).
- **Consumes from**: AI Processing domain (to generate contextual messages based on LLM inference).
- **Serves**: Thought Management (Outputs final messages as Thoughts for long-term storage).

## Message Generation Behavior

### Multi-Message Sequences

When generating a message for a persona, the AI may produce **1 to 3 related messages** in a single turn, simulating natural social texting behavior (e.g., splitting a thought, adding a reaction, or appending an afterthought). Each message is stored as a separate `Message` entity, ordered by `created_at`.

### Age-Based Communication Style

The persona's `age` directly influences message structure:

| Age Group            | Messages     | Style                                                     |
| -------------------- | ------------ | --------------------------------------------------------- |
| Teens (13-19)        | 2-3          | Short, fragmented texts with slang, abbreviations, emojis |
| Young Adults (20-35) | 1-3          | Casual but more complete sentences, occasional slang      |
| Middle-Aged (36-55)  | 1-2          | Composed, full sentences with moderate vocabulary         |
| Older Adults (56+)   | 1 (rarely 2) | Proper grammar, warm/considered tone, full sentences      |

## Architectural Anomalies (DDD Violations)

- Currently, logic for Conversation handling (including the final consolidation of Messages into Thoughts) is tangled within `libs/db_service/service.py` (`ThoughtService`) rather than an independent `ConversationService` or `ConversationRepository`.
