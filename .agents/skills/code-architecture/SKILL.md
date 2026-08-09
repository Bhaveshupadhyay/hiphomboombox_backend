---
name: code-architecture
description: Code architecture, design patterns, 5-layer Clean repository-service structure, and contribution guidelines for HipHopBoomBox backend.
---

# Code Architecture & Contribution Guidelines

This skill provides comprehensive instructions for understanding, navigating, and contributing to the **HipHopBoomBox Backend** codebase.

---

## 1. Tech Stack & Infrastructure

- **Framework**: FastAPI (Python ≥ 3.12 / specified as `>=3.14` in `pyproject.toml`)
- **Package Manager**: `uv` (using `pyproject.toml` and `uv.lock`)
- **Database & ORM**: PostgreSQL via SQLAlchemy 2.0 (`sessionmaker` sync sessions)
- **Caching**: Upstash Redis (`upstash-redis`)
- **Data Validation & Settings**: Pydantic v2 & `pydantic-settings`
- **Containerization**: Docker (`Dockerfile`)

---

## 2. Layered Architecture Pattern

The project strictly follows a **5-Layer Domain Pattern** backed by a `core/` infrastructure module:

```text
app/
├── api/v1/          # 1. API Route Handlers (Controllers)
├── services/        # 2. Service Layer (Business Logic & Transactions)
├── repositories/    # 3. Repository Layer (Raw DB Queries & Persistence)
├── models/          # 4. ORM Layer (SQLAlchemy Models)
├── schemas/         # 5. Schema Layer (Pydantic DTOs & Validation)
└── core/            # Infrastructure (Config, DB Engine, Redis, DI)
```

### Layer Responsibilities:

1. **`app/api/v1/` (Route Handlers)**
   - Responsible only for request parsing, status codes, dependency injection, calling services, and returning Pydantic response schemas.
   - **NO direct business logic or raw SQL queries allowed in route handlers.**

2. **`app/services/` (Service Layer)**
   - Encapsulates domain logic, workflow orchestration, validation rules, and caching coordination.
   - Wraps and delegates data persistence to the repository layer.

3. **`app/repositories/` (Repository Layer)**
   - Performs database CRUD operations using SQLAlchemy sessions (`Session`).
   - **NO HTTP exceptions, request objects, or high-level business rules.**

4. **`app/models/` (SQLAlchemy ORM)**
   - Database table schema definitions extending SQLAlchemy declarative models.

5. **`app/schemas/` (Pydantic Schemas)**
   - Request and response validation contracts (`Base`, `Create`, `Update`, `Response`).

6. **`app/core/` (Infrastructure & Dependencies)**
   - Settings (`config.py`), DB engine & Redis clients (`client.py`), lifecycle (`lifespan.py`), dependency injection factories (`dependency.py`).

---

## 3. Contribution Guidelines

When creating new features or refactoring existing code, always follow these rules:

1. **Strict 5-Layer Parity**:
   Every new domain entity (e.g., `artist`, `album`) MUST have a corresponding file across all 5 domain layers:
   - `app/api/v1/<entity>.py`
   - `app/services/<entity>.py`
   - `app/repositories/<entity>.py`
   - `app/models/<entity>.py`
   - `app/schemas/<entity>.py`

2. **Dependency Injection Pattern**:
   Wire repositories and services in `app/core/dependency.py` and inject services into route handlers using FastAPI's `Depends`:

   ```python
   # app/core/dependency.py
   def get_post_repo() -> PostRepository:
       return PostRepository(get_db)

   def get_post_service() -> PostService:
       repo = get_post_repo()
       return PostService(repo)

   # app/api/v1/post.py
   @router.get("/", response_model=list[PostResponse])
   def get_all_posts(service: PostService = Depends(get_post_service)):
       return service.get_all_posts()
   ```

3. **Package & Environment Rules**:
   - Manage dependencies using `uv` (`uv add <package>`).
   - Do not create `requirements.txt` or manually edit `uv.lock`.

4. **Code Style & Error Handling**:
   - Use explicit type annotations everywhere.
   - Return clear Pydantic schemas in API endpoints.
   - Raise explicit `HTTPException(status_code=..., detail=...)` at the API handler level.
