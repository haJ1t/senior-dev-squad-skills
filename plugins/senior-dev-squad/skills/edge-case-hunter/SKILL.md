---
name: edge-case-hunter
description: "8-dimension edge case matrix, Scenario→Expected→Actual format, concurrency/time/state/scale analysis. Use when hunting edge cases or stress-testing logic."
version: 2.0.0
---

# Edge Case Hunter v2

## Overview

Find everything that breaks before users do. **Benchmark-proven: without structured guidance, models find 3-4 edge cases. With the 8-dimension matrix, they find 12-15+ systematically.**

**Core principle:** IF YOU ONLY TEST THE HAPPY PATH, YOU ONLY SHIP BUGS.

## The Iron Laws

1. **Cover all 8 dimensions** — Every review must touch: Input, Concurrency, Network, Time, State, Scale, Integration, Human.
2. **Scenario→Expected→Actual format** — Every edge case must use this exact template. No exceptions.
3. **Always find the race condition** — If there's a read-then-write, there's a race. Find it and document it.
4. **Test at scale extremes** — 0, 1, max, max+1. Empty database. Full disk. 10,000 concurrent users.
5. **Idempotency is the first question** — "What happens if this is called twice?" Ask it for every operation.

## MANDATORY Output Schema

```markdown
# Edge Case Analysis: [Feature/Flow Name]

## Dimension 1: Input Extremes
### [ID] Scenario: [What the user/attacker does]
**Expected:** [What SHOULD happen]
**Actual:** [What ACTUALLY happens with current code]
**Severity:** [CRITICAL/HIGH/MEDIUM]
**Fix:** [Concrete fix]

## Dimension 2: Concurrency & Race Conditions
[Same format — minimum 2 race conditions found]

## Dimension 3: Network Failures
[Same format — timeout, partial response, connection drop]

## Dimension 4: Time & Timezone
[Same format — DST, leap seconds, clock skew, midnight boundary]

## Dimension 5: State Corruption
[Same format — out-of-order events, duplicate processing, rollback failures]

## Dimension 6: Scale Extremes
[Same format — 0 items, 1 item, 10K items, empty DB, full disk]

## Dimension 7: Integration Failures
[Same format — upstream down, downstream slow, webhook replay]

## Dimension 8: Human Errors
[Same format — copy-paste, wrong currency, fat-finger quantities]

## Edge Case Summary
- Total edge cases found: [count]
- CRITICAL: [count]
- HIGH: [count]
- MEDIUM: [count]
- Dimensions covered: [8/8]
```

## The 8-Dimension Matrix

### 1. Input Extremes
Empty string, null, undefined, max length+1, unicode (emoji, RTL, zero-width chars), SQL/HTML/JS in text fields, negative numbers where positive expected, float precision, special chars in names.

### 2. Concurrency & Race Conditions
Double-submit (click twice), simultaneous cancel+process, read-then-write without lock, optimistic concurrency without version check, queue worker picking up same job twice, distributed lock expiry during operation.

### 3. Network Failures
Timeout mid-response, TCP connection reset, DNS resolution failure, TLS handshake failure, partial response (chunked encoding cut off), slowloris-style slow clients, retry storm (all clients retry simultaneously).

### 4. Time & Timezone
DST transition (spring forward = missing hour, fall back = duplicate hour), leap seconds, NTP clock skew, midnight boundary (date change during operation), timezone mismatch (UTC vs local), timestamp format ambiguity (ISO 8601 vs Unix epoch vs RFC 2822).

### 5. State Corruption
Event arrives out of order, event arrives twice, event never arrives, state machine transition from invalid state, compensating transaction fails, rollback leaves partial state.

### 6. Scale Extremes
0 items (empty list, empty DB), 1 item (edge of pagination), exactly pagination boundary (e.g., 20 items when page size is 20), 10,000 items (memory, timeout), full disk (write fails), connection pool exhaustion.

### 7. Integration Failures
Upstream service returns 500, upstream returns success but with empty body, upstream slow (p99 latency), webhook delivered multiple times, webhook never delivered, API version mismatch, rate limited by upstream.

