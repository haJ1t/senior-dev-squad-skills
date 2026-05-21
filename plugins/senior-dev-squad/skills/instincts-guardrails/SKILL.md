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

## Phase 1: Context Window Management (Automatic)

Runs before the terminal output at every step.

**BEFORE every operation:**

1. **Check token usage** — Retrieve current token count, calculate limits.
2. **Check 70% threshold** — If the context is 70% or more full, display a **YELLOW WARNING**:
   - "Your context window is at 70% capacity. Consider cleaning up unnecessary output."
   - Provide options to truncate/split output (e.g., filter with `grep`, cut with `head`).
3. **Check 85% threshold** — If the context is 85% or more full, trigger a **RED STOP**:
   - Pause all operations.
   - Notify the user: "Your context window is at 85% capacity. Memory consolidation is required before continuing."
   - Initiate the memory consolidation workflow (Phase 3).
4. **Track phase-based token budget** — Update the token budget allocated for each phase, warn on budget overruns.

```bash
# Context status check (automatic, at each step)
TOKEN_USAGE=$(some_token_check_command)  # if available
if [ "$TOKEN_USAGE" -gt 85 ]; then
  echo "[RED STOP] Context window is at 85% capacity — memory consolidation is required"
  # -> Redirect to Phase 3
elif [ "$TOKEN_USAGE" -gt 70 ]; then
  echo "[YELLOW WARNING] Context window is at 70% capacity — please truncate output"
fi
```

## Phase 2: Git Hygiene Audit (Automatic)

Triggered automatically before any `git commit` or `git push`.

**Pre-commit checks:**

1. **Commit message format** — Does it follow the `type(scope): description` format (e.g., `feat(auth): add login endpoint`)?
   - If not -> notify the user and request correction.
2. **Branch name standard** — Does it start with `feature/`, `bugfix/`, `hotfix/`, or `chore/`?
   - Direct commits to `main` or `master` branches are blocked.
3. **Staged file validation** — In staged files:
   - Is there a large file (>1MB)? -> Warn.
   - Is there a binary file? -> Warn (if unexpected).
   - Are there files containing `.env`, `credentials`, or secrets? -> Block.
4. **Unresolved merge conflicts** — Do any files contain `<<<<<<<`, `=======`, or `>>>>>>>`? -> Block.

```bash
# Branch name check
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" != "feature/"* && "$BRANCH" != "bugfix/"* && "$BRANCH" != "hotfix/"* && "$BRANCH" != "chore/"* ]]; then
  echo "[WARNING] Branch name does not match the standard: $BRANCH"
  echo "  Expected: Must start with feature/, bugfix/, hotfix/, or chore/"
fi
```

## Phase 3: Memory Preservation and Consolidation (Automatic)

Triggered prior to context compression or session closure.

**Pre-consolidation steps:**

1. **Automatic entry in the decision log** — Write all critical decisions made in this session to the `decision-log.md` file:
   - Decision: What was decided?
   - Rationale: Why was this decision made?
   - Alternatives: What options were evaluated?
   - Date: Session timestamp
2. **Save progress status** — Write current phase/state details to the `session-state.md` file.
3. **Apply memory consolidation** — Clean up unnecessary output, preserve critical context.
4. **Validation** — Verify that the saved files are readable.

```bash
# Add to decision log
cat >> decision-log.md << 'EOF'

## Decision: [SHORT TITLE]
- **Date:** $(date '+%Y-%m-%d %H:%M')
- **Decision:** [Decision made]
- **Rationale:** [Why]
- **Alternatives:** [Other options]
- **Impact:** [Expected impact]
EOF
```

## Phase 4: Quality Gates (Pre-Commit, Automatic)

Triggered automatically after any code change and before committing.

**Automatic quality gate sequence:**

1. **Lint check** — Lint the modified files:
   - Python: `ruff check` or `pylint`
   - JavaScript: `eslint`
   - General: Use any executable linter if available.
   - **If errors are found** -> Block commit, request fix.
2. **Test check** — Run existing tests:
   - `pytest`, `jest`, `go test`, etc.
   - **If there are broken tests** -> Block commit, report.
3. **Security scan** — Check for sensitive data/secret leakage:
   - `gitleaks` or `trufflehog` (if available).
   - Look for API keys, tokens, or password patterns.
   - **If findings are found** -> Block commit, report.
