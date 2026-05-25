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

## Decision Tree — Where Does This Test Live?

```
Does the test cross a process boundary (network, DB, filesystem, 3rd-party)?
├── YES → integration or e2e
│   └── Does it drive a real browser / full user journey?
│       ├── YES → e2e  (critical paths only — login, checkout, password reset)
│       └── NO  → integration  (API contract + DB, services talking to each other)
└── NO  → unit
    └── Is the logic a pure function / isolated component / util?
        ├── YES → unit (fast, no mocks needed)
        └── NO  → do you need to mock more than 1 collaborator to test it?
            ├── YES → design smell; consider splitting the unit first
            └── NO  → unit with a single controlled double

When NOT to write a test at all:
  - The behavior is already fully covered by a test one level up
  - The function is a trivial wrapper with no logic (e.g., re-exports, pass-throughs)
  - The test would be more complex than the code it tests and adds no safety
```

## Flaky Test Triage

A flaky test is a reliability tax on every engineer who runs the suite. Fix it the same sprint it appears; a retry is not a fix.

**Step 1 — Reproduce deterministically.** Run the test 20× in isolation (`--repeat=20`). If it never fails alone, it is order-dependent or shares state.

**Step 2 — Identify the root cause.**

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Fails only in CI | Clock/timezone drift or env var missing | Pin timezone; audit env |
| Fails when another test runs first | Shared mutable state (global, DB row, module cache) | `beforeEach` teardown; factory fixtures |
| Fails intermittently async | Assertion fires before async work settles | `await` the assertion; use `waitFor` not `setTimeout` |
| Fails on different port/network | Hard-coded port or real outbound call | Mock at the boundary; use dynamic ports |
| Fails only after file changes | Module cache not reset | `jest.resetModules()` in `afterEach` |

**Step 3 — Verify the fix.** Run 50× in CI before closing. If it still flips once: root cause is wrong, keep digging.

**Step 4 — Guard it.** Add a comment citing the root cause so the next engineer does not re-introduce it.

## Coverage That Matters

Line coverage tells you which lines were *executed*. It does not tell you whether your tests would catch a bug.

**Test behavior, not lines.** A test that calls a function but makes no assertion is a lie. `expect(fn()).toBeDefined()` exercises the line and proves nothing about correctness.

**Branch coverage is more honest.** A function with `if (user.isAdmin)` needs at least two tests — one where the flag is true and one where it is false. Aim for ≥ 70% branch coverage, not just line coverage.

**Mutation testing is the strongest signal.** Tools like [Stryker](https://stryker-mutator.io/) change one operator at a time (`>` → `>=`, `&&` → `||`) and check whether your tests catch the change. A mutant that survives means your tests do not actually enforce that logic. Target ≥ 60% mutation score on critical business logic.

**Why 100% line coverage can be misleading:**
- A test that calls every line with no assertions has 100% coverage and zero safety.
- Generated code, error-boundary boilerplate, and platform-specific branches inflate coverage without adding risk.
- Focus your coverage budget on: auth flows, payment logic, state machines, and all error branches.

## Worked Example — Password Reset Flow

See [`REFERENCE.md`](./REFERENCE.md) for a complete worked example showing exactly which tests to write at each pyramid level for the password reset feature, with annotated snippets and the rationale for each placement.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll write the tests after the code works"
- "This is too simple to test"
- "100% coverage means no bugs"
- "I'll skip the edge case test, it's unlikely"
- "The test passes on my machine, must be a CI issue"
- "I'll add the error test later"
- "This test is flaky but it passes most of the time"

**Testing-specific anti-patterns that also mean STOP:**
- **Testing implementation details** — asserting that `db.insert` was called instead of asserting the observable outcome; refactors break these tests without changing behavior
- **Over-mocking** — mocking 5 collaborators to test 1 function; if you mock everything, you test nothing
- **Snapshot-everything** — using snapshot tests on components with no behavioral assertions; snapshots catch diffs, not regressions
- **Asserting nothing** — `expect(fn()).toBeDefined()` or `expect(result).toBeTruthy()` — these pass on any non-null return and prove no contract

**ALL of these mean: STOP. The missing or broken test matters more than the next feature.**

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
| "I mocked everything, so it's isolated" | Mocking every dependency tests your mock configuration, not your code. |
| "The snapshot test covers the component" | Snapshots detect unexpected diffs; they do not assert that the component works correctly. |
| "I tested the internal state" | Implementation tests survive refactors without telling you if behavior broke — behavioral tests catch what internal tests miss. |

## Coverage Targets

| Level | Target | How to Measure |
|-------|--------|---------------|
| Line coverage | ≥ 80% | `nyc`, `c8`, `istanbul` |
| Branch coverage | ≥ 70% | Catches missing conditions |
| New code coverage | 100% | Every new line must be covered |
| Mutation score | ≥ 60% | `stryker` — tests kill mutants |

## Specialized Testing Techniques

Beyond the standard pyramid, reach for these when the situation demands it:

- **Mutation testing** — when you need to know if your tests would actually catch a bug (not just execute lines); run Stryker on critical modules to get a kill-rate score.
- **Visual regression** — when a UI component or page layout must not drift; use Percy, Chromatic, or Playwright snapshots to diff screenshots against an approved baseline.
- **Contract testing** — when two services or a mobile app + API must stay in sync across independent deploys; use Pact so consumers define what they need and providers verify it in CI.
- **Load & stress testing** — when you need to validate SLAs, find capacity limits, or catch resource leaks before a high-traffic event; use k6 or Locust with defined p95 latency and error-rate thresholds.

See [REFERENCE.md](REFERENCE.md) for mutation, visual-regression, contract, and load testing details.

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
