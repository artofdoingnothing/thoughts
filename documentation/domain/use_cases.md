# Application Layer (Use Cases)

## Overview

The Application Layer in our Domain-Driven Design (DDD) architecture orchestrates the execution of business workflows. It is represented by the `libs/use_cases/` directory, serving as the bridge between the API/Presentation layer and the core Domain services.

## Core Responsibilities

- **Orchestration**: Directing the flow of data by invoking the necessary domain services, infrastructure capabilities (like the Event Bus or Background Workers), and external adapters.
- **Transaction Boundaries**: While lower-level services handle pure logic, the application layer often defines the boundaries for a single business transaction.
- **Data Translation**: It takes in raw inputs (or HTTP request dependencies) and translates them into domain concepts, often returning Data Transfer Objects (DTOs) instead of raw database entities to the upper layers.

## Use Cases Hierarchy

In the `libs/use_cases/` directory, application logic is grouped by domain feature:

- `thought_use_cases.py`: Orchestrates logic for creating, linking, and retrieving thoughts.
- `conversation_use_cases.py`: Orchestrates the flow of creating conversations, appending messages, and wrapping up conversations into thoughts.
- `generation_use_cases.py`: Handles complex workflows that require asynchronous background processing (e.g., generating traits, analyzing cognitive distortions).

## Interaction with DTOs and Domain Services

The Application Use Cases act as the primary consumers of both Domain Services (e.g., `ThoughtService`, `PersonaService`) and DTOs.

Instead of passing SQLAlchemy models up to the API layer, Use Cases transform the entities retrieved from Domain Services into pristine Pydantic DTOs (e.g., `ThoughtDTO`, `ConversationDTO`). This protects the API layer from being tightly coupled to the underlying database schema and enforces the integrity of the data being exposed.
