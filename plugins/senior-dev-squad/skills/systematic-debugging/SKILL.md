---
name: systematic-debugging
description: "Diagnoses bugs to verified root cause using reproduce-minimize-hypothesize-bisect-confirm. Use when a bug resists quick fixes, flakes, only appears in one env, or is a regression."
---

# Systematic Debugging

## Overview

Systematic debugging is the discipline of finding the actual root cause of a defect before writing a single fix. It replaces instinct-driven trial-and-error with a reproducible scientific method: shrink the problem, isolate the variable, explain the mechanism, then fix. This process does not slow you down — it prevents you from "fixing" the wrong thing and shipping new bugs in its wake.

**Core principle:** You cannot fix what you cannot explain. A fix without a mechanism hypothesis is a guess wearing a commit message.

## The Iron Law

```
REPRODUCE BEFORE YOU FIX. CHANGE ONE VARIABLE AT A TIME.
NEVER CLOSE A BUG YOU CANNOT MECHANISTICALLY EXPLAIN.
```

If you have not reproduced the failure reliably, you are not debugging yet — you are speculating. If you cannot state the exact causal chain from trigger to symptom, the investigation is not done.

## When to Use

**Use this when:**
- A bug report arrives and the cause is not immediately obvious
- A fix attempt failed or made the bug worse
- A feature works locally but fails in staging or production
- A test flakes intermittently across CI runs
- The bug appeared after a recent change (regression)

**Use this ESPECIALLY when:**
- You feel pressure to ship a hotfix NOW (pressure creates wrong fixes)
- The bug is intermittent and you have only seen it once
- Multiple engineers have already tried to fix it without success
- The symptoms are bizarre or contradictory (Heisenbugs need a process, not luck)

**Never skip when:**
- Someone says "just try X and see if it works" — that is how you lose hours
- The bug looks obvious at first glance (obvious-looking bugs hide the real cause most often)
- You are under a production incident SLA (the process takes 20 minutes; guessing takes hours)

## The Nine Phases

### Phase 1: Reproduce Reliably

**Goal:** a runnable, consistently-failing reproduction. If you cannot reach this state, consult the Decision Tree in [REFERENCE.md](./REFERENCE.md).

1. **Capture the exact environment** — OS, runtime version, config flags, seed data, user state. Write it down.
2. **Run the reporter's exact steps** — copy-paste inputs, use the same endpoint, the same fixture data.
3. **Confirm the failure mode** — exact error message, stack trace line, or observed vs. expected output.
4. **Achieve a pass/fail oracle** — a deterministic signal: a log line, assertion, HTTP status. "It feels slow" is not an oracle.

```bash
# Freeze the env so nothing drifts under you
node --version > repro-env.txt && npm ls --depth=0 >> repro-env.txt && git rev-parse HEAD >> repro-env.txt
```

**Exit criterion:** repro script produces the failure 3/3 times.

### Phase 2: Minimize the Reproduction

**Goal:** the smallest possible input / code path that still triggers the bug.

1. Strip unrelated inputs one at a time until the bug disappears; put the last removed item back — it is load-bearing.
2. Inline dependencies: replace external services with stubs. Bug survives → not in the external service.
3. Bisect the data: split a large triggering dataset in half; recurse until minimal.
4. Produce a self-contained script a teammate can run cold.

A minimal reproduction exposes the bug's shape. Skipping this phase means chasing ghosts.

### Phase 3: Form One Hypothesis

**Goal:** a single, falsifiable statement about the cause.

Form: *"I believe [component/path] causes [symptom] when [condition] because [mechanism]."*

Rules:
- **One hypothesis at a time.** Rank candidates; start with the most likely.
- **The hypothesis must be falsifiable** — there must be an observation that would prove it wrong.
- **Write it down** before testing. This prevents post-hoc rationalization.

Bad: "Maybe it's a race condition."
Good: "I believe `UserCache.get()` returns a stale token when two requests arrive within 100 ms because the TTL check reads `Date.now()` before the async write completes."

### Phase 4: Test by Changing One Variable

**Goal:** evidence that confirms or eliminates the hypothesis.

1. Identify the single observable change your hypothesis predicts.
2. Change **only that variable**. Revert everything else to the known-good state.
3. Record the result: pass, fail, or changed symptom.
4. Interpret: failure persists → hypothesis wrong, return to Phase 3. Failure disappears → supported, proceed. Symptom changes → refine.

```python
# Change ONE thing: set cache TTL to 0. Run oracle. Record.
CACHE_TTL = 0   # was: 100
result = run_oracle()
# Do NOT also change thread count, batch size, or anything else.
```

### Phase 5: Bisect / Binary-Search the Space

**Goal:** pinpoint the exact commit, line, or layer responsible.

**`git bisect` for regressions:**
```bash
git bisect start
git bisect bad                       # current commit fails
git bisect good v2.3.1               # last known good release
git bisect run ./scripts/oracle.sh   # automates the binary search
git bisect reset
```

**Comment-out bisection for call-stack depth:** disable the deepest call; if the bug disappears, it lives there. Re-enable and remove the one above; repeat.

**Layer isolation for environment-only bugs:** swap each layer (framework version, runtime, OS). The layer where the swap changes the outcome contains the bug.

Exit criterion: you can name the exact commit hash, function, or infrastructure layer responsible.

