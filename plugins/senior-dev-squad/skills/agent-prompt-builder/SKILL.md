---
name: agent-prompt-builder
description: "Spec-to-prompt synthesis, single-shot agent prompt, self-contained instructions, task decomposition. Use when building a prompt to dispatch a sub-agent."
---

# Agent Prompt Builder

## Overview

Synthesize all planning documents into a single, self-contained prompt that a coding agent can execute from start to finish. The prompt must include everything the agent needs — no external context, no assumptions, no missing pieces.

**Core principle:** THE PROMPT MUST BE COMPLETELY SELF-CONTAINED. ZERO EXTERNAL CONTEXT REQUIRED.

## The Iron Law

```
A PROMPT IS NOT READY UNTIL AN AGENT CAN BUILD THE ENTIRE PROJECT FROM IT WITHOUT ASKING A SINGLE QUESTION
```

If the agent would need to ask something, the prompt is incomplete.

## When to Use

**Use this when:**
- Spec + implementation plan + tasks are complete
- User wants a "single command to build everything"
- Before handing off to a coding agent (Claude Code, Codex, etc.)
- After task-breaker has produced ordered tasks

## Prompt Structure

```
# PROJECT: [Name]

## Overview
[2-3 sentence elevator pitch]

## Tech Stack
- Runtime: [Node 22, Python 3.12, Go 1.22, ...]
- Framework: [Next.js 14, FastAPI, Gin, ...]
- Database: [PostgreSQL 16, SQLite, ...]
- Key packages: [specific versions]

## Architecture
[2-3 sentence architecture description]

## Directory Structure
```
project-root/
├── src/
│   ├── api/         ← REST endpoints
│   ├── core/        ← Business logic
│   ├── db/          ← Database layer
│   └── ui/          ← Components
├── tests/
├── Dockerfile
├── package.json
└── README.md
```

## Data Model
[Key entities with fields and types]

## API Contract
[Key endpoints with request/response shapes]

## Implementation Steps (Checklist)

- [ ] Step 1: Initialize project, install dependencies
- [ ] Step 2: Set up database schema and migrations
- [ ] Step 3: Implement core business logic
...
- [ ] Step N: Final verification and README

Each step must include:
- Exact files to create/modify
- Key code patterns (signatures, types, structural examples)
- Verification method (test command, manual check)

## Key Code Patterns

```typescript
// Critical pattern examples inline:
// - Auth middleware
// - Error handling
// - Database queries
// - API handlers
```

## Verification

Before marking prompt complete, verify:
- [ ] Agent can run without asking questions
- [ ] All dependencies have specific versions
- [ ] All file paths are exact
- [ ] All code patterns are COMPLETE (not placeholders)
- [ ] Test/verify command after every step
- [ ] Commit messages specified
```

## Red Flags

Any "TBD", "TODO", "fill in later" in the prompt. Any missing version number. Any assumption about the agent's environment. Any "similar to above" without repeating the pattern.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The agent will figure out the version from the package.json" | The agent doesn't have your package.json. Omitting a version number is a silent assumption that breaks builds. |
| "This pattern is obvious from context" | Agents produce hallucinated boilerplate when patterns are not explicit. Obvious to you means ambiguous to the agent. |
| "I'll clean up the TBDs before running it" | You won't. The agent will encounter the TBD mid-execution, guess, and produce wrong code you'll spend hours tracing. |
| "The architecture is in a separate doc the agent can read" | The prompt must be self-contained. External references are context the agent will not reliably retrieve or interpret correctly. |
| "A detailed prompt will confuse the agent" | Agents do not get confused by specificity. They get confused by ambiguity. More precision always beats less. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "The agent asked me what framework to use" — The tech stack section is missing or underspecified.
- "It built the whole thing but in the wrong directory structure" — The directory layout was described but not enforced with exact paths per task step.
- "Half the tests are failing because of import paths" — Code pattern examples were incomplete or omitted, so the agent improvised conventions.
- "It used a different auth pattern than we use everywhere else" — The key code patterns section was absent or too brief to be authoritative.
- "The agent stopped mid-way and said it needed more context" — Dependencies between steps were not explicit, leaving the agent unable to proceed without external information.

**When you see these:** STOP. Return to the prompt, identify which section is ambiguous or missing, add concrete specifics, and re-run the verification checklist before handing off again.

## Related Skills

- **spec-first-development** → spec to summarize
- **architecture-planner** → architecture to describe
- **task-breaker** → tasks to include as checklist

## Verification

- [ ] Every dependency has a specific version
- [ ] Every file path is exact
- [ ] No "TBD" or "TODO" remain
- [ ] Code patterns are complete (not stubs)
- [ ] Verification method after every step
