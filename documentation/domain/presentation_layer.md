# API / Presentation Layer

## Overview

The API / Presentation Layer is the outermost layer of the system. It handles external incoming requests, primarily routing HTTP requests into Application layer capabilities. It resides in the `backend/routers/` directory for FastAPI integration.

## Role in the DDD Context

The presentation layer acts purely as an adapter for external callers.

### Responsibilities

- **Request Validation**: Intercepting input and using HTTP layer schemas (Pydantic payload models) to ensure structural correctness.
- **HTTP Routing**: Defining endpoint URLs, verbs, and authentication wrappers.
- **Translation**: It translates HTTP requests and payloads into parameters suitable for the Application layer (Use Cases).
- **Error Handling**: Catching domain or infrastructure exceptions appropriately and converting them into proper fast API HTTP exceptions (e.g., 404 Not Found, 400 Bad Request).

### Best Practices & Enforcement

Under our DDD guidance:

- Routers **MUST NOT** directly manipulate SQLAlchemy data models.
- Routers **MUST NOT** embed business logic directly. Any logic modifying the state of a domain entity must be handed off to the Application Use Cases or underlying Domain Services.
- Routers act as consumers of the Application Layer output (usually obtaining clean DTOs) and relaying it as pure JSON to the frontend.
