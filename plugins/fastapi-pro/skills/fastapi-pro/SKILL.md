---
name: fastapi-pro
description: "FastAPI patterns, Pydantic, async SQL, dependency injection, WebSocket, testing. Use when building or reviewing FastAPI services."
---

# FastAPI Pro

## Purpose

Build production-grade FastAPI applications with proper dependency injection, async patterns, validation, testing, and OpenAPI documentation.

## When to Use

**Use this when:**
- Building async Python APIs with FastAPI, Pydantic v2, and SQLAlchemy async sessions
- Structuring dependency injection chains for auth, database sessions, and pagination
- Writing pytest-asyncio tests against a real test database with AsyncClient

**Use this ESPECIALLY when:**
- Adding authentication — JWT dependency chains must be composed correctly from the start
- Defining Pydantic schemas for request validation or ORM-backed response serialization
- Any route calls a database or external service — sync calls inside async handlers will block the event loop

**Don't skip when:**
- Creating a new router module — prefix, tags, and DI wiring must follow project conventions consistently
- Adding background work — choosing between `BackgroundTasks` and Celery has operational consequences

## Core Patterns

### 1. Project Structure

Canonical layout: `app/main.py` (factory + lifespan), `config.py` (pydantic-settings), `dependencies.py` (shared DI), `models/`, `schemas/`, `routers/`, `services/`, `tasks/`, `tests/`, `migrations/`. See [REFERENCE.md](REFERENCE.md) for the full directory tree.

### 2. Settings Management

Use `pydantic-settings` `BaseSettings` with a singleton `settings = Settings()`. Fields: `database_url`, `redis_url`, `jwt_secret`, `jwt_algorithm`, `access_token_expire_minutes`, `environment`. See [REFERENCE.md](REFERENCE.md) for the full `config.py` snippet.

### 3. Dependency Injection

Chain `get_db` → `get_current_user` → `get_admin_user` using `Depends`. Each dependency yields an `AsyncSession` or raises `HTTPException`. See [REFERENCE.md](REFERENCE.md) for the full `dependencies.py` example with JWT verification.

### 4. Router Patterns

Routers declare `prefix`, `tags`, and inject `db`/`user` via `Depends`. Paginated list endpoints take `page`/`per_page`/filter `Query` params and return a `PaginatedResponse`. See [REFERENCE.md](REFERENCE.md) for `list_projects` and `create_project` examples.

### 5. Pydantic Schemas

Request schemas use `Field` validators; response schemas set `model_config = ConfigDict(from_attributes=True)` for ORM serialization. Wrap list endpoints in a generic `PaginatedResponse[T]`. See [REFERENCE.md](REFERENCE.md) for `CreateProjectRequest`, `ProjectResponse`, and `PaginatedResponse` definitions.

### 6. Service Layer

Business logic lives in `services/`, separate from routers. Services receive an `AsyncSession` and return typed results. Count queries use `func.count()` with a matching `WHERE` clause. See [REFERENCE.md](REFERENCE.md) for the `ProjectService.list` example with offset pagination.

### 7. Error Handling

Define an `AppError(Exception)` with `code`, `message`, `status`, and register a global `@app.exception_handler(AppError)` that returns a consistent `{"error": {"code": ..., "message": ...}}` JSON shape. See [REFERENCE.md](REFERENCE.md) for the handler and usage examples.

### 8. Async Testing

Use `httpx.AsyncClient` with `ASGITransport` against the real app and a real test DB. Fixtures: `app`, `client`, `db_session` — all `async`. Mark tests with `@pytest.mark.asyncio`. See [REFERENCE.md](REFERENCE.md) for the full `conftest.py` and a sample test.

### 9. Background Tasks

Use FastAPI's `BackgroundTasks` for lightweight async work (e.g. welcome emails). Use Celery for heavy production work (e.g. report generation). See [REFERENCE.md](REFERENCE.md) for both patterns with code examples.

## Checklist

- [ ] Async everywhere (no sync DB or HTTP calls)
- [ ] Pydantic v2 schemas with `from_attributes=True` for ORM
- [ ] Dependency injection for db, auth, pagination
- [ ] Service layer separates business logic from routes
- [ ] Error responses follow consistent format
- [ ] OpenAPI docs enabled and accurate (endpoint descriptions)
- [ ] CORS configured (not `*` in production)
- [ ] Rate limiting implemented (slowapi or custom)
- [ ] Health check endpoint (`/health`)
- [ ] Alembic migrations for schema changes
- [ ] Tests use real test DB (not mocks)

## Related Skills

- **backend-senior-engineer** — design the service and repository layers that FastAPI routers delegate to, especially for complex domain logic
- **api-design-reviewer** — review Pydantic request/response schemas and OpenAPI doc accuracy before the API is consumed by clients
- **postgres-pro** — optimize SQLAlchemy async queries, connection pool settings, and Alembic migration patterns for PostgreSQL backends
- **test-engineer** — structure pytest-asyncio fixtures, async test databases, and httpx AsyncClient test suites for FastAPI apps
- **security-reviewer** — audit JWT dependency chains, CORS configuration, and rate-limiting middleware for authentication bypass risks
- **django-pro** — reference when migrating from or comparing Django/DRF patterns; FastAPI and Django handle auth and ORM differently
- **performance-engineer** — profile async endpoint concurrency, connection pool exhaustion, and background task queue depth
