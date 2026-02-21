# Missing Backend Test Cases

The following files have lower test coverage and need baseline test cases. Edge cases are not required.

## Backend Routers

- `backend/routers/conversation_routes.py`
- `backend/routers/persona_routes.py`
- `backend/routers/processor_routes.py`
- `backend/routers/thought_routes.py`

## DB Service

- `libs/db_service/conversation_service.py`
- `libs/db_service/persona_service.py`
- `libs/db_service/service.py`

## Event Bus and Handlers

- `libs/events/bus.py`
- `libs/events/handlers.py`

## LLM Service

- `libs/llm_service/base.py`
- `libs/llm_service/gemini.py`

## Processor Service

- `libs/processor_service/service.py`

## Use Cases

- `libs/use_cases/conversation_use_cases.py`
- `libs/use_cases/generation_use_cases.py`
- `libs/use_cases/thought_use_cases.py`

## Workers

- `workers/tasks.py`
- `workers/worker.py`