4. **Summary report** — Display all gate results in a single table:

```
| Gate        | Status | Detail                         |
|-------------|--------|--------------------------------|
| Lint        | ✓ PASS | ruff — 0 errors, 3 warnings    |
| Test        | ✓ PASS | pytest — 42/42 passed          |
| Security    | ✓ PASS | gitleaks — 0 findings          |
```

## Phase 5: Security Boundaries (Automatic, Pre-Destructive Operation)

Triggered **before** the following types of operations:

- `rm -rf`, `rm -r` (directory deletion)
- `git reset --hard`, `git clean -fd`, `git push --force`
- `DROP TABLE`, `DROP DATABASE`, `DELETE FROM` (SQL queries)
- `chmod -R`, `chown -R`
- Any bulk file deletion or reset operations.

**Pre-operation steps:**

1. **Define the operation** — Explain to the user what you want to perform.
2. **Specify the blast radius** — Which files/directories/databases will be affected?
3. **Request explicit confirmation** — Require explicit input (e.g., "type YES to confirm"):
   - `This operation will delete [X] files/directories. Do you confirm? (type YES):`
4. **Check backups** — Check when the last backup was taken (if applicable).
5. **If confirmed** — Execute the operation.
6. **If not confirmed** — Cancel the operation, suggest an alternative.

```bash
echo "[SECURITY] Destructive operation detected: rm -rf ./build/"
echo "  Affected: build/ directory (will be permanently deleted)"
echo "  Last backup: $(date)"
read -p "  Do you confirm? (type YES): " CONFIRM
if [ "$CONFIRM" != "YES" ]; then
  echo "[CANCEL] Operation cancelled."
  return 1
fi
```

## Phase 6: Session Recovery (Automatic, On Start)

Triggered at the start of every new session.

**Session start steps:**

1. **Check previous session state** — Does `session-state.md` exist?
   - If not -> New session, start clean.
   - If yes -> Initiate recovery workflow.
2. **Load critical context** — Read the last 10 decisions from `decision-log.md`, add them to context.
3. **Resume where left off** — Determine the last active phase/state, continue from there.
4. **Load cross-session memory** — Check `cross-session-memory.md` for:
   - Permanent decisions (do not ask again).
   - Lessons learned.
   - Project constants.
5. **Notify the user** — "Recovered from previous session. Resuming at: [phase/state]"

```bash
if [ -f "session-state.md" ]; then
  echo "[RECOVERY] Previous session state found."
  PREV_STATE=$(head -1 session-state.md)
  echo "  Resuming at: $PREV_STATE"
  echo "  Decision log: decision-log.md (last 10 decisions loaded)"
fi
```

## Phase 7: Token Budget Tracking (Automatic)

Monitors the token limit allocated for each phase.

**Steps:**

1. **Assign budget at phase start** — Default: 4000 tokens per phase.
2. **Update consumption at each step** — Deduct the tokens used from the phase budget.
3. **Warn at 80% consumption** — "You have consumed 80% of your phase budget. Remaining: [N] tokens"
4. **Stop at 100% consumption** — "Phase budget exhausted. To proceed: (a) increase budget (b) terminate phase"
5. **Report at phase end** — "Phase [X] completed. Tokens used: [N]/[BUDGET]"

```bash
# Token budget tracking (at each step)
PHASE_BUDGET=4000
PHASE_USED=$(get_token_usage_for_phase)  # if available
if [ "$PHASE_USED" -gt $((PHASE_BUDGET * 80 / 100)) ]; then
  echo "[BUDGET WARNING] 80% of phase budget used. Remaining: $((PHASE_BUDGET - PHASE_USED)) tokens"
fi
```

## Phase 8: Final Verification

After all guardrails are executed:

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

## Self-Audit

After completing the process for this skill:

1. **Coverage Check:** Did all guardrails run at every step? None bypassed?
2. **Edge Case Check:** Were unexpected scenarios (e.g., context explosion, secret leak) handled correctly?
3. **Quality Check:** Does the output meet the standard of the Iron Law — no guardrail is negotiable?
4. **Retrospective Check:** Did you bypass any guardrail this session? If so, why and how will you fix it?
5. **Improvement Check:** Can the guardrails themselves be improved? Should a new guardrail be added?

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
