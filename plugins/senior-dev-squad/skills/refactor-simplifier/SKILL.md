---
name: refactor-simplifier
description: "Simplify after it works: remove clever code, duplication, dead abstraction. Use when reducing complexity in working code without changing behavior."
---

# Refactor Simplifier

## Overview

After code works and is tested, simplify. Remove cleverness, eliminate duplication, flatten abstractions. The best code is the code that isn't there.

**Core principle:** CLEVER CODE IS BUGS IN DISGUISE. THE SIMPLEST SOLUTION IS THE MOST MAINTAINABLE.

## The Iron Law

```
IF YOU NEED A COMMENT TO EXPLAIN WHAT IT DOES, THE CODE IS TOO COMPLEX
```

Rewrite it so the code speaks for itself.

## When to Use

**Use this when:**
- A feature is working and tests are passing, and you want to reduce future maintenance cost
- A code review surfaces readability concerns (deep nesting, cryptic variable names, duplicated logic)
- A module is being revisited for a new feature and the existing code is visibly complex

**Use this ESPECIALLY when:**
- A new team member cannot understand a function without a walkthrough
- The same logic appears in three or more places in the codebase
- A function takes a boolean parameter that changes its behavior entirely

**Don't skip when:**
- "We just need to ship" — complexity accumulates and becomes unmovable technical debt
- "It's working, don't touch it" — working code that nobody understands will break and nobody will be able to fix it
- "The original author knows what it means" — code is read far more often than it is written, by people who weren't the original author

## The 10 Simplifications

| # | Rule | Fix |
|---|------|-----|
| 1 | Nested ternaries > 1 level | Guard clauses or if/else |
| 2 | Short variable names (x, tmp) | Descriptive names |
| 3 | Method chaining > 3 calls | Intermediate variables |
| 4 | Dead code / commented code | Delete it |
| 5 | Duplication (3+ occurrences) | Extract function |
| 6 | Single-implementation interface | Remove abstraction |
| 7 | Deep nesting (> 3 levels) | Early returns |
| 8 | Magic numbers/strings | Named constants |
| 9 | Unnecessary variables | Inline |
| 10 | Boolean parameters | Options object |

## Red Flags — STOP

Clever code is not impressive — it's a future bug. "We might need this later" is YAGNI. Delete it. "I'll refactor next PR" = never. Refactor now.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's clever, it works" | Clever code works until it doesn't, then no one can fix it. |
| "We might need this abstraction" | Add it when you actually need it. Not before. |
| "Duplication is only in two places" | Two is the beginning of three. Extract now. |
| "I'll refactor it in the next PR" | You won't. Next PR adds more code on top. |



## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "I can't follow what this function does" — variable names are opaque or logic is too nested; simplify before continuing
- "Why are there three versions of this helper?" — duplication was not extracted; consolidate into a single function
- "This used to be simpler" — the refactor introduced new abstractions that weren't needed; revert the over-engineering
- "Can you add a comment explaining this?" — if a comment is needed, the code is too clever; rewrite it to be self-explanatory
- "What does `true` mean here?" — a boolean parameter is being used; replace with an options object or two explicit functions

**When you see these:** STOP. Apply the relevant simplification from the 10 rules before adding any new code.

## Verification

- [ ] No nested ternaries deeper than one level remain
- [ ] Every variable name describes what it holds (no `x`, `tmp`, `data`, `val`)
- [ ] No method chain longer than three calls without an intermediate variable
- [ ] All dead code and commented-out blocks deleted
- [ ] Logic duplicated in three or more places extracted into a named function
- [ ] No interface or abstract class with only one concrete implementation
- [ ] No function with nesting deeper than three levels (early returns applied)
- [ ] No magic numbers or magic strings — all replaced with named constants
- [ ] No boolean function parameters — replaced with options object or separate functions
- [ ] All simplifications verified against existing tests — no tests broken

## Related Skills

- **code-reviewer** — use before refactor-simplifier to identify which areas have the highest complexity burden
- **test-engineer** — run tests after each simplification step to confirm behavior is preserved
- **spec-first-development** — if simplification reveals ambiguous behavior, return to spec to clarify intent before rewriting
- **task-breaker** — use to split a large refactor across multiple atomic commits so each step is independently reviewable

## Output Schema (MANDATORY)

```markdown
# [Test Type]: [Target]
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

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Happy path only | Misses failures | Test error/edge/empty states |
| Vague scenarios | Not reproducible | Exact Given/When/Then |
| Missing severity | Can't prioritize | CRITICAL/HIGH/MEDIUM on every finding |
| "Fix later" | Never gets fixed | Concrete fix with every finding |
| Single dimension | Blind spots | Cover all categories systematically |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Coverage breadth | 1-2 dimensions | 4-6 | All categories |
| Scenario specificity | Vague | Partial | Exact Given/When/Then |
| Severity accuracy | None | Some | All correctly rated |
| Fix quality | "Fix it" | Partial | Complete fix |
| Reproducibility | Can't reproduce | Hard | Easy to reproduce |

**Pass: 8/10**
