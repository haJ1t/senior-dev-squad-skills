---
name: instincts-guardrails
description: "Always-on guardrails — context management, git hygiene, memory preservation, quality gates, and security boundaries. Use when enforcing safe coding practices."
---

# Instincts Guardrails

## Overview

Inspired by ECC's "Instinct System," this skill is *never manually invoked* — it consists of always-on automatic guardrails that execute at every step. Much like a pilot's cockpit alarms, they run in the background as you work: monitoring the context window, enforcing git discipline, logging decisions to memory, auditing quality standards, and warning you before destructive operations. These guardrails cannot be bypassed, disabled, or negotiated.

**Core Principle:** Guardrails are not suggestions; they are absolute mandates. They are never disabled under pressure.

## The Iron Law

```
NO STEP, NO OPERATION, NO DECISION CAN PROCEED WITHOUT THE APPROVAL OF THESE GUARDRAILS.
AUTOMATIC GUARDRAILS CAN NEVER BE BYPASSED — THEY MUST ONLY BE OBSERVED AND SOLVED.
```

## When to Use

**These are ALWAYS active (run automatically, not manually invoked) during:**

- Before every terminal command (context window check)
- Before every git commit (commit message, branch name, staged files check)
- Before every memory consolidation (automatic logging to decision log)
- Before every code submission (lint, test, security scan)
- Before every destructive operation (deleting, moving, permission changes)
- At the start of every session (load previous state, resume where left off)
- On every token limit threshold breach (warn, pause, redirect)

**ESPECIALLY active when:**

- Under time pressure — when the temptation to take shortcuts is highest.
- During complex multi-file edits — when the risk of context overflow is highest.
- Late at night or when fatigued — when attention drift is highest.
- During session recovery/restart scenarios — when previous state might be lost.

**NEVER bypassed when:**

- You say "this is a small change"
- You say "it's urgent, I'll fix it later"
- You say "it's only one file, why test it"

## Guardrail Phases (Summary)

Eight automatic phases run continuously. See [REFERENCE.md](REFERENCE.md) for the full step-by-step procedures and bash examples for each phase.

**Phase 1 — Context Window Management:** Checks token usage before every operation; issues YELLOW WARNING at 70% and RED STOP at 85%, triggering memory consolidation.

**Phase 2 — Git Hygiene Audit:** Runs before any `git commit` or `git push`; validates commit message format, branch naming, staged file safety, and absence of merge conflict markers.

**Phase 3 — Memory Preservation and Consolidation:** Triggered before context compression or session closure; writes critical decisions to `decision-log.md` and saves phase state to `session-state.md`.

**Phase 4 — Quality Gates:** Runs after every code change and before committing; executes lint, test, and security scan in sequence; blocks commit on any failure.

**Phase 5 — Security Boundaries:** Triggered before destructive operations (`rm -rf`, `git reset --hard`, `DROP TABLE`, bulk deletes, etc.); defines blast radius, requires explicit YES confirmation, and checks backup status.

**Phase 6 — Session Recovery:** Runs at the start of every session; loads `session-state.md`, reads the last 10 decisions from `decision-log.md`, and resumes at the last active phase.

**Phase 7 — Token Budget Tracking:** Assigns 4 000 tokens per phase; warns at 80% consumption and stops at 100%; reports usage at phase end.

**Phase 8 — Final Verification:** Confirms all guardrails passed before marking a session complete (checklist below).

## Red Flags — STOP and Observe the Process

If you catch yourself thinking:

- "This commit is too small, no need for lint/test"
- "Context window is full but it's fine, let's keep going"
- "Just a quick `rm -rf`, no need to ask for confirmation"
- "Token budget is not an issue, the task is almost done"
- "No need to record this decision, I'll remember it"
- "Branch naming standard doesn't matter, this is a one-off"
- "No need to load the previous session state, I'll just restart"

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Warning Signals

**Watch for these redirections:**

- "Didn't you test this before committing?" — You bypassed the quality gate.
- "Take a look at the commit message" — You bypassed the git hygiene audit.
- "We talked about this before" — You forgot to write to the decision log.
- "Why didn't you ask for permission to delete this file?" — You bypassed the security boundary.
- "Where did we leave off?" — You bypassed session recovery.
- "Watch the token limit" — You bypassed context window management.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This is a small change, no need for guardrails" | Small changes hide the biggest mistakes. |
| "I don't have time, I'll do it later" | There is no "later" — guardrails save time in the long run. |
| "Context window is full but I am fine" | Context overflow is the most common source of mistakes. |
| "No need to record this decision, it's in my head" | Human memory is unreliable; written decisions are permanent. |
| "Branch naming standard is just a formality" | Standards are the foundation of teamwork; there are no formalities. |
| "Force pushing is fine, I am the only developer" | Force pushing is always risky; confirmation is mandatory. |
| "Token budget slows me down" | The budget doesn't slow you down; it guides you smart. |
| "Session recovery is a waste of time" | Continuing where you left off is faster than starting from scratch. |

## Related Skills

- **context-compass** — When manual strategies are needed for context management.
- **decision-log** — When manual entries are needed in the decision log.
- **git-hygiene** — For detailed manual audits of git standards.
- **quality-gates** — To customize or extend quality gates.
- **memory-mesh** — For manual management of cross-session memory.
- **safe-operations** — For sensitive but non-destructive operations.

## Verification

After completing the process for this skill:

1. **Coverage Check:** Did all guardrails run at every step? None bypassed?
2. **Edge Case Check:** Were unexpected scenarios (e.g., context explosion, secret leak) handled correctly?
3. **Quality Check:** Does the output meet the standard of the Iron Law — no guardrail is negotiable?
4. **Retrospective Check:** Did you bypass any guardrail this session? If so, why and how will you fix it?
5. **Improvement Check:** Can the guardrails themselves be improved? Should a new guardrail be added?

Final checklist before marking complete:

- [ ] Is the context window below 85% capacity?
- [ ] Does the git branch name follow the standard?
- [ ] Is the latest commit message in the correct format?
- [ ] Is the decision log up to date?
- [ ] Did all quality gates (lint, test, security) pass?
- [ ] Are there zero leaks of secrets or API keys?
- [ ] Was the session state saved (`session-state.md`)?
- [ ] Is the token budget within bounds?
- [ ] Were destructive operations confirmed?
- [ ] Has the cross-session memory been updated?
