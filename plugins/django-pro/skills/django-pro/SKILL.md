---
name: django-pro
description: "Django ORM, DRF, signals, management commands, Celery, testing. Use when building or reviewing Django applications."
model: any
user-invocable: true
always: false
---

# Django Pro

## Purpose

Build production-grade Django applications with clean project structure, optimized ORM queries, DRF best practices, Celery background tasks, and comprehensive testing.

## When to Use

**Use this when:**
- Building REST APIs or full-stack web apps in Python using Django or Django REST Framework
- Working with Django ORM models, migrations, signals, or admin customization
- Adding Celery background tasks, management commands, or custom middleware to a Django project

**Use this ESPECIALLY when:**
- Diagnosing N+1 query problems, slow ORM queries, or missing database indexes
- Structuring a multi-app Django project with proper settings splitting and app boundaries
- Writing DRF serializers, viewsets, permission classes, or custom filter backends

**Don't skip when:**
- Touching Django models for the first time in a project — migration safety and index design matter immediately
- Implementing any authenticated endpoint — DRF permission layering must be deliberate from the start

## Core Patterns

### 1. Project Structure

```
project/
  settings/
    base.py        ← Shared settings
    development.py
    production.py
    test.py
  urls.py           ← Root URL config
  wsgi.py / asgi.py

apps/
  projects/
    migrations/
    templates/
    __init__.py
    admin.py
    apps.py
    models.py       ← Project, Task, ProjectMember
    serializers.py  ← DRF serializers
    views.py         ← API views / viewsets
    urls.py
    filters.py       ← django-filter
    permissions.py
    signals.py
    tasks.py         ← Celery tasks
    tests/
      test_models.py
      test_views.py
      test_services.py
    management/
      commands/
        backfill_project_stats.py

templates/
static/
media/
```

### 2. Model Design

```python
# apps/projects/models.py
import uuid
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator

class Project(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        ARCHIVED = "archived", "Archived"
        DELETED = "deleted", "Deleted"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    description = models.TextField(blank=True, default="")
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="projects",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name
```

### 3. DRF ViewSets

```python
# apps/projects/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status"]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        project = self.get_object()
        project.status = Project.Status.ARCHIVED
        project.save()
        return Response({"status": "archived"})
```

### 4. ORM Performance

```python
# ✅ Select related (avoid N+1)
projects = Project.objects.select_related("owner").all()

# ✅ Prefetch related (for reverse relations)
projects = Project.objects.prefetch_related("tasks").all()

# ✅ Only needed fields
projects = Project.objects.only("id", "name", "owner_id")

# ✅ Batch operations
Project.objects.filter(status="archived").update(status="deleted")

# ❌ Never do this in a loop
for project in projects:
    print(project.tasks.count())  # N queries!
```

### 5. Celery Tasks

```python
# apps/projects/tasks.py
from celery import shared_task
from django.utils import timezone

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def generate_project_report(self, project_id):
    try:
        project = Project.objects.get(id=project_id)
        report = ReportGenerator.generate(project)
        return {"project_id": str(project.id), "report_id": str(report.id)}
    except Project.DoesNotExist:
        logger.error(f"Project {project_id} not found")
        return None
    except Exception as exc:
        raise self.retry(exc=exc)
```

### 6. Signals

```python
# apps/projects/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

@receiver(post_save, sender=Project)
def project_created_handler(sender, instance, created, **kwargs):
    if created:
        # Create default project settings
        ProjectSettings.objects.create(project=instance)
        # Send notification
        notify_user(instance.owner, f"Project '{instance.name}' created")
```

### Checklist

- [ ] Select_related / prefetch_related for all queries
- [ ] Indexes on foreign keys and filtered fields
- [ ] UUID primary keys (not auto-increment)
- [ ] Soft deletes (is_active or status field)
- [ ] Django FilterBackend for list filtering
- [ ] Throttling on API views (`UserRateThrottle`)
- [ ] Celery tasks with retry logic
- [ ] db_index on frequently filtered fields
- [ ] N+1 query detection (django-debug-toolbar or nplusone)
- [ ] .only() / .defer() for large model queries



## Related Skills

- **backend-senior-engineer** — use for service-layer architecture decisions and cross-cutting concerns before implementing Django business logic
- **postgres-pro** — pair when designing Django model indexes, writing raw SQL, or tuning ORM-generated queries against PostgreSQL
- **api-design-reviewer** — review DRF serializer contracts and endpoint conventions before they are consumed by clients
- **test-engineer** — covers pytest-django fixtures, factory_boy patterns, and test database isolation strategies for Django test suites
- **security-reviewer** — audit DRF permission classes, authentication backends, and signal handlers for privilege escalation risks
- **devops-release-engineer** — integrate Celery workers, management command runners, and Django migrations into CI/CD pipelines
- **performance-engineer** — profile Django ORM query plans, connection pool sizing, and cache layer (Redis/Memcached) configuration

## Output Schema (MANDATORY)

```markdown
## Endpoint: [METHOD] [PATH]
### Request
```json
{"field": "type (constraints)"}
```
### Success (200/201)
```json
{"data": {}, "meta": {"requestId": "uuid"}}
```
### Errors
| Status | Code | When |
### Implementation
```[lang]
[Full code with: validation, auth, transaction, logging, rate limit, idempotency]
```
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| No input validation | Security hole | Schema validation at boundary |
| Missing transaction | Data corruption | Atomic multi-step operations |
| No idempotency | Duplicate writes on retry | Idempotency key + cached response |
| print() instead of logger | No structured logs | JSON logger with requestId |
| No rate limiting | DoS vulnerable | Rate limiter on every endpoint |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Input validation | None | Partial | Full schema per field |
| AuthN/AuthZ | None | AuthN only | Both layers |
| Transaction safety | None | Partial | All multi-step atomic |
| Error handling | None | Generic | Specific + error schema |
| Rate limiting | None | Commented | Working implementation |
| Idempotency | None | Key exists | Check + cached response |
| Structured logging | print() | Basic | requestId + context |

**Pass: 10/14**
