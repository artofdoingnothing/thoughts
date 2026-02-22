# Thought Management Domain

## Overview

The Thought Management domain acts as the central hub for the application's core data: **Thoughts**. It handles the creation, organization, linking, and retrieval of thoughts, both human-generated and AI-generated.

## Core Entities & Value Objects

### Thought (Aggregate Root)

The primary entity of this domain. Represents a single atomic idea, statement, or observation.

- **Attributes**:
  - `id`: Unique identifier
  - `content`: The text content of the thought
  - `status`: Lifecycle state (e.g., "pending", "processed")
  - `is_generated`: Boolean indicating if an AI generated this thought
  - `action_orientation`: Optional actionability context
  - `thought_type`: Optional categorization of the thought
  - `created_at` / `updated_at`: Timestamps
  - `persona_id`: Optional link to the Persona domain if a specific persona generated this thought

### ThoughtLink

Represents a directed relationship between two thoughts.

- **Attributes**:
  - `source_id`: Origin thought
  - `target_id`: Destination thought
- **Concept**: Enables building a web or graph of related thoughts.

### Categorization Entities

These are standalone entities that can be linked to many thoughts, effectively acting as metadata tagging.

- **Tag**: Simple keyword labeling.
- **Emotion**: Captures the emotional sentiment or state associated with a thought.
- **Topic**: Higher-level thematic categorization.
- _Note: Each of these relates to `Thought` via many-to-many join tables (`thought_tag`, `thought_emotion`, `thought_topic`)._

## Key Services and Operations

- **Creation**: Thoughts can be created manually or automatically generated based on external sources (UI/API layer coordinates with the AI Processing domain for the latter).
- **Linking**: Establishing `ThoughtLink` relationships to build connected structures.
- **Retrieval Engine**: Filtering thoughts by `persona_id`, `tag`, `emotion`, etc., to serve the frontend view or provide context for the Conversation domain.

## Domain Boundaries

- **Interacts heavily with**: Persona Management (Thoughts belong to personas).
- **Consumes from**: AI Processing domain (which analyzes and generates Thoughts).
- **Serves**: Conversation Management (Thoughts form the context and memory from which personas converse).

## Architecture Status

Logic for Thought handling has been successfully decoupled from the previous monolithic setup. It is now handled by dedicated services (e.g., `ThoughtService`, `ThoughtUseCases`) ensuring a proper separation of concerns within the Thought Management domain.
