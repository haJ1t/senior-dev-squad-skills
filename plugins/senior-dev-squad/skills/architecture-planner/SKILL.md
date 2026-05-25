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

## Red Flags — STOP and Follow Process

- No tradeoffs documented for any decision
- "We'll figure out the tech stack later"
- "The API is obvious, no need to document it"
- "This DB will work for now, we can migrate later"
- No mermaid/ASCII deployment diagram
- Missing idempotency strategy
- "We don't need CAP analysis, we're on AWS"

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll document decisions later" | Future you has no memory of today's tradeoffs. |
| "Everyone knows why we chose Postgres" | New team members don't. Neither will you in 6 months. |
| "Let's keep it flexible" | Vague architectures create more work, not less. |
| "CAP doesn't matter in practice" | Every cloud outage is a partition. Know your CP/AP choice. |

## Few-Shot Examples (MANDATORY Reference)

### ❌ BAD Output (Most common in benchmarks)

```markdown
## Architecture
Use microservices with Kafka for async communication. 
PostgreSQL for main DB, Redis for caching.
```
**Why it is bad:** Which services? Which bounded contexts? CAP analysis? Tradeoffs? Deployment topology? None of these are present.

### ✅ GOOD Output (As it should be)

```yaml
## Service Decomposition
| Service | Responsibility | Owns Data | Depends On | Scale Profile |
|---------|---------------|-----------|------------|---------------|
| order-service | Order lifecycle, state machine | orders, order_items | payment-service (async) | 10K writes/min, 50K reads/min |
| payment-service | Payment processing, PCI-DSS scope | payments, payment_methods | stripe (external) | 5K writes/min |
| restaurant-service | Restaurant profile, menu, hours | restaurants, menus, hours | — | 1K writes/min, 100K reads/min |
| delivery-service | Driver tracking, assignment, ETA | drivers, assignments, locations | maps (external) | 50K location updates/min |

## ADR-001: Kafka over RabbitMQ
**Context:** Order service needs to notify payment, delivery, notification services.
**Options:** Kafka (event streaming), RabbitMQ (message queue), Direct HTTP
**Decision:** Kafka
**Tradeoffs:** +Replay capability, +Partition ordering, +Throughput | -Operational complexity, -Higher latency floor (~5ms vs ~1ms)
**Consequences:** Need Kafka Connect for CDC, Schema Registry for Avro evolution, 12 partitions for order events topic

## CAP Analysis
| Data Store | Type | CP/AP | Partition Behavior |
|-----------|------|-------|-------------------|
| orders (PostgreSQL) | RDBMS | CP | Refuses writes during partition (consistency > availability for orders) |
| driver_locations (Redis) | Cache | AP | Continues accepting writes, eventual consistency with Postgres |
| menu_cache (CDN) | Read cache | AP | Stale data acceptable (menus change infrequently) |
```

### ❌ BAD: Missing deployment topology
```markdown
## Deployment
Deploy to AWS with auto-scaling.
```
**Why it is bad:** Which region? How many AZs? How many instances? Network topology? None.

### ✅ GOOD: Complete deployment diagram
```
                    [CloudFront CDN]
                          |
                    [ALB - us-east-1]
                    /        |        \
               [az-1a]   [az-1b]   [az-1c]
                 |          |          |
            [order-svc] [order-svc] [order-svc]  (3 replicas, HPA: 2-10)
                 |          |          |
            [RDS Primary - az-1a] [RDS Standby - az-1b]
                       |
            [Read Replica - az-1c]
                       |
            [ElastiCache Redis - Cluster mode, 3 shards]
                       |
            [MSK Kafka - 3 brokers, 12 partitions]
                       |
            [eu-west-1 — Active-Passive, async replication, RPO: 5min, RTO: 15min]
```

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
