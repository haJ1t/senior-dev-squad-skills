---
name: user-story-refiner
description: "Transform raw ideas into production-ready user stories with INVEST validation, Given/When/Then, story splitting. Use when refining backlog items or writing user stories."
version: 1.0.0
platforms: [linux, macos]
---

# User Story Refiner

## What It Does
Transforms raw product ideas and feature requests into production-ready user stories that development teams can execute without ambiguity. Applies INVEST criteria validation, writes Given/When/Then acceptance criteria, enumerates edge cases systematically, splits oversized stories using SPIDR patterns, and identifies stories that require technical spikes before estimation.

## Iron Laws (NEVER violate)
1. **INVEST or reject** — Every story must be Independent, Negotiable, Valuable, Estimable, Small, Testable. Fail any → refine or split.
2. **Acceptance criteria before estimation** — No story is estimable until Given/When/Then acceptance criteria are written.
3. **One actor per story** — "As a [single role]" — never combine multiple user types in one story. Split by actor.
4. **Edge cases enumerated** — Every story must list edge cases (empty state, error state, concurrent access, boundary values) before it enters development.

## Red Flags (STOP immediately)
- **Epic disguised as story** — Story requires 3+ days of work → too large; split with SPIDR
- **No acceptance criteria** — "The team knows what to do" → recipe for rework and missed expectations
- **Technical task as user story** — "As a developer, I want to refactor the database" → not a user story; use technical task type
- **Ambiguous actor** — "As a user" when the system has admin, customer, and partner roles → needs role specificity

## Common Rationalizations (self-deception)
- "We'll figure out edge cases during development" → Unenumerated edge cases become production bugs. Find them now.
- "This story is simple, it doesn't need splitting" → "Simple" stories that take 5 days are epics in denial. Split ruthlessly.
- "The acceptance criteria is implied by the title" → Implied AC = different interpretations by different developers. Write it down.

## When To Use
- User provides a feature idea and wants it refined for development
- Grooming/refinement sessions for upcoming sprints
- Story is too large and needs splitting
- Acceptance criteria need to be formalized
- Identifying stories that need technical spikes

## Human Partner Signals (escalate to human)
- **Business rule ambiguity** — Acceptance criteria depends on a business rule that hasn't been decided → product owner call
- **Cross-team dependency** — Story requires work from a team outside the squad → coordination needed
- **UX undefined** — Story needs UI/interaction design that doesn't exist yet → design team involvement
- **Legal/compliance** — Story touches regulated data or processes → compliance review

## Pipeline
1. Capture: receive raw idea/feature request in any format (bullet points, paragraph, ticket)
2. Structure: format as user story — "As a [role], I want [capability], so that [value]"
3. Validate: check INVEST criteria; flag failures for splitting or clarification
4. Acceptance: write Given/When/Then scenarios covering happy path, error path, and edge cases
5. Enumerate: systematically list edge cases (empty, error, boundary, concurrent, permission, data type)
6. Split: apply SPIDR if story is too large — Spike, Path, Interface, Data, Rules
7. Spike check: identify stories that need technical investigation before estimation
8. Ready: story meets Definition of Ready and can enter sprint

## Verification Checklist
- [ ] INVEST criteria passed for every story (no failures without documented reason)
- [ ] Given/When/Then acceptance criteria cover happy path + error path + 3+ edge cases
- [ ] Actor is specific (not generic "user")
- [ ] Story is small enough for single-sprint completion (≤3 days estimated)
- [ ] Edge case list includes: empty state, error state, boundary values, concurrent access
- [ ] Spike stories identified and separated from implementation stories



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
## Related Skills
- `spec-first-development` — User stories are the spec format for implementation
- `test-engineer` — Acceptance criteria become test cases
- `edge-case-hunter` — Edge case methodology applied specifically to stories
- `roadmap-prioritizer` — Prioritized initiatives become refined stories
