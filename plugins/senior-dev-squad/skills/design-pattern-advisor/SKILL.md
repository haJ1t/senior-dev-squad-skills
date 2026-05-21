---
name: design-pattern-advisor
description: "Design pattern catalog, pattern selection guide, code sketches, project-type recommendations. Use when choosing the right design pattern for a problem."
---

# Design Pattern Advisor

## Overview

Recommend the right design patterns for a project based on its type, scale, and requirements. Don't just name-drop patterns — show how each one applies with a short code sketch specific to THIS project.

**Core principle:** PATTERNS ARE SOLUTIONS TO PROBLEMS, NOT CHECKLIST ITEMS TO COLLECT.

## The Iron Law

```
NEVER RECOMMEND A PATTERN WITHOUT SHOWING WHY IT APPLIES TO THIS SPECIFIC PROJECT
```

"Use Repository pattern" without showing the data access code = cargo culting.

## When to Use

**Use this when:**
- Architecture decision needs pattern guidance
- User asks "what patterns should I use?"
- Before architecture-planner for complex projects
- When reviewing code and it's missing appropriate patterns

## Pattern Selection Guide

### Project Type → Recommended Patterns

| Project Type | Core Patterns | When to Add |
|-------------|--------------|-------------|
| **Web API** | Repository, Service Layer, DTO, Middleware Chain | CQRS for complex queries, Saga for distributed transactions |
| **Full-stack Web** | Component, Container/Presenter, Controlled Components, Custom Hooks | State Machine for complex UI flows |
| **CLI** | Command, Builder, Option/Fluent Builder | Plugin for extensibility |
| **Library/SDK** | Facade, Factory, Strategy | Adapter for multiple backends |
| **Data Pipeline** | Pipeline, Chain of Responsibility, Strategy | Observer for events |
| **Game** | Component (ECS), State, Observer, Object Pool | Command for undo/redo |
| **Mobile** | MVVM, Repository, Coordinator/Navigation | Observer for reactive updates |
| **Microservice** | Saga, Circuit Breaker, API Gateway, Strangler Fig | CQRS + Event Sourcing |

### Scale → Required Patterns

```
<100 users:  Service Layer, Repository (optional), Component patterns
100-10K:     Repository, Service Layer, Middleware Chain, DTO
10K-100K:    CQRS (read models), Cache-Aside, Queue-based Load Leveling
100K+:       CQRS, Event Sourcing, Saga, Circuit Breaker, Bulkhead
```

## Pattern Selection by Concern

```
Need to organize business logic?
  → Service Layer: Encapsulate domain logic from infrastructure
  → Domain Model: Rich domain objects with behavior (not anemic)

Need to abstract data access?
  → Repository: Abstracts persistence from business logic
  → Unit of Work: Coordinates multiple repository writes as one transaction

Need to handle complex workflows?
  → State Machine: Explicit states, transitions, guards
  → Strategy: Swappable algorithms at runtime
  → Chain of Responsibility: Pipeline of handlers, each decides next

Need to decouple components?
  → Observer/Pub-Sub: One-to-many notifications
  → Mediator: Centralizes complex communication between components
  → Event Bus: Decoupled event publishing/subscribing

Need to manage cross-cutting concerns?
  → Middleware Chain: Request pipeline (auth, logging, rate limiting)
  → Decorator: Wraps core logic with additional behavior
  → Proxy: Controls access to another object (lazy, remote, protection)

Need to handle errors/failures?
  → Circuit Breaker: Prevents cascading failures
  → Retry with Backoff: Handles transient failures
  → Saga: Coordinates failure recovery across services
  → Bulkhead: Isolates failures to one part of the system
```

## Code Sketch Format

For every recommended pattern, show:

```typescript
// Repository Pattern — WHY it applies here
// This project has complex query logic that would bloat controllers
// Repository encapsulates all data access, keeps controllers thin

interface ProjectRepository {
  findById(id: string): Promise<Project | null>
  findActiveByOwner(ownerId: string, page: number): Promise<PaginatedResult<Project>>
  create(data: CreateProjectDTO): Promise<Project>
  update(id: string, data: Partial<Project>): Promise<Project>
  delete(id: string): Promise<void>
}

class PostgresProjectRepository implements ProjectRepository {
  constructor(private db: PrismaClient) {}

  async findById(id: string): Promise<Project | null> {
    return this.db.project.findUnique({ where: { id } })
  }
  // ...remaining methods with specific query patterns
}
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This project should use Repository pattern — every project needs it"
- "I'll recommend all the patterns I know, the developer can pick"
- "Microservice patterns apply here even though it's a small monolith"
- "The pattern is well-known so I don't need to show how it fits this code"
- "We can add the Facade layer later when complexity grows"
- "Singleton is fine here, everyone uses it"

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This pattern is industry standard" | Standards exist for contexts. Show why this context matches. |
| "We'll abstract it properly once we have more use cases" | Premature abstraction and late abstraction are both painful — pick the right pattern now. |
| "The developer knows the patterns, I just need to name them" | Naming without application is cargo-culting. Show the code sketch. |
| "CQRS/Event Sourcing is best practice for scalability" | These patterns carry enormous operational overhead. Only recommend when scale demands it. |
| "We can swap patterns later if this one doesn't fit" | Ripping out a core structural pattern after implementation costs weeks. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "That seems over-engineered for what we need" — you recommended enterprise patterns for a small project
- "We already have something like that" — you didn't explore the existing code before recommending
- "How does that actually work in our codebase?" — your recommendation was abstract, not grounded in their code
- "That's too many patterns at once" — you recommended every applicable pattern instead of the two or three that matter most
- "We tried that before and it made things worse" — you didn't ask about prior attempts and constraints

**When you see these:** STOP. Re-read the project type and scale indicators. Return to the Pattern Selection Guide and cut recommendations to the essential core patterns only.

## 1. Components/Contexts
[Table: Name | Responsibility | Data | Dependencies]
## 2. Decisions (ADR format)
### ADR-001: [Title]
**Context:** [Why] **Options:** [2+ alternatives] **Decision:** [What] **Tradeoffs:** [+gain / -sacrifice]
## 3. Communication Matrix
[Table: From→To | Pattern | Protocol | Timeout | Retry]
## 4. Data & CAP Analysis
[Per store: Type | CP/AP | Partition behavior]
## 5. Deployment Topology
[ASCII diagram]
## Verdict: READY / NEEDS CLARIFICATION
```

## Related Skills

- **architecture-planner** — uses pattern recommendations
- **code-reviewer** — verifies patterns are applied correctly

## Verification

- [ ] Patterns match project type + scale
- [ ] Each pattern includes "why this applies here" rationale
- [ ] Each pattern has project-specific code sketch
- [ ] Trade-offs documented for each recommendation
