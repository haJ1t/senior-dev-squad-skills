---
name: fastapi-pro
description: "FastAPI patterns, Pydantic, async SQL, dependency injection, WebSocket, testing. Use when building or reviewing FastAPI services."
model: any
user-invocable: true
always: false
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

```
app/
  main.py                 ← App factory, lifespan, middleware
  config.py               ← Settings (pydantic-settings)
  dependencies.py         ← Shared DI (db, auth, pagination)
  models/
    __init__.py
    project.py            ← SQLAlchemy/Beanie models
  schemas/
    __init__.py
    project.py            ← Pydantic request/response schemas
  routers/
    __init__.py
    projects.py           ← /api/v1/projects endpoints
    users.py
  services/
    __init__.py
    project_service.py    ← Business logic layer
  tasks/
    __init__.py
    email_tasks.py        ← Background tasks / Celery
  tests/
    conftest.py
    test_projects.py
  migrations/             ← Alembic
  Dockerfile
```

### 2. Settings Management

```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()  # Singleton
```

### 3. Dependency Injection

```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = verify_token(token, settings.jwt_secret)
    user = await db.get(User, payload.sub)
    if not user:
        raise HTTPException(status_code=401)
    return user

async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403)
    return current_user
```

### 4. Router Patterns

```python
# routers/projects.py
from fastapi import APIRouter, Depends, Query, status

router = APIRouter(prefix="/api/v1/projects", tags=["projects"])

@router.get("/", response_model=PaginatedResponse[ProjectResponse])
async def list_projects(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """List projects with pagination and filtering."""
    projects, total = await ProjectService.list(
        db, user, page=page, per_page=per_page, status=status
    )
    return PaginatedResponse(
        data=projects,
        total=total,
        page=page,
        per_page=per_page,
    )

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    body: CreateProjectRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Create a new project."""
    return await ProjectService.create(db, user, body)
```

### 5. Pydantic Schemas

```python
# schemas/project.py
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from uuid import UUID

class CreateProjectRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)

class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: str
    owner_id: UUID
    created_at: datetime
    updated_at: datetime

class PaginatedResponse(BaseModel):
    data: list[ProjectResponse]
    total: int
    page: int
    per_page: int
```

### 6. Service Layer

```python
# services/project_service.py
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

class ProjectService:
    @staticmethod
    async def list(
        db: AsyncSession, user: User, page: int, per_page: int, status: str | None = None
    ) -> tuple[list[Project], int]:
        query = select(Project).where(Project.owner_id == user.id)
        count_query = select(func.count()).select_from(Project).where(Project.owner_id == user.id)

        if status:
            query = query.where(Project.status == status)

        total = await db.scalar(count_query)
        result = await db.execute(
            query.offset((page - 1) * per_page).limit(per_page)
        )
        return result.scalars().all(), total
```

### 7. Error Handling

```python
# Centralized exception handlers
class AppError(Exception):
    def __init__(self, code: str, message: str, status: int):
        self.code = code
        self.message = message
        self.status = status

@app.exception_handler(AppError)
async def app_error_handler(request, exc: AppError):
    return JSONResponse(
        status_code=exc.status,
        content={"error": {"code": exc.code, "message": exc.message}},
    )

# Usage
raise AppError("PROJECT_NOT_FOUND", "Project does not exist", 404)
raise AppError("INSUFFICIENT_PERMISSIONS", "Cannot delete another user's project", 403)
```

### 8. Async Testing

```python
# conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import create_app
from app.dependencies import get_db

@pytest.fixture
async def app():
    return create_app()

@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.fixture
async def db_session():
    async with async_session() as session:
        yield session

# test_projects.py
@pytest.mark.asyncio
async def test_create_project(client: AsyncClient, auth_header: dict):
    response = await client.post(
        "/api/v1/projects",
        json={"name": "Test Project"},
        headers=auth_header,
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Project"
```

### 9. Background Tasks

```python
# Using FastAPI's built-in BackgroundTasks (simple cases)
from fastapi import BackgroundTasks

async def send_welcome_email(email: str):
    await mail_service.send(email, "Welcome!")

@router.post("/signup")
async def signup(
    body: SignupRequest,
    tasks: BackgroundTasks,
):
    user = await UserService.create(body)
    tasks.add_task(send_welcome_email, user.email)
    return user

# Using Celery (production)
@celery.task
def generate_report(project_id: str):
    # Heavy background work
    pass
```

### Checklist

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

## Output Schema (MANDATORY)

```markdown
# [Review Type]: [Target]
## CRITICAL Findings
### C1: [Title] | [Framework]: [ID]
**Finding:** [What]
**Impact:** [Why matters]
**Fix:** [Concrete fix — code, not words]
## HIGH Findings
[Same format]
## MEDIUM / LOW
[Same format]
## Summary
- CRITICAL: N, HIGH: N, MEDIUM: N
- Verdict: PASS/FAIL
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague fixes ("add validation") | Not actionable | Show exact code |
| Missing severity tag | No prioritization | Always CRITICAL/HIGH/MEDIUM/LOW |
| Single-focus blindness | Misses related issues | Scan ALL categories separately |
| No framework mapping | Can't track compliance | Map to OWASP/MITRE/NIST |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Finding completeness | Missed major issues | Found most | All issues found |
| Severity accuracy | None/random | Some correct | All correctly rated |
| Fix quality | "Fix it" | Partial code | Complete, runnable fix |
| Framework mapping | None | Some mapped | All mapped to framework |
| Output format | Free text | Partial structure | Schema-compliant |

**Pass: 8/10**
