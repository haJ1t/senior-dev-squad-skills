---
name: architecture-planner
description: "ADR, tradeoff tables, mermaid diagrams, CAP awareness, deployment topology, full-stack architecture. Use when planning or documenting system architecture."
version: 2.0.0
---

# Architecture Planner v2

## Overview

Design production-ready architecture before implementation. Every decision documented with tradeoffs. **Benchmark-proven: without structured Iron Laws, models produce generic plans with no tradeoff analysis (tested across 4 frontier models).**

**Core principle:** NO IMPLEMENTATION WITHOUT AN APPROVED ARCHITECTURE.

## The Iron Laws

1. **EVERY decision MUST have a documented tradeoff** — If you chose X over Y and can't explain why, you guessed.
2. **Every service owns its database** — Shared database = distributed monolith, not microservices.
3. **The network is unreliable** — Every inter-service call: timeout + retry + circuit breaker. No exceptions.
4. **Idempotency is mandatory** — Every mutation must be safe to retry. Idempotency key on every write.
5. **CAP awareness** — For every data store data decision, declare: CP or AP? What happens during partition?

## MANDATORY Output Schema

```markdown
# Architecture: [System Name]

## 1. Service Decomposition
[Table: Service | Responsibility | Owns Data | Depends On | Scale Profile]

## 2. Architecture Decision Records (ADR)
### ADR-001: [Decision Title]
**Context:** [Why this decision matters]
**Options Considered:** [At least 2 alternatives]
**Decision:** [What we chose]
**Tradeoffs:** [What we gain + what we sacrifice]
**Consequences:** [What this means for the system]

## 3. Communication Matrix
[Table: From→To | Pattern | Protocol | Timeout | Retry | Circuit Breaker]

## 4. Data Consistency Strategy
[For each cross-service operation: Saga/Outbox/2PC/Eventual]
[Diagram: sequence showing happy path + compensation path]

## 5. CAP Tradeoffs
[Table: Data Store | Type | CP/AP | Partition Behavior | Justification]

## 6. Fault Tolerance
[Table: Failure Mode | Probability | Impact | Mitigation | Fallback]

## 7. Deployment Topology
```
[ASCII or mermaid diagram showing: regions, AZs, services, DBs, caches, queues]
```

## 8. Risk Register
[Table: Risk | Likelihood | Impact | Mitigation | Owner | Review Date]

## Architecture Verdict
- Decisions made: [count]
- Tradeoffs documented: [count]
- Known risks: [count]
- Critical unknowns: [list]
- Overall: READY FOR IMPLEMENTATION / NEEDS CLARIFICATION
```

## When to Use

**Use this when:**
- After spec-first-development has produced an approved spec.
- Starting a new project or major feature.
- The architecture touches multiple bounded contexts.
- Considering a database or infrastructure change.

