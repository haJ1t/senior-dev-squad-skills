# Instincts Guardrails — Reference

Full step-by-step procedures and bash examples for each guardrail phase. Linked from [SKILL.md](SKILL.md).

---

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
