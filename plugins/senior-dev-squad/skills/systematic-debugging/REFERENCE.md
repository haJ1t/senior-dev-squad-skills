# Systematic Debugging — Reference

Companion to `SKILL.md`. Contains the full worked example and decision tree referenced in the main skill.

---

## Worked Example

**Bug report:** "User occasionally sees a 401 on the dashboard right after logging in. Happens maybe 1 in 10 times. No errors in the app logs."

---

**Phase 1 — Reproduce reliably:**

Initial attempts with a single browser fail to reproduce. The reporter mentions they tested on two tabs. Hypothesis seed: concurrent requests. Oracle script: open two tabs simultaneously via Playwright, hit `/dashboard` within 50 ms. Repro rate: 7/10. Reliable enough.

---

**Phase 2 — Minimize:**

Remove Playwright; replace with two concurrent `fetch()` calls in a Node script. Still reproduces. Strip auth middleware flags to defaults — still reproduces. Reduce to a single endpoint: `GET /api/me`. Minimal repro: two concurrent requests to `/api/me` with the same session cookie within 100 ms.

```js
// minimal.js
const cookie = 'session=abc123';
Promise.all([fetch('/api/me', { headers: { cookie } }),
             fetch('/api/me', { headers: { cookie } })])
  .then(rs => rs.map(r => console.log(r.status)));
// Output: 200, 401 — every 7/10 runs
```

---

**Phase 3 — One hypothesis:**

"I believe `SessionStore.validate()` has a read-invalidate race: the first request reads the session, the second request reads and then marks it consumed (sliding expiry reset), leaving the first request's subsequent write with a mismatched nonce."

---

**Phase 4 — Change one variable:**

Add a 1 ms sleep between the two requests. Repro drops to 0/10. Remove sleep; repro returns. Confirms timing window is the trigger. Does NOT confirm the exact mechanism yet — proceed.

---

**Phase 5 — Bisect:**

`git bisect run ./minimal.js` between `v1.4.0` (known good) and `HEAD` (bad). Identifies commit `8c3f1a`: "perf: remove per-request session lock". Diff shows a `Mutex.acquire()` call removed from `SessionStore.validate()`.

---

**Phase 6 — Confirm root cause:**

> **Trigger:** Two requests with the same session cookie arrive within the mutex-free window introduced by commit `8c3f1a`.
> **Path:** Both calls to `validate()` read the session record concurrently (line 34). Both compute a new nonce and write back asynchronously. The second write (line 51) overwrites the first write's nonce. The first request then attempts to read its own nonce on the next tick and finds a mismatched value, returning 401.
> **Why it worked before:** The mutex serialized concurrent validations — each request waited for the previous to complete before reading.
> **Proof:** `git bisect` isolates commit `8c3f1a`; re-introducing `Mutex.acquire()` in isolation eliminates the repro 10/10.

---

**Phase 7 — Fix:**

Re-introduce a per-session read-modify-write lock scoped to the session ID (not a global lock, to preserve the perf intent).

---

**Phase 8 — Verify:**

Run `minimal.js` against the fix: 0/10 failures across 50 runs. Full test suite: green.

---

**Phase 9 — Regression test:**

```typescript
it('concurrent session validation does not produce 401 race', async () => {
  const sessionId = await createSession(testUser);
  const results = await Promise.all(
    Array.from({ length: 10 }, () => validateSession(sessionId))
  );
  expect(results.every(r => r.valid)).toBe(true);
});
```

ADR note added: "Locking must be per-session-ID, not global, to avoid serializing unrelated users' requests. See `8c3f1a` post-mortem."

---

## Decision Tree

Use this when the standard phase sequence stalls.

```
START: Bug reported
│
├─ Can you reproduce it?
│   ├─ YES → proceed to Phase 2
│   └─ NO
│       ├─ Do you have logs/traces from the failure?
│       │   ├─ YES → reconstruct the environment from them; try Phase 1 again
│       │   └─ NO → instrument and wait for next occurrence;
│       │           add broad logging NOW; set a "canary" alert
│       └─ Is the reporter the only person who saw it?
│           ├─ YES → suspect reporter-specific state (account flags,
│           │         browser extension, cached data); ask for HAR/console
│           └─ NO → higher confidence it's real; check for common
│                   env differences (region, feature flag, shard)
│
├─ Is the bug intermittent / flaky?
│   ├─ Run the repro 20+ times; measure the failure rate
│   ├─ Flake rate < 5% → likely timing; add instrumentation around
│   │   critical sections; suspect mutex removal, async ordering, TTL edges
│   ├─ Flake rate 5–50% → suspect concurrency or resource contention;
│   │   isolate thread/process count as a variable (Phase 4)
│   └─ Flake rate > 50% → treat as deterministic; find the hidden
│       variable (clock, random seed, env var) that controls the coin flip
│
├─ Is it a regression (worked before, broken now)?
│   ├─ YES → run git bisect immediately (Phase 5 first, then Phase 3)
│   │         The bad commit IS the hypothesis seed
│   └─ NO (new code, new feature)
│       └─ Proceed normally from Phase 1
│
├─ Does the bug only appear in one environment?
│   ├─ Prod only / not local → suspect: config diff, secret diff,
│   │   traffic volume, clock skew, different dependency version
│   │   Action: diff env vars, dependency lock files, infra config
│   ├─ Local only / not CI → suspect: local state, credentials,
│   │   host OS difference, uncommitted files
│   │   Action: reproduce in a clean container; compare CI env vars
│   └─ Specific region / shard only → suspect: data shape, infra version,
│       config drift between nodes. Action: compare shard configs.
│
└─ Is it a Heisenbug (disappears when you observe it)?
    ├─ Adding logging makes it vanish → timing-sensitive; logging adds latency
    │   Action: use non-blocking structured logging; add counters not prints;
    │   try deterministic time injection (fake clock)
    ├─ Debugger pauses make it vanish → race condition; do not use breakpoints
    │   Action: use atomic counters, post-mortem logs, or sleep-injection tests
    └─ Changing compile/opt flags makes it vanish → undefined behavior or
        memory error. Action: run with sanitizers (ASAN, TSAN, Valgrind);
        treat any UB finding as the root cause candidate
```