**Don't skip when:**
- "It's just a CRUD app" (CRUD apps still need clean boundaries).
- "We'll refactor the architecture later" (you won't).
- "The app seems simple enough to figure out as we go".

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for all naming, and respect the decisions recorded in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## The Seven Phases

### Phase 1: System Decomposition

Split into bounded contexts. Each context must answer:

| Question | Answer Format |
|----------|--------------|
| **Responsibility** | What does this context own? |
| **API surface** | What contract does it expose? |
| **Data ownership** | What data does it manage exclusively? |
| **Dependencies** | What does it need from other contexts? |
| **Scaling concern** | Will this context need to scale independently? |

### Phase 2: Technology Decisions (ADR Format)

Every technology choice documented as Architecture Decision Record.

### Phase 3: API Contract

Define API BEFORE backend code. Every endpoint: request schema, response schema, error codes, rate limit.

### Phase 4: Database Model

Zero-downtime migrations. Index rules: FK columns always, WHERE columns, sort columns. Use EXPLAIN ANALYZE.

### Phase 5: Auth Model

Authentication method (JWT/OAuth/session) + Authorization model (RBAC/ABAC/ReBAC) + tenant isolation (RLS).

### Phase 6: Deployment Architecture

Environments (dev/staging/prod), CI/CD pipeline, container strategy, multi-AZ, disaster recovery.

### Phase 7: Risk Register

Every risk: likelihood, impact, mitigation, owner. Critical risks must have tested mitigations before production.

## Decision Tree

Use these branches before writing any ADR to avoid defaulting to the fashionable choice.

**Deployment model**
```
Is the team < 8 engineers?
├── YES → monolith first (single deployable, shared DB, domain packages for isolation)
│         Revisit when: independent deploy cadence needed OR distinct scale profiles emerge
└── NO  → Are bounded contexts independently deployable today?
          ├── YES → microservices (each owns its DB; see Iron Law 2)
          └── NO  → modular monolith (strict package boundaries, shared DB is acceptable
                    ONLY if packages never write to each other's tables)
```

**Communication pattern**
```
Does the caller need the result to continue?
├── YES → synchronous (REST or gRPC)
│         Mandatory: timeout + retry + circuit breaker on every call
│         If call chain depth > 2: reconsider async or introduce BFF/aggregator
└── NO  → asynchronous (event/message)
          Choose broker by replay need:
          ├── Replay needed (audit, re-processing) → Kafka / event-stream
          └── Fire-and-forget / work queue       → RabbitMQ / SQS
```

**Consistency model**
```
Can this data store tolerate a stale read during a partition?
├── NO  → CP (strong consistency): PostgreSQL primary, leader-election stores
│         Cost: writes refused or latency spikes during partition
└── YES → AP (eventual consistency): Redis cache, CDN, read replicas, search index
          Document the staleness bound (e.g. "menus stale up to 5 min acceptable")
```

**Cross-service write strategy**
```
Do multiple services own data that must change together?
├── Can one service own all the data? → refactor ownership (preferred)
└── Cannot → choose:
    ├── 2PC (XA)     → avoid in practice; blocks all participants, kills throughput
    ├── Saga         → choreography (events) or orchestration (workflow engine)
    │                  Use when: eventual consistency is acceptable, compensations are codeable
    └── Transactional Outbox → service writes event to its own DB atomically,
                               relay picks it up; strongest guarantee without 2PC
                               Use when: at-least-once delivery + idempotent consumers
```

## Worked Example

See `REFERENCE.md` in this directory for a complete walk-through: a **notifications service** decomposed into four bounded contexts, two full ADRs (broker choice + consistency strategy), a deployment topology sketch, and the CAP/outbox decision explained end-to-end. Read it before your first architecture session to see the method producing real output.

## Red Flags — STOP and Follow Process

**Decision quality failures:**
- No tradeoffs documented for any decision — a decision without tradeoffs is a guess
- ADR lists only one option ("we chose Kafka") — options considered is missing, so the reasoning cannot be reviewed
- "We'll figure out the tech stack later" — tech choices ARE architecture; deferring them defers the architecture

**Boundary failures:**
- Two or more services writing to the same database table — this is a distributed monolith, not microservices
- Services share a database and the boundaries are "logical" — logical boundaries in a shared schema drift to zero
- "We'll split the monolith later" — the coupling that makes it a monolith is the same coupling that makes splitting it later painful

**Network / reliability failures:**
- Any inter-service call without a documented timeout — timeouts are not optional; the network will hang
- Sync call chain depth > 2 without a circuit breaker — fan-out sync calls cascade failures by design
- No idempotency strategy for any mutation — retries without idempotency cause double-writes; this is a data corruption risk

**Consistency failures:**
- Cross-service write with no documented consistency strategy (no saga, no outbox, no 2PC decision)
- "We'll handle distributed transactions with try/catch" — catching exceptions across network boundaries does not provide atomicity
- No documented partition behavior for any data store — partitions happen; "we're on AWS" is not a mitigation

**Documentation failures:**
- No mermaid/ASCII deployment diagram — if the team cannot draw where services run, they disagree about it
- "The API is obvious, no need to document it" — obvious APIs still generate conflicting implementations
- "This DB will work for now, we can migrate later" — live data migrations under load are the most expensive non-feature in distributed systems

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll document decisions later" | Future you has no memory of today's tradeoffs. The ADR takes 10 minutes now or 10 hours of archaeology later. |
| "Everyone knows why we chose Postgres" | New team members don't. Neither will you in 6 months after three oncall rotations. |
| "Let's keep it flexible" | "Flexible" without constraints is undefined. Vague architectures create integration bugs, not options. |
| "CAP doesn't matter in practice" | Every cloud outage is a partition event. Not knowing your CP/AP choice means discovering it during an incident. |
| "Microservices give us agility" | Microservices without clear bounded contexts and owned data give you a distributed monolith with network latency added. |
| "We don't need a circuit breaker, our infra is reliable" | Circuit breakers protect against slow callers, not just down callers. Timeouts without circuit breakers let slow dependencies drain your thread pools. |
| "We can handle failures with retries" | Retries without idempotency keys turn transient failures into duplicate transactions. Idempotency is a correctness requirement, not a nice-to-have. |

## Output Quality Bar

**Bad output** names technologies without decomposing bounded contexts, skips tradeoff tables, and writes "deploy to AWS" without an AZ diagram. **Good output** follows the MANDATORY schema above: every service has a responsibility and owns its data, every ADR names at least two alternatives, every data store has a CP/AP declaration, and the deployment diagram shows regions, AZs, and replica counts.

See `REFERENCE.md` in this directory for a complete worked example (notifications service, 4 services, 2 full ADRs, topology diagram, outbox decision, CAP table, risk register).

## Model-Specific Calibration (BENCHMARK FINDINGS)

| Model | Tendency | Calibration |
|-------|---------|-------------|
| **Claude Sonnet 4** | Most structural, naturally follows the ADR format, deployment details are good | "Compare at least 2 alternatives in each ADR" — Claude sometimes offers only one option |
| **GPT-4o** | Fast but skips tradeoffs, writes "what we chose" instead of "why we chose it" | "For every choice, write: 'We chose X over Y because...' — never just state the choice" |
| **Gemini 2.5 Pro** | Shortest, performs CAP analysis naturally but deployment topology is weak | "Draw an ASCII or mermaid deployment diagram showing regions, AZs, and service placement" |
| **DeepSeek V3** | Most economical, good concrete YAML examples but skips the risk register | "Complete the Risk Register with at least 5 risks — likelihood, impact, mitigation, owner" |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "How does service X talk to service Y?" — The communication matrix is absent or lists patterns without timeout and retry values.
- "What happens if the payment service is down?" — Fault tolerance section is missing or the failure mode has no fallback documented.
- "We never agreed to use Kafka" — A technology decision was made without an ADR, so the reasoning was never visible or approved.
- "The deploy blew up because we didn't account for the migration" — Database migration strategy was skipped or marked "TBD" in the architecture doc.
- "Why are there two services sharing the same database?" — Data ownership boundaries were not enforced during decomposition.
- "This looks fine on paper but I have no idea how it runs" — Deployment topology section is missing or describes only "deploy to cloud" without AZ diagram.

**When you see these:** STOP. Return to the relevant phase (decomposition, ADR, communication matrix, fault tolerance, or deployment topology), resolve the gap with a documented decision and tradeoff, and re-run the verification checklist before handing off to implementation.

## Related Skills

- **spec-first-development** — run BEFORE this skill; the approved spec is the required input
- **task-breaker** — run AFTER this skill to convert the architecture into ordered, agent-executable tasks
- **security-reviewer** — reviews the auth model and data boundary decisions produced in Phase 5
- **test-engineer** — derives integration and contract test strategy from the communication matrix
- **performance-engineer** — validates the scaling profile and CAP tradeoff decisions against load requirements
- **code-reviewer** — verifies the architecture document passes its checklist before implementation begins

## Verification Checklist

- [ ] Every bounded context has clear responsibility + data ownership
- [ ] Every technology decision has an ADR with tradeoffs
- [ ] Communication matrix complete (every call: timeout, retry, circuit breaker)
- [ ] CAP analysis for every data store
- [ ] Deployment topology diagram (ASCII or mermaid)
- [ ] Risk register with mitigations for High/Critical risks
- [ ] Idempotency strategy documented for all mutations
- [ ] Output follows MANDATORY schema
- [ ] Architecture Verdict: READY FOR IMPLEMENTATION
