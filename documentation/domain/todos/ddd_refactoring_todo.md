# Domain-Driven Design (DDD) Refactoring TODO

The current codebase (specifically `libs/db_service/service.py` and `backend/main.py`) acts predominantly as a monolithic CRUD system with mixed domain logic. To align closer with true DDD principles, the following refactoring steps should be addressed:

## 1. Decompose `ThoughtService` into Domain-Specific Services / Repositories

- **Current State**: `libs/db_service/service.py` contains the `ThoughtService` class which handles _everything_: Persona creation, Thought creation, Emotion mapping, Conversation messaging, and Event resolution (ending a conversation). This is a God Class.
- **Action**:
- [x] Create a dedicated `PersonaRepository` and `PersonaService` for managing Identity and Profile Generation.
  - [x] Create a dedicated `ConversationRepository` and `ConversationService` for orchestrating multi-agent interactions.
  - [x] Narrow down `ThoughtService` to just handle atomic thoughts and tags/emotions.

## 2. Introduce Proper Domain Events (Optional but Recommended)

- **Current State**: When a `Conversation` ends, the `ThoughtService` directly runs a loop to convert `Messages` to `Thoughts`.
- **Action**:
  - [x] Implement a Domain Event bus. When `ConversationEndedEvent` is fired from the `Conversation` domain, a handler in the `Thought` domain should listen to it and create the corresponding Thoughts asynchronously.

## 3. Decouple Background Workers from Database Layer

- **Current State**: `workers/tasks.py` imports `ThoughtService` directly to persist the results of the LLM responses.
- **Action**:
  - [x] Workers should either hit internal APIs (Application layer) or invoke application Use Cases, passing DTOs rather than relying on direct Database Service imports from another module.

## 4. Decompose `backend/main.py` Router

- **Current State**: All API routes sit in a single `main.py` file.
- **Action**:
  - [x] Break down the FastAPI app into distinct routers (e.g., `routers/thought_routes.py`, `routers/persona_routes.py`, `routers/conversation_routes.py`) reflecting the boundaries of the Bounded Contexts defined in the domain documentation.
