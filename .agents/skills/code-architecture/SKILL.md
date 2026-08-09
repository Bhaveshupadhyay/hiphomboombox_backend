---
name: code-architecture
description: Guide for understanding the HipHopBoomBox backend architecture, repository-service pattern, layer responsibilities, Graphify integration, and contribution guidelines for AI agents and developers.
---

# Code Architecture & Contribution Guidelines

This skill provides comprehensive instructions for understanding, navigating, and contributing to the **HipHopBoomBox Backend** codebase.

---

## 1. Project Overview & Tech Stack

- **Framework**: FastAPI (Python ≥ 3.14)
- **Package Manager**: `uv` (using `pyproject.toml` and `uv.lock`)
- **Database & ORM**: PostgreSQL via SQLAlchemy 2.0 (`sessionmaker` sync sessions)
- **Caching**: Upstash Redis (`upstash-redis`)
- **Data Validation & Settings**: Pydantic v2 & `pydantic-settings`
- **Knowledge Graph**: Graphify (`graphify-out/` for fast code traversal)

---

## 2. Layered Architecture Pattern

The project strictly follows a 5-layer Clean / Repository-Service architecture pattern:

```
app/
├── api/v1/          # 1. API Route Handlers (Controllers)
├── services/        # 2. Service Layer (Business Logic & Transactions)
├── repositories/    # 3. Repository Layer (Raw DB Queries & Persistence)
├── models/          # 4. ORM Layer (SQLAlchemy Models)
├── schemas/         # 5. Schema Layer (Pydantic DTOs & Validation)
└── core/            # Infrastructure (Config, DB Engine, Redis, DI)
```

### Layer Responsibilities & Rules:

1. **`app/api/v1/` (Route Handlers)**
   - Responsible only for HTTP request parsing, status codes, dependency injection, calling services, and returning Pydantic response schemas.
   - **NO direct business logic or SQL queries allowed in route handlers.**

2. **`app/services/` (Service Layer)**
   - Encapsulates core domain business logic, workflow orchestration, validation rules, and caching coordination.
   - Wraps and delegates data operations to the repository layer.

3. **`app/repositories/` (Repository Layer)**
   - Performs database CRUD operations using SQLAlchemy sessions (`Session`).
   - **NO HTTP exceptions, request objects, or high-level business rules.**

4. **`app/models/` (SQLAlchemy ORM)**
   - Database table schema definitions extending SQLAlchemy declarative models.

5. **`app/schemas/` (Pydantic Schemas)**
   - Request and response validation contracts (`Base`, `Create`, `Update`, `Response`).

6. **`app/core/` (Infrastructure & Dependencies)**
   - Central settings (`config.py`), DB engine & Redis clients (`client.py`), lifecycle (`lifespan.py`), dependency injection factories (`dependency.py`).

---

## 3. Contribution Guidelines for AI Agents & Developers

When implementing new features or modifying existing code, always follow these rules:

1. **Strict 5-Layer Parity**:
   Every new domain entity (e.g. `artist`, `album`, `track`) MUST have a corresponding file in each layer:
   - `app/api/v1/<entity>.py`
   - `app/services/<entity>.py`
   - `app/repositories/<entity>.py`
   - `app/models/<entity>.py`
   - `app/schemas/<entity>.py`

2. **Dependency Injection**:
   - Routes inject services using `Depends(get_<entity>_service)`.
   - Services receive repositories via `__init__(self, repo: <Entity>Repository)`.
   - Repositories receive DB sessions via `__init__(self, db: Session)`.

3. **Graphify Knowledge Graph Rules**:
   - Whenever you edit or add code files, run `graphify update .` to keep `graphify-out/` current.
   - Use `graphify query "<question>"` to trace dependencies or understand relationships across modules before making large architectural changes.
   - **Do NOT commit `graphify-out/` to Git**—it is built automatically in GitHub Actions.

4. **Package & Environment Rules**:
   - Manage dependencies using `uv` (`uv add <package>`).
   - Do not create `requirements.txt` or manually edit `uv.lock`.

5. **Code Style & Standards**:
   - Use explicit type annotations everywhere.
   - Return clear Pydantic schemas in API endpoints.
   - Keep route handlers thin, repositories generic, and services focused.
