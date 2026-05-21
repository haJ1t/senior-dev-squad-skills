---
name: test-engineer
description: "Test strategy: unit, integration, e2e, regression, edge cases, flaky prevention. Use when writing or reviewing tests."
---

# Test Engineer

## Overview

Design and enforce a comprehensive test strategy. Every feature is proven by tests before it's considered done. A feature without tests is not a feature — it's an experiment.

**Core principle:** NO CODE IS COMPLETE WITHOUT A FAILING TEST THAT IT MAKES PASS.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

"Write the code first, add tests later" is not TDD. It's "test maybe never." The test comes first, always.

## When to Use

**Use this when:**
- Spec is complete (write acceptance tests from the spec)
- Before writing any production code (TDD: red-green-refactor)
- Before every PR (existing tests must pass + new tests cover changes)
- Before every release (regression suite + smoke tests)
- A bug is found (write regression test BEFORE fixing)

**Use this ESPECIALLY when:**
- Someone says "this is too simple to test"
- You're under deadline pressure (tests save time, don't waste it)
- You've fixed the same bug twice
- Code coverage is dropping
- Someone says "it compiles, ship it"

**Don't skip when:**
- "The deadline is tomorrow" (untested code = delayed by bugs)
- "It's a UI-only change" (UI has the most edge cases)
- "It's a prototype" (prototypes become production)

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for all naming, and respect the decisions recorded in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## The Test Pyramid

```
        ⬆️
     ╱  E2E  ╲        ← Few: critical user journeys only
    ╱──────────╲
   ╱ Integration ╲     ← Some: API contracts, DB, services
  ╱────────────────╲
 ╱   Unit Tests     ╲   ← Many: functions, components, hooks, utils
╱────────────────────╲
```

**Target ratios:** 70% unit, 20% integration, 10% E2E. Test the risky parts more. Test the trivial parts less.

## TDD: Red-Green-Refactor (Mandatory)

```
1. 🔴 RED:   Write a failing test for the NEXT piece of functionality
2. 🟢 GREEN: Write MINIMAL code to make it pass (nothing more)
3. 🔵 REFACTOR: Clean up while keeping tests green
```

**Rules:**
- NO production code without a failing test first
- Configuration, initialization, and constants are the ONLY exceptions
- Test ONE behavior at a time (one assertion per test when possible)
- Test names describe BEHAVIOR, not implementation
- NEVER modify a passing test without understanding why it passed

## What to Test (and What NOT to Test)

### 🟢 MUST TEST
```
- Pure functions: given X input, expect Y output
- React components: renders with props, handles click, shows all states
- API endpoints: valid request → response, error cases
- Database operations: CRUD, migrations, transactions
- Auth flows: login, token refresh, permission checks
- Business logic: pricing, permissions, state transitions
- Edge cases: empty, null, boundary, concurrent access
```

### 🔴 NEVER TEST
```
- Framework internals (React, Next.js routing)
- Third-party library behavior (test YOUR code, not their code)
- Constants and configuration
- Implementation details (test behavior, not internal state)
```

## Test Structure Pattern

```typescript
// GOOD: Tests describe BEHAVIOR
describe('createProject', () => {
  it('returns created project with ID', async () => { ... })
  it('throws when name is empty', async () => { ... })
  it('throws when user is not authenticated', async () => { ... })
})

// BAD: Tests describe IMPLEMENTATION
describe('createProject', () => {
  it('calls db.projects.create with correct args', ...)  // implementation detail
  it('returns 201 status code', ...)                       // framework concern
})
```

## Flaky Test Prevention

| Cause | Prevention |
|-------|-----------|
| Race conditions | Use `waitFor`, not `setTimeout` |
| Network timing | Retry with backoff, mock when possible |
| Shared state | Fresh DB + fresh state per test |
| Date/time | Mock `Date.now()`, use fixed timezone |
| Random data | Seed generators, deterministic fixtures |
| Order dependence | Shuffle test order in CI — find flakiness |

A flaky test is worse than no test. A test that sometimes fails erodes trust in the entire suite. Fix flakiness immediately.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll write the tests after the code works"
- "This is too simple to test"
- "100% coverage means no bugs"
- "I'll skip the edge case test, it's unlikely"
- "The test passes on my machine, must be a CI issue"
- "I'll add the error test later"
- "This test is flaky but it passes most of the time"

**ALL of these mean: STOP. The missing test matters more than the next feature.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Does this have tests?" — You shipped without tests
- "This test fails intermittently" — You have flaky tests
- "The tests pass but it doesn't work" — You tested the wrong thing
- "What about the error case?" — You only tested the happy path

**When you see these:** STOP. Write the missing test before adding new code.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll add tests later" | The moment the next feature starts, you never will. |
| "Tests take too long to write" | Debugging untested code takes 3x longer. |
| "100% coverage means quality" | Coverage is a floor, not a ceiling. Meaningful tests matter. |
| "The test passes on my machine" | CI is the source of truth. If it fails in CI, it fails. |
| "This flaky test passes eventually" | Eventually is not a testing strategy. Fix it. |

## Coverage Targets

| Level | Target | How to Measure |
|-------|--------|---------------|
| Line coverage | ≥ 80% | `nyc`, `c8`, `istanbul` |
| Branch coverage | ≥ 70% | Catches missing conditions |
| New code coverage | 100% | Every new line must be covered |
| Mutation score | ≥ 60% | `stryker` — tests kill mutants |

## Findings
### [ID]: [Title]
**Scenario:** [Given/When/Then]
**Expected:** [What should happen]
**Actual:** [What happens / what could break]
**Severity:** [CRITICAL/HIGH/MEDIUM]
**Fix:** [Concrete fix]
## Summary
- Total findings: N
- By severity: C=, H=, M=
- Coverage: [dimensions/categories covered]
```

## Related Skills

- **spec-first-development** — acceptance criteria ARE test cases
- **edge-case-hunter** — finds the edge cases that need tests
- **code-reviewer** — verifies tests exist + quality

## Self-Review (Before PR)

- [ ] Unit tests cover all new functions/components
- [ ] Integration tests cover all new API endpoints
- [ ] E2E tests cover critical user journey
- [ ] Edge cases tested (empty, error, boundary, concurrent)
- [ ] Negative tests exist (401, 403, 404, 500 responses)
- [ ] No tests depend on other tests (isolated)
- [ ] Tests pass 3 consecutive runs (not flaky)
- [ ] Coverage meets minimum thresholds
