---
name: project-discovery
description: "Interactive project elicitation: 8-step question flow to extract requirements before any design. Use when gathering requirements for a new project or feature."
---

# Project Discovery

## Overview

Before any specification, architecture, or code — understand the project through structured conversation. This skill extracts requirements systematically so every subsequent document has a solid foundation.

**Core principle:** A SPEC BUILT ON GUESSES IS WORSE THAN NO SPEC AT ALL.

## The Iron Law

```
NEVER GENERATE A DOCUMENT WITHOUT COMPLETING THE DISCOVERY FLOW FIRST
```

Skip discovery = build the wrong thing. Every time.

## When to Use

**Use this when:**
- User says "I want to build X" with any level of detail
- Before spec-first-development (this skill feeds into it)
- Before tech-stack-advisor (needs project type + scope)
- Before any planning or architecture work

**Use this ESPECIALLY when:**
- User gives a vague 1-liner ("build me a todo app")
- User says "you decide" on everything
- User uploads an existing doc (extract what's already said)
- User seems unsure about tech choices

**Don't skip when:**
- "The requirements are obvious" (they're not)
- "The user already told me everything" (they didn't)
- "I know what this project looks like" (you don't)

## Discovery Flow (8 Steps)

### Step 1: Project Identity — always ask

```
Freeform: "Describe what you want to build in a few sentences."

Then:
AskUserQuestion: What type of project?
  ["Web Application", "CLI / Library", "API / Backend", "Mobile / Desktop App"]

AskUserQuestion: What's the scope?
  ["MVP / PoC", "Full Product v1.0", "Enterprise System"]
```

### Step 2: Technical Direction — always ask

```
AskUserQuestion: Language preference?
  ["Yes, I know", "Help me choose", "No preference"]

If "Help me choose" → run tech-stack-advisor skill
```

### Step 3: Data & Storage — ask for most projects

```
AskUserQuestion: Need a database?
  ["Relational (SQL)", "Document (NoSQL)", "Help me choose", "No / File-based"]
```

### Step 4: Features & Scope — always ask

```
Freeform: "What are the 3-5 core features?"

AskUserQuestion: Need auth?
  ["Full auth", "API keys only", "No auth", "Undecided"]

AskUserQuestion: Need a UI?
  ["Web UI", "CLI", "Desktop", "No UI (API only)"]
```

### Step 5: Architecture Preferences — ask for medium+ projects

```
AskUserQuestion: API style?
  ["REST", "GraphQL", "gRPC", "Multiple", "No API"]

AskUserQuestion: Need real-time?
  ["Yes (WebSocket/SSE)", "No", "Maybe later"]
```

### Step 6: Operations — ask for medium+ projects

```
AskUserQuestion: How will users get this?
  ["Docker", "Single binary", "Package manager", "Cloud-hosted"]

AskUserQuestion: CI/CD from day one?
  ["Full pipeline", "Basic (lint+test)", "Not yet"]
```

### Step 7: Scale — ask for larger projects

```
AskUserQuestion: Expected launch scale?
  ["<100 users", "100-10K", "10K-100K", "100K+", "Unknown"]
```

### Step 8: Project Meta — ask when engaged

```
AskUserQuestion: Open source?
  ["Fully open", "Open-core", "Proprietary", "Undecided"]

AskUserQuestion: Team size?
  ["Solo", "Small team (2-5)", "Larger team (5+)"]
```

## Adaptive Questioning Matrix

| User Input | Questions to Ask |
|-----------|-----------------|
| "I want to build X" (1 line) | Steps 1-5 fully, 6-8 selectively |
| Detailed 3+ paragraph brief | Gaps in Steps 1-3 only |
| "Help me with everything" | All steps, all tiers |
| Uploads existing doc | Extract answers, ask only gaps |
| "You decide" | Choose safe default, state it clearly |

## Red Flags — STOP

"Asking questions wastes time" — a 5-minute discovery saves 5 hours of wrong implementation.
"I already know what they want" — no you don't. Ask.
"Skip discovery, just build it" — you'll build the wrong thing.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The user already explained it" | They told you the solution, not the problem. |
| "Discovery takes too long" | 5 questions now vs 50 bug reports later. |
| "I know this project type" | Every project has unique constraints. |
| "The user will correct me" | Users validate, they don't design. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "You're assuming too much" — You skipped asking and filled gaps with guesses instead of questions
- "That's not what I want at all" — You proceeded to generate a document without completing the discovery flow
- "Can we back up?" — You advanced to spec or architecture before validating the discovery output
- "I already said that" — You asked a question already answered in the user's initial message; re-read before asking
- "Why are you asking about deployment already?" — You jumped ahead in the step sequence without confirming earlier steps

**When you see these:** STOP. Return to Step 1 and re-run only the steps whose answers are missing or unvalidated.

## 1. Components/Contexts
[Table: Name | Responsibility | Data | Dependencies]
## 2. Decisions (ADR format)
### ADR-001: [Title]
**Context:** [Why] **Options:** [2+ alternatives] **Decision:** [What] **Tradeoffs:** [+gain / -sacrifice]
## 3. Communication Matrix
[Table: From→To | Pattern | Protocol | Timeout | Retry]
## 4. Data & CAP Analysis
[Per store: Type | CP/AP | Partition behavior]
## 5. Deployment Topology
[ASCII diagram]
## Verdict: READY / NEEDS CLARIFICATION
```

## Related Skills

- **tech-stack-advisor** — run after discovery if user needs help choosing
- **spec-first-development** — uses discovery output to write spec
- **architecture-planner** — needs discovery for design decisions

## Verification

Before proceeding:
- [ ] Project type known (web, CLI, API, mobile, desktop)
- [ ] Scope defined (MVP, v1.0, enterprise)
- [ ] Tech direction established (or "help me choose" invoked)
- [ ] Three core features identified
- [ ] Auth + UI decisions made
- [ ] User has approved proceeding to next skill