### Phase 6: Confirm the Root Cause

**Goal:** explain the mechanism completely in prose before writing the fix.

Write a root-cause statement with:
- **Trigger:** the exact condition that initiates the failure
- **Path:** the causal chain from trigger to symptom, naming each step
- **Why it worked before:** what changed or what edge case was not previously hit
- **Proof:** the evidence (bisect output, log lines, test result) that confirms the path

If you cannot write this statement, return to Phase 3.

### Phase 7: Fix

Write the fix. The Phase 6 statement tells you exactly what to change.

1. Fix the mechanism, not the symptom — suppressing an error log is not a fix.
2. Make the smallest change that addresses the confirmed root cause.
3. Leave the minimal reproduction runnable — you need it in Phase 8.

### Phase 8: Verify the Repro Is Gone

Run your Phase 1/2 reproduction script against the fix.

- Repro fails (bug is gone): continue.
- Repro still passes (bug survives): the fix is wrong. Return to Phase 3. Do not ship.

Run the full test suite. New failures indicate the fix broke something else — return to Phase 4.

### Phase 9: Regression Test and Prevention

1. **Write a regression test** that exercises the exact minimal reproduction. It must fail on pre-fix code and pass on post-fix code.
2. **Add to CI** at the appropriate level: unit, integration, or e2e.
3. **Document a post-mortem note** (comment or ADR entry): what the root cause was, why existing tests missed it, what systemic change prevents the class recurring.

```typescript
// regression: concurrent session writes cause token mismatch (commit a3f9d2)
it('handles concurrent session creation without token collision', async () => {
  const [s1, s2] = await Promise.all([createSession(userId), createSession(userId)]);
  expect(s1.token).not.toBe(s2.token);
  expect(await getSession(s1.token)).toBeDefined();
  expect(await getSession(s2.token)).toBeDefined();
});
```

## Worked Example and Decision Tree

The full worked example (a concurrent-session 401 race walked through all nine phases) and the branching Decision Tree (no-repro, intermittent/flaky, regression, environment-only, Heisenbug paths) are in [REFERENCE.md](./REFERENCE.md).

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I know what this is, let me just push the fix"
- "I can't reproduce it but I see a suspicious line, I'll change it anyway"
- "I changed three things and it stopped failing, good enough"
- "It's probably a network blip, it'll sort itself out"
- "The test is flaky, let me just mark it `skip`"
- "We'll add the regression test in the next sprint"
- "I understand the mechanism well enough without writing it down"

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I've seen this pattern before, I know the fix" | Pattern recognition fails on bugs with similar symptoms but different causes. Phase 3 exists for this. |
| "I can't reproduce it, so I can't debug it" | No repro means invest in observability, not give up. Instrument, wait, reconstruct. |
| "Changing two things at once saves time" | It loses the signal entirely. You now cannot know which change mattered. |
| "The fix is obvious from the stack trace" | Stack traces show where the program noticed the problem, not where it was caused. |
| "Adding logging will disturb the bug" | That tells you it is timing-sensitive. That IS the finding — use it. |
| "We can skip the regression test, we understand the cause" | Understanding does not stop the same pattern recurring in six months. The test does. |
| "Debugging in prod is faster" | Debugging in prod changes prod. Reproduce locally; use prod logs as clues only. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Did you actually reproduce it?" — You described the bug without running it
- "What's your hypothesis?" — You are changing code without a stated mechanism
- "Why did you change that?" — You changed more than one variable; partner cannot follow your reasoning
- "Can you reproduce it in a clean environment?" — Your repro is contaminated by local state
- "What does the root cause statement say?" — You skipped Phase 6 and went straight to a fix
- "Did the repro pass before you opened the PR?" — You forgot Phase 8
- "Where's the regression test?" — Phase 9 is incomplete

**When you see these:** STOP. Name the phase you skipped and return to it before writing another line of code.

## Related Skills

- **forensic-investigator** — use when the bug involves production data or you must reconstruct a timeline from logs rather than live reproduction
- **incident-responder** — use when the bug is actively causing a production outage; this skill feeds the "root cause" step of the incident process
- **edge-case-hunter** — use after Phase 6 to enumerate which other inputs could trigger the same mechanism before writing the fix
- **test-engineer** — use in Phase 9 to ensure the regression test is at the right level and matches project testing standards
- **research-first** — use when Phase 3 stalls because the mechanism involves an unfamiliar library, protocol, or runtime behaviour

## Verification

Before closing any bug investigation:

- [ ] Reproduction script runs and fails deterministically (Phase 1 complete)
- [ ] Minimal reproduction isolated — no unrelated inputs or services (Phase 2 complete)
- [ ] Written hypothesis: "X causes Y when Z because M" (Phase 3 complete)
- [ ] Only one variable changed per test run; result recorded (Phase 4 complete)
- [ ] Exact commit, line, or layer identified via bisection or isolation (Phase 5 complete)
- [ ] Root-cause statement written: trigger, causal path, why-before, proof (Phase 6 complete)
- [ ] Fix addresses the mechanism, not the symptom (Phase 7 complete)
- [ ] Reproduction script passes on fixed code; full test suite green (Phase 8 complete)
- [ ] Regression test added to CI and named with the bug reference (Phase 9 complete)
- [ ] Post-mortem note or ADR comment explains the class of bug and systemic prevention
