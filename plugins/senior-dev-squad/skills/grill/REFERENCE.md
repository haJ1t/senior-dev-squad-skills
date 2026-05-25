# Grill — Reference: Requirements Elicitation & User Stories

This reference covers two extended modes that grill now absorbs: **structured project discovery** (run before grilling when the project is new or vague) and **INVEST user-story refinement** (run after grilling to harden the stories that surfaced during the interview).

---

## Part 1 — Structured Project Discovery

Use this when a new project or feature arrives with little context and you need enough shape to ask intelligent grill questions. Complete these steps *before* the main interview loop; the answers become the seed for your first grill question.

### The 8-Step Discovery Flow

Run adaptively — not every step is needed for every project (see the matrix below).

**Step 1 — Project Identity** (always ask)

Ask the user to describe what they want to build in a few sentences. Then clarify:
- What type? Web Application / CLI or Library / API or Backend / Mobile or Desktop
- What scope? MVP or PoC / Full Product v1.0 / Enterprise System

**Step 2 — Technical Direction** (always ask)

- Language/framework preference known? Yes / Help me choose / No preference
- If "Help me choose" → invoke `tech-stack-advisor` before continuing

**Step 3 — Data & Storage** (ask for most projects)

- Need a database? Relational (SQL) / Document (NoSQL) / Help me choose / No or File-based

**Step 4 — Features & Scope** (always ask)

- What are the 3–5 core features?
- Need auth? Full auth / API keys only / No auth / Undecided
- Need a UI? Web UI / CLI / Desktop / No UI (API only)

**Step 5 — Architecture Preferences** (medium+ projects)

- API style? REST / GraphQL / gRPC / Multiple / No API
- Need real-time? Yes (WebSocket/SSE) / No / Maybe later

**Step 6 — Operations** (medium+ projects)

- How will users get this? Docker / Single binary / Package manager / Cloud-hosted
- CI/CD from day one? Full pipeline / Basic (lint + test) / Not yet

**Step 7 — Scale** (larger projects)

- Expected launch scale? <100 users / 100–10K / 10K–100K / 100K+ / Unknown

**Step 8 — Project Meta** (when engaged)

- Open source? Fully open / Open-core / Proprietary / Undecided
- Team size? Solo / Small team (2–5) / Larger team (5+)

### Adaptive Questioning Matrix

| User Input Style | Steps to Run |
|---|---|
| 1-liner ("I want to build X") | Steps 1–5 fully; 6–8 selectively |
| Detailed 3+ paragraph brief | Gaps in Steps 1–3 only |
| "Help me with everything" | All steps, all tiers |
| Uploads existing doc | Extract answers, ask only gaps |
| "You decide" | Choose safe default; state it clearly |

### Discovery Verification

Before moving to the main grill interview, confirm:
- [ ] Project type known (web, CLI, API, mobile, desktop)
- [ ] Scope defined (MVP, v1.0, enterprise)
- [ ] Tech direction established (or `tech-stack-advisor` invoked)
- [ ] Three core features identified
- [ ] Auth + UI decisions made
- [ ] User has approved proceeding to the interview phase

---

## Part 2 — INVEST User-Story Refinement

After grilling surfaces what the user wants, transform the raw ideas into production-ready user stories that a development team can execute without ambiguity.

### Iron Laws (never violate)

1. **INVEST or reject** — every story must be Independent, Negotiable, Valuable, Estimable, Small, Testable. Fail any criterion → refine or split.
2. **Acceptance criteria before estimation** — no story is estimable until Given/When/Then scenarios are written.
3. **One actor per story** — "As a [single role]" — never combine multiple user types in one story; split by actor.
4. **Edge cases enumerated** — every story must list edge cases (empty state, error state, concurrent access, boundary values) before it enters development.

### INVEST Criteria Definitions

| Letter | Criterion | Test |
|---|---|---|
| I | Independent | Can be built without depending on another story in the same sprint? |
| N | Negotiable | Scope can flex within the stated value; not a rigid contract? |
| V | Valuable | Delivers value to a real user or business goal on its own? |
| E | Estimable | Team can produce a rough size estimate? |
| S | Small | Can be completed in ≤ 3 days estimated effort? |
| T | Testable | Has objectively verifiable acceptance criteria? |

### The Refinement Pipeline

1. **Capture** — receive the raw idea in any format (bullet, paragraph, ticket)
2. **Structure** — format as: *"As a [role], I want [capability], so that [value]"*
3. **Validate** — check INVEST; flag failures for splitting or clarification
4. **Acceptance** — write Given/When/Then scenarios: happy path, error path, edge cases
5. **Enumerate** — systematically list edge cases: empty state, error state, boundary values, concurrent access, permission boundaries, unexpected data types
6. **Split** — apply SPIDR if the story is too large (see below)
7. **Spike check** — identify stories that need technical investigation before estimation; separate spike stories from implementation stories
8. **Ready** — story meets Definition of Ready and can enter sprint

### Given/When/Then Format

```
Given [context / precondition]
When  [actor takes an action]
Then  [observable outcome]
```

Write at minimum: one happy-path scenario, one error-path scenario, and three or more edge-case scenarios per story.

### SPIDR Story-Splitting Patterns

Use when a story fails the S (Small) criterion.

| Letter | Pattern | How to split |
|---|---|---|
| S | Spike | Extract the unknown into a time-boxed investigation story; implement separately |
| P | Path | Split by user workflow paths (happy path story / error path story / edge path story) |
| I | Interface | Split by UI layer — deliver backend story first, frontend story second |
| D | Data | Split by data variation — one story per distinct data type or input category |
| R | Rules | Split by business rule — one story per distinct rule or permission tier |

### Red Flags — STOP

- **Epic disguised as story** — story requires 3+ days → split with SPIDR
- **No acceptance criteria** — "the team knows what to do" → recipe for rework
- **Technical task as user story** — "As a developer, I want to refactor the DB" → use a technical task type, not a story format
- **Ambiguous actor** — "As a user" when the system has admin, customer, and partner roles → needs role specificity

### Refinement Verification Checklist

- [ ] INVEST criteria passed for every story (no failures without documented reason)
- [ ] Given/When/Then scenarios cover happy path + error path + 3+ edge cases
- [ ] Actor is specific (not generic "user")
- [ ] Story is small enough for single-sprint completion (≤ 3 days estimated)
- [ ] Edge case list includes: empty state, error state, boundary values, concurrent access
- [ ] Spike stories identified and separated from implementation stories