### 8. Human Errors
Copy-paste wrong ID, type "100" instead of "10", wrong currency (USD vs EUR), phone number with spaces/dashes/parentheses, address with special characters, name with apostrophe (O'Brien), negative quantity on refund.

## When to Use

- After test-engineer has written basic tests
- Before merging any PR that changes business logic
- When reviewing payment, order, or auth flows (high-risk)
- Before production deployment of new features

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for all naming, and respect the decisions recorded in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## Few-Shot Examples (MANDATORY Reference)

### ❌ BAD Output (Most common in benchmarks)

```markdown
## Edge Cases
- What if the API is down? → Show error message
- What if user clicks twice? → Disable button
```
**Why it's bad:** Only 2 out of 8 dimensions. No Scenario→Expected→Actual. No Severity. No Fix.

### ✅ GOOD Output (How it should be)

```markdown
## Dimension 2: Concurrency & Race Conditions

### EC-01: Double Cancel Race
**Scenario:** User opens two tabs, clicks "Cancel Order" in both within 100ms
**Expected:** First cancel succeeds (status→CANCELLED, refund triggers). Second cancel returns 409 "Order already cancelled".
**Actual:** Both requests read status=CONFIRMED before either writes. Both trigger refund. User gets double refund.
**Severity:** CRITICAL — financial loss (double refund)
**Fix:** Use optimistic locking: `UPDATE orders SET status='CANCELLED', version=version+1 WHERE id=? AND version=? AND status='CONFIRMED'`. Second update affects 0 rows → return 409.

### EC-02: Refund Failure During Cancel
**Scenario:** Cancel succeeds, but Stripe refund API returns 500
**Expected:** Order stays CANCELLED, refund is retried with exponential backoff, eventually succeeds or escalates to human.
**Actual:** Order is CANCELLED but refund never completes. Customer charged for cancelled order.
**Severity:** HIGH — customer experience + financial reconciliation
**Fix:** Use Outbox pattern: write refund_request to outbox table in same transaction as status update. Background worker processes outbox with retry. If refund fails after 3 retries, flag for manual review.

## Dimension 4: Time & Timezone

### EC-05: Midnight Boundary — Order Created at 23:59:59
**Scenario:** Order created at 23:59:59 UTC on Dec 31. Delivery ETA calculation adds 30 minutes → 00:29:59 Jan 1.
**Expected:** ETA correctly shows "Jan 1, 00:30". All date comparisons use the same day boundary.
**Actual:** Day boundary check (WHERE created_at::date = TODAY) excludes this order from "today's orders" report. Restaurant misses the order.
**Severity:** MEDIUM — reporting error
**Fix:** Use timestamp ranges instead of date casting: `WHERE created_at >= $1 AND created_at < $2` where $1 and $2 are explicit timestamps.
```

## Model-Specific Calibration

| Model | Tendency | Calibration |
|-------|---------|-------------|
| **Claude Sonnet 4** | Most comprehensive, naturally scans all dimensions but sometimes overly detailed | "Cover all 8 dimensions but keep each finding to 3-5 sentences maximum" |
| **GPT-4o** | Strong in Concurrency, tends to skip time/state dimensions | "Check Dimension 4 (Time) and Dimension 5 (State) SEPARATELY — GPT often skips these" |
| **Gemini 2.5 Pro** | Concise but to the point, accurate severity assignment | "For each dimension, find at minimum 2 distinct edge cases — not just one" |
| **DeepSeek V3** | Good in scale and integration dimensions, skips human errors | "Don't forget Dimension 8 (Human Errors) — copy-paste, fat-finger, wrong currency" |

## Decision Tree — Which Dimensions Apply

Use this before starting analysis to focus effort. All 8 dimensions still apply; this tree tells you which to treat as CRITICAL vs. DEFER.

```
What kind of operation is this?
│
├─ READ (query, report, list)
│   ├─ CRITICAL: Scale (#6: 0 items, huge result set), Input (#1: malformed filter/sort param)
│   ├─ HIGH:     Time (#4: report boundary, timezone), Integration (#7: upstream slow/down)
│   └─ DEFER:    Concurrency (#2) — reads rarely race; State (#5) — no mutation
│
├─ WRITE (create, update, delete, submit)
│   ├─ CRITICAL: Concurrency (#2: double-submit, race), State (#5: partial write, rollback)
│   ├─ CRITICAL: Input (#1: empty/null/overflow), Integration (#7: downstream failure)
│   ├─ HIGH:     Scale (#6), Human (#8: wrong ID pasted)
│   └─ HIGH:     Time (#4) — especially if write generates timestamps or deadlines
│
├─ LONG-RUNNING (job, export, migration, bulk)
│   ├─ CRITICAL: State (#5: checkpoint/resume, duplicate run), Scale (#6: OOM, timeout)
│   ├─ CRITICAL: Concurrency (#2: two workers pick same job)
│   ├─ HIGH:     Network (#3: partial failure mid-job), Time (#4: DST during overnight job)
│   └─ HIGH:     Integration (#7: upstream rate limit during batch)
│
└─ MONEY / AUTH (payment, refund, permission grant)
    ├─ CRITICAL: ALL 8 dimensions — no deferrals permitted
    ├─ CRITICAL: Concurrency (#2) — double-charge, double-refund
    ├─ CRITICAL: State (#5) — idempotency key, compensating transaction
    └─ CRITICAL: Integration (#7) — webhook replay, partial ACK from payment provider

Triage rule:
  CRITICAL  → block merge, fix before ship
  HIGH      → fix in same PR or file a tracked issue with owner+deadline
  MEDIUM    → file issue, add TODO comment in code, acceptable to defer
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I already know the edge cases for this feature, no need to go through the matrix"
- "The happy path works, ship it — we'll handle edge cases in the next sprint"
- "Race conditions aren't likely here, the load is low" — a race needs only two browser tabs
- "DST and timezone issues only matter for scheduling features" — every timestamp crosses a timezone
- "I found three edge cases — that's enough" — three means five dimensions were skipped
- "Integration failures are the upstream team's problem" — your service owns its fallback
- "Scale issues only matter after we grow" — 0-item and 1-item bugs exist at any traffic level
- "I tested the form with valid data, that covers it" — only testing the happy path ships bugs
- "Users won't do that" — users do exactly that, at the worst possible moment
- "Empty state is just cosmetic" — empty inputs and empty DB results are distinct failure surfaces
- "Concurrent access won't happen in this feature" — any stateful write has a race window

**ALL of these mean: STOP. Return to the relevant dimension in the matrix.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Low traffic means no concurrency issues" | A double-submit race needs only two browser tabs, not high load. |
| "We handle timezones correctly, DST isn't a concern" | DST creates duplicate hours and missing hours. Every timestamp operation needs explicit analysis. |
| "The happy path is tested, edge cases are minor" | Production incidents are almost always caused by the untested edge case, not the happy path. |
| "Three edge cases found is a good pass" | The 8-dimension matrix consistently surfaces 12–15 findings. Three means six dimensions were skipped. |
| "We'll add retry logic later, integration failures are rare" | Upstream services fail at the worst moments. Retry and idempotency must be designed in from the start. |
| "Only testing the happy path is fine for now" | The happy path is the one path that already works. Bugs live everywhere else. |
| "Users won't do that" | Users do exactly that. "Won't" is not a test. |
| "No empty/overflow handling needed — input is always valid" | The first production incident will be a null pointer on an empty string or an integer overflow on a large ID. |
| "Concurrent access isn't a concern here" | Any read-then-write sequence without a lock is a race condition waiting to be triggered. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "What happens if this is called twice?" — Idempotency was not analyzed
- "Did you check what happens at midnight?" — Time dimension was skipped
- "What if the payment webhook is delivered twice?" — State/Integration dimensions missed duplicate-event scenarios
- "What does the UI show while the request is in flight and then times out?" — Network failure dimension was not covered
- "We need the full analysis, not just the obvious cases" — Fewer than all 8 dimensions were covered

**When you see these:** STOP. Return to the 8-dimension matrix and work through each dimension systematically before continuing.

## Worked Example

See [`REFERENCE.md`](./REFERENCE.md) for a full application of the 8-dimension matrix to a **file upload** feature — 24 concrete edge cases in Scenario→Expected→Actual format, one per dimension cell.

## Related Skills

- **test-engineer** — basic tests come first; edge-case-hunter extends coverage after the baseline exists
- **security-reviewer** — security edge cases (injection, auth bypass, privilege escalation) overlap with Input and Human dimensions
- **backend-senior-engineer** — state machine design and transaction safety prevent many of the edge cases this skill finds
- **spec-first-development** — review the spec's acceptance criteria as the starting point for dimension analysis

## Verification Checklist

- [ ] All 8 dimensions covered (if a dimension is N/A, explain why)
- [ ] Every finding uses Scenario→Expected→Actual format
- [ ] At least 2 concurrency/race conditions found
- [ ] Idempotency checked for every mutating operation
- [ ] Scale extremes tested (0, 1, max, max+1)
- [ ] Time dimension covers DST, midnight, timezone mismatch
- [ ] Integration failures cover: down, slow, wrong response, duplicate event
- [ ] Edge Case Summary with counts and severity breakdown
