# Architecture & Contribution Rules for HipHopBoomBox Backend

## Code Architecture
This repository follows a strict 5-layer Repository-Service architecture:
- `app/api/v1/`: Thin route handlers. No direct DB access or heavy business logic.
- `app/services/`: Domain business logic and cache management. Wraps repositories.
- `app/repositories/`: Database operations using SQLAlchemy `Session`.
- `app/models/`: SQLAlchemy ORM entity models.
- `app/schemas/`: Pydantic v2 data validation DTOs.
- `app/core/`: Configuration, database client singletons, and dependency injection helpers.

## AI Contribution Rules
1. Every new domain entity must implement files across all 5 layers (`api/v1`, `services`, `repositories`, `models`, `schemas`).
2. Dependency injection must be used throughout: `Depends(get_<entity>_service)` $\rightarrow$ `Service(repo)` $\rightarrow$ `Repository(db)`.
3. Use `uv` for package management. Never edit `uv.lock` or add `requirements.txt`.
4. Keep `graphify-out/` updated locally using `graphify update .` after code edits, but do NOT push `graphify-out/` to Git.
