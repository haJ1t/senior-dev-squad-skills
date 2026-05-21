---
name: performance-engineer
description: "Bundle size, lazy loading, N+1, indexes, caching, Core Web Vitals. Use when diagnosing or fixing performance issues."
---

# Performance Engineer

## Overview

Find and fix performance issues across the full stack. Performance is a feature — users notice speed more than any UI polish. A 100ms delay costs 1% conversion. A 1s delay costs 10%.

**Core principle:** MEASURE BEFORE YOU OPTIMIZE. WITHOUT METRICS, YOU'RE GUESSING.

## The Iron Law

```
EVERY OPTIMIZATION MUST BE VERIFIED BY MEASUREMENT
Without a before/after measurement, you didn't optimize — you just added complexity.
```

## When to Use

**Use this when:**
- A page or endpoint is noticeably slow and you need to find the cause
- A PR introduces new database queries, data fetching, or heavy computation
- Core Web Vitals scores (LCP, INP, CLS) are in the "Poor" range
- A feature is approaching scale (10K+ users, large datasets, high throughput)

**Use this ESPECIALLY when:**
- Someone says "it's fast enough on my machine" (production data is always larger)
- N+1 query patterns appear during a code review
- A new background job, scheduled task, or data migration is being added
- Bundle size grows significantly after adding a new library

**Don't skip when:**
- The app is user-facing and conversion or retention depends on speed
- A slow query is already in production and causing timeouts or degraded UX

## Core Web Vitals (Frontend)

| Metric | Good | Poor | User Impact |
|--------|------|------|-------------|
| LCP | ≤ 2.5s | > 4.0s | Page feels slow |
| INP | ≤ 200ms | > 500ms | UI feels unresponsive |
| CLS | ≤ 0.1 | > 0.25 | Content jumps while reading |

## N+1 Query Detection (Backend — #1 killer)

```sql
-- BAD: 1 query for projects + N queries for tasks = N+1
SELECT * FROM projects;
-- For each project:
SELECT * FROM tasks WHERE project_id = $1;

-- GOOD: 1 query with JOIN
SELECT p.*, t.* FROM projects p
LEFT JOIN tasks t ON p.id = t.project_id;
```

## Caching Strategy

| Layer | Cache Type | TTL | Hit Rate Target |
|-------|-----------|-----|----------------|
| CDN | Static assets | 1 year | 99% |
| API | HTTP cache (Cache-Control) | 5-60s | 70% |
| App | In-memory / Redis | 30-300s | 80% |
| Client | SWR / React Query | Stale-while-revalidate | 90% |

## Red Flags — STOP

"This page is fast enough on my machine" — dev DB has 10 rows, production has 10M.
"We'll add indexes later" — the slow query is already in production.
"N+1 is fine for small datasets" — small datasets become large datasets.
"I know what's slow, no need to measure" — you're wrong. Measure first.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Dev machine is fast enough" | Dev database has 10 rows. Production has 10M. |
| "We'll add indexes later" | The query is already slow in production. |
| "Premature optimization is the root of all evil" | So is shipping apps that crawl. |
| "CDN is overkill for our site" | A CDN is a few DNS changes and saves 50% load time. |



## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "We don't have time to profile, just fix the query" — you haven't explained why measurement must come first
- "That's a lot of infrastructure for a small app" — you recommended caching layers or CDN configuration that outscale the problem
- "The numbers look the same to me" — your before/after metrics were unclear or not shown side by side
- "That made things worse" — you optimized without establishing a baseline and introduced regression
- "Can you just add an index?" — you proposed architectural changes when a targeted fix was sufficient

**When you see these:** STOP. Return to the measurement-first principle. Establish a concrete baseline metric, then propose the smallest intervention that moves that specific number.

## Related Skills

- **spec-first-development** — performance requirements (LCP targets, query budgets) should be captured in the spec before implementation
- **code-reviewer** — use alongside code review to catch N+1 queries, missing indexes, and unoptimized bundle imports before they reach production
- **architecture-planner** — caching strategy, database read replicas, and CDN topology are architectural decisions that need planning before implementation
- **test-engineer** — performance regression tests and load tests must be written alongside optimizations to prevent backsliding
- **devops-release-engineer** — performance monitoring, alerting thresholds, and rollout strategies for optimizations belong in the deployment pipeline

## Output Schema (MANDATORY)

Structure your response with:
1. **Analysis** — What you found/designed
2. **Concrete output** — Code, YAML, tables (not just descriptions)
3. **Tradeoffs/risks** — What you chose and why, what could go wrong
4. **Verification** — How to confirm correctness

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague recommendations | Not actionable | Concrete examples, specific steps |
| Missing tradeoffs | One-sided analysis | Every choice: "X over Y because..." |
| "Consider doing X" | No commitment | "Do X. Why: [reason]" |
| No verification criteria | Can't confirm quality | "Verify by: [test/check]" |
| Generic response | Not tailored | Domain-specific vocabulary, exact tool names |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Specificity | Generic advice | Some specifics | Concrete, actionable output |
| Tradeoff awareness | None | Mentioned | Documented with alternatives |
| Output format | Free text | Partial structure | Structured, scannable |
| Verification | None | Vague | Specific test/criteria |
| Domain accuracy | Wrong terms | Mostly correct | Precise domain vocabulary |

**Pass: 7/10**
