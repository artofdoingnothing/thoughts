# AI Processing & Infrastructure Domain

## Overview

The AI Processing domain acts as a shared supporting context for the rest of the application. It is responsible for interfacing with external Large Language Models (LLMs), executing complex asynchronous data transformations (via background workers), and running prompt-based analytical logic.

## Core Components

### `llm_service`

A low-level infrastructure adapter that abstracts communication with external LLM APIs.

- **`BaseLLM`**: Interface for LLM operations.
- **`GeminiLLM`**: Concrete implementation interacting with the Google Gemini API.
- **`LLMFactory`**: Manages instantiation of the configured LLM provider.

### `processor_service`

A higher-level domain service that encapsules specific prompt templates and parsing logic. It translates abstract AI tasks into concrete LLM calls.

- **Key Responsibilities**:
  - Analyzing thoughts (Sentiment, Cognitive Distortions, Action Orientation, Thought Type, Topics).
  - Generating new thoughts from external content (e.g., parsing blogs).
  - Assisting Persona Management (e.g., extracting emotions from a profile).
  - Participating in Conversational flows (generating dialogue messages).
  - Drafting and modifying essays.

### Background Workers (`workers/tasks.py`)

Infrastructure-level mechanism (Redis Queue) to perform AI Processing tasks asynchronously without blocking the main application thread.

- **Tasks**:
  - `analyze_cognitive_distortions`
  - `analyze_sentiment`
  - `parse_blog_and_generate_thoughts`
  - `generate_essay`
  - `generate_conversation_message`
- _Note_: These tasks typically invoke the `ProcessorService` and then update the main database via `ThoughtService`.

## Domain Boundaries

- **Interacts with**: All other domains (Thought, Persona, Conversation). It acts as an upstream service providing reasoning and generation capabilities.
- **Architectural characteristic**: Mostly stateless infrastructure and application services. It does not own persistent domain entities of its own but rather operates on DTOs and outputs data to be persisted by other domains.

## Architectural Anomalies (DDD Violations)

- `workers/tasks.py` directly references and uses `ThoughtService` from `libs.db_service`. In a strict DDD architecture, background workers should ideally publish domain events or interact via dedicated Use Case handlers rather than calling another domain's database service directly.
