# Data Transfer Objects (DTOs)

## Overview

Data Transfer Objects (DTOs) provide a secure, type-checked contract for transferring data between different layers of our Domain-Driven Design (DDD) architecture. They are primarily defined in `libs/db_service/dto.py`.

## Boundries Between Pydantic DTO Models and SQLAlchemy

In our architecture, the boundaries are clear between persistence models and the models explicitly returned to layers outside of the core domain:

### SQLAlchemy Domain Entities

- Usually found linked directly with `libs/db_service/`.
- Repurposed **purely for the persistence layer**.
- Tightly entangled with DB sessions, lazy relationship loading, and schema migrations.

### Pydantic DTOs

- Live primarily in `libs/db_service/dto.py`.
- **Stateless** representations of data with zero persistent behavior and complete independence from SQLAlchemy.
- Used actively by Use Cases to translate the results obtained from Domain Services, which eventually propagate upwards to the `Presentation Layer`.

## Why Separate The Two?

- **Security Check**: Passing pure Dicts or raw DB entities to the API layer often results in leaking sensitive private fields or exposing DB architecture (for example, relational backrefs). DTOs map exactly what should be safely exposed.
- **Session Safety**: ORM elements passed directly out of the application services layer risk "DetachedInstanceError" bugs within async FastAPIs. DTOs serialize data gracefully before any DB session commits or closes.
- **Interface Stability**: Changing the database schema underlying standard Entities won't implicitly break client applications; standardizing around robust DTOs gives room to map fields interchangeably.
