# CONTEXT.md Format

`CONTEXT.md` is a project's **ubiquitous-language glossary** plus squad config. It lets skills decode project jargon and adapt to the team's setup. Keep it short and high-signal — terms only the project defines, not general programming concepts.

Place it at the repo root. For multi-context (large) repos, add a root `CONTEXT-MAP.md` pointing to per-area `CONTEXT.md` files.

## Recommended shape

```md
# Context: <project name>

One or two sentences on what this project is and its domain.

## Glossary

| Term | Definition | Notes / aliases |
|------|------------|-----------------|
| Materialization | Giving a draft lesson a real filesystem path | aka "making real" |
| Cancellation | Voiding an unfulfilled order (NOT a refund) | refund = separate flow |

## Domain rules

- Short, durable invariants. e.g. "An Order has exactly one Customer."

## Squad Config

- issue-tracker: github            # github | gitlab | linear | local
- triage-labels: [bug, feature, chore, p0, p1, p2]
- docs: { context: CONTEXT.md, adr: docs/adr/, specs: docs/specs/ }
```

## Rules

- **Create lazily** — add a term the first time it needs resolving, not upfront.
- **One canonical term per concept.** When two words mean the same thing, pick one; list the other as an alias.
- **No general-knowledge entries** ("REST", "index") — only project-specific meaning.
- Skills (`grill`, `spec-first-development`, etc.) read the Glossary for naming and the Squad Config for behavior.
