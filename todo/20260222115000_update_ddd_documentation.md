# Update and Expand Domain-Driven Design (DDD) Documentation

**Status:** COMPLETED

## Context / Current State

Recent changes refactored the backend architecture to better align with DDD principles. This included decoupling the `ThoughtService` monolith into separate domain services (`ConversationService`, `PersonaService`, `ThoughtService`), introducing Application Use Cases (`libs/use_cases/`), and creating a Domain Event Bus (`libs/events/`). However, the documentation in `documentation/domain/` has not been fully updated to reflect these advances, and new architectural layers remain undocumented.

## Action Items

### Document New DDD Layers

These layers are active but completely miss documentation on their role in the current DDD structure.

- [x] **Application Layer (Use Cases)**
  - Document the `libs/use_cases/` directory.
  - Explain how Application Services orchestrate domain services and infrastructure logic via Data Transfer Objects (DTOs).
- [x] **Domain Event Bus**
  - Document `libs/events/bus.py` and `libs/events/handlers.py`.
  - Explain the event-driven architecture and how domain events help to decouple domain contexts.
- [x] **API / Presentation Layer**
  - Document `backend/routers/`.
  - Define its role in the DDD context (e.g., interface layer, translating HTTP input to Application layer requests).
- [x] **Data Transfer Objects (DTOs)**
  - Document the usage of `libs/db_service/dto.py`.
  - Explain the boundaries between Pydantic DTO models and SQLAlchemy domain entities.

### Update Existing Domain Docs (Remove Outdated "Architectural Anomalies")

The existing domain documentation still states historical DDD violations that have been successfully refactored.

- [x] **Update `documentation/domain/ai_processing.md`**
  - Remove the claim that `workers/tasks.py` directly references `ThoughtService`. It now interacts correctly via Use Cases (e.g., `ThoughtUseCases`).
- [x] **Update `documentation/domain/conversation_management.md`**
  - Remove the anomaly note about Conversation handling being tangled within `ThoughtService`, as we now have a dedicated module for this.
- [x] **Update `documentation/domain/persona_management.md`**
  - Remove the note regarding Persona logic running within `ThoughtService`. This was successfully extracted.
- [x] **Update `documentation/domain/thought_management.md`**
  - Correct the anomaly section to clarify that we now have dedicated logic without the monolithic setup.

## Additional Notes

### Goal

Update the existing DDD documentation to reflect recent architectural refactoring and expand the documentation to cover missing layers of the application's domain-driven design structure.

### Guidelines

- Update existing files in `documentation/domain/` directly.
- Add new markdown files in `documentation/domain/` for missing layers (e.g. `use_cases.md`, `events.md`, `presentation_layer.md`).
- Ensure that the documentation style is simple and easy to follow.
