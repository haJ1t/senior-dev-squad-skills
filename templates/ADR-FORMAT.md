# ADR Format

An **Architecture Decision Record** captures one hard or irreversible decision and why. Store ADRs in `docs/adr/` named `NNNN-kebab-title.md` (zero-padded, sequential). ADRs are append-only: to reverse a decision, write a new ADR that supersedes the old one (don't edit history).

## Template

```md
# NNNN. <short decision title>

- Status: proposed | accepted | superseded by ADR-NNNN
- Date: YYYY-MM-DD
- Deciders: <names/roles>

## Context

The forces at play: the problem, constraints, and what makes this non-trivial.
State facts, not the decision yet.

## Decision

The choice made, in one or two clear sentences. "We will <X>."

## Consequences

- Positive: what gets better / easier.
- Negative: the cost, the tradeoff accepted, what gets harder.
- Follow-ups: anything that must now happen.

## Options considered (optional)

| Option | Pros | Cons | Why not chosen |
|--------|------|------|----------------|
```

## Rules

- **One decision per ADR.** If you're deciding two things, write two ADRs.
- **Write at decision time**, while the context is fresh (the `grill` skill does this inline).
- **Status is honest** — mark superseded ADRs, don't delete them.
- Keep it tight: context + decision + consequences is enough; skip ceremony.
