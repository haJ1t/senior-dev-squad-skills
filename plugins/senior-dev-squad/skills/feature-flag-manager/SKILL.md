---
name: feature-flag-manager
description: "Manages feature flags across their full lifecycle: creation, targeting, rollout, kill-switch, and removal. Use when adding flags, ramping releases, responding to incidents, or auditing flag debt."
---

# Feature Flag Manager

## Overview

Feature flags are a deployment superpower — and a debt-accumulation machine. This skill governs the full lifecycle of every flag: choosing the right flag type, writing targeting rules, executing safe percentage rollouts, triggering kill switches during incidents, and — critically — removing flags before they become permanent load-bearing code no one dares touch.

The failure mode is not adding flags. The failure mode is never removing them. A codebase full of stale toggles is a codebase where nobody knows what's on, what's off, or what happens if you flip the wrong switch. Every flag that ships without an owner and a removal date is tech debt that compounds silently in production.

**Core principle:** Every flag is temporary. Name an owner, set an expiry date, and treat removal as part of the feature, not a future cleanup task.

## The Iron Law

```
EVERY FLAG SHIPS WITH AN OWNER, AN EXPIRY DATE, AND A REMOVAL TICKET.
A FLAG WITH NO EXPIRY IS TECH DEBT DISGUISED AS A FEATURE.
```

This is non-negotiable. The flag lifecycle ends with deletion. If you cannot name who owns it and when it dies, you are not done defining the flag.

## When to Use

**Use this when:**
- Introducing a new flag of any type (release, experiment, ops, permission)
- Ramping a feature from 0 % to 100 % of traffic
- Responding to a production incident that requires instant rollback
- Auditing existing flags for staleness or missing owners
- Cleaning up flags after a feature reaches full rollout

**Use this ESPECIALLY when:**
- A release is going out under time pressure ("we'll clean up the flag later")
- An experiment ends but the winning variant code is never cleaned up
- Someone adds a flag "just in case" with no defined purpose or owner
- The codebase has flags older than 90 days that are still at 0 % or 100 %

**Never skip when:**
- The flag targets PII-sensitive cohorts or permission tiers — ownership and audit trail are mandatory
- You are activating a kill switch — follow the procedure even at 2 AM
- An experiment concludes — the winning path must be hardcoded and the flag removed

## Flag Type Reference

Every flag belongs to exactly one type. The type determines its expected lifetime and cleanup trigger.

| Type | Purpose | Typical Lifetime | Removal Trigger |
|---|---|---|---|
| **Release toggle** | Gate an in-progress feature from reaching users prematurely | Days to weeks | Feature reaches 100 % and is stable for one release cycle |
| **Ops / kill switch** | Instantly disable a risky code path during an incident | Indefinite (long-lived) | Risky path removed or risk accepted permanently |
| **Experiment / A/B** | Split traffic to measure hypothesis outcomes | Duration of experiment (days to weeks) | Experiment concludes; winning variant hardcoded |
| **Permission / entitlement** | Gate features by user plan, role, or cohort | Long-lived (product lifecycle) | Feature becomes universally available or product tier retired |

Long-lived flags (ops, permission) must still have an owner and a review cadence — they are not exempt from the Iron Law.

## Phase 1: Define the Flag

Before creating anything, answer every field in this definition block. If any field is blank, stop and get the answer.

```yaml
# Flag definition — required before creation
flag_key: payments.new_checkout_flow      # snake_case, namespaced by domain
type: release                             # release | ops | experiment | permission
description: >
  Gates the redesigned checkout flow for gradual rollout.
  Off = legacy flow. On = new flow.
owner: "@alice"                           # single accountable engineer
team: "payments-squad"
created: 2026-05-25
expiry: 2026-06-22                        # hard deadline — must exist
removal_ticket: PROJ-4821                 # ticket to delete the flag + dead code
default_off_behavior: "serve legacy checkout flow"
default_on_behavior: "serve new checkout flow"
```

**Rules:**
1. `flag_key` must be namespaced (`domain.flag_name`). Flat names create collisions.
2. `expiry` is a calendar date, not "after launch" or "when stable."
3. `removal_ticket` must exist in your tracker before the flag is created in code.
4. Write down what both states do. If you cannot describe the off state, you do not understand the flag.

## Phase 2: Implement the Flag

**Guard pattern — wrap the minimum surface area:**

```typescript
// Good: flag wraps only the diverging branch
if (featureFlags.isEnabled('payments.new_checkout_flow', { userId })) {
  return renderNewCheckout(cart);
}
return renderLegacyCheckout(cart);

// Bad: flag wraps unrelated logic or entire page render
if (featureFlags.isEnabled('payments.new_checkout_flow', { userId })) {
  // 300 lines of mixed old/new logic
}
```

**Testing both states is mandatory:**

```typescript
describe('checkout flow flag', () => {
  it('renders new checkout when flag is ON', () => {
    mockFlag('payments.new_checkout_flow', true);
    // assert new flow renders
  });

  it('renders legacy checkout when flag is OFF', () => {
    mockFlag('payments.new_checkout_flow', false);
    // assert legacy flow renders
  });
});
```

If your test suite only covers the on-state, the off-state is untested in production. This is the most common flag implementation bug.

## Phase 3: Configure Targeting and Rollout

**Targeting rule hierarchy** (evaluate top to bottom; first match wins):

```
1. Override list (specific user IDs, org IDs) — for internal testing
2. Cohort rules (role = admin, plan = enterprise, region = EU)
3. Percentage rollout (hash on stable user ID, not session ID)
4. Default (flag default_value)
```

**Gradual rollout schedule — never go 0 % → 100 % in one step:**

```
Day 1:   1 %   — internal users / beta opt-ins only
Day 2:   5 %   — watch error rate, latency p99, conversion
Day 3:  20 %   — widen if metrics nominal
Day 5:  50 %   — pause point: full metric review
Day 7: 100 %   — full rollout; start removal clock
```

Pause at each step if any of these signals spike: error rate, latency p99, support tickets, revenue metrics. Do not advance the rollout while signals are degraded.

**Stable hashing rule:** percentage rollout MUST hash on a stable user identifier (user_id, org_id), never on session ID or request ID. Session-based hashing causes users to see the feature flicker on and off across sessions, which breaks experiments and confuses support.

## Phase 4: Operate the Kill Switch

An ops / kill switch flag is your fastest path to stopping a production incident without a deploy. Treat its activation as an incident response action.

**Activation procedure:**

1. **Confirm** the kill switch covers the failing code path (check the flag definition's `default_off_behavior`)
2. **Announce** in the incident channel: "Activating kill switch `payments.new_checkout_flow` — rolling back to legacy flow"
3. **Flip** the flag to 0 % (or the off default) in your flag management console
4. **Observe** error rate and latency for 2 minutes — confirm recovery
5. **Do not remove** the flag immediately after activation; the risky code path must be fixed or removed first
6. **Post-incident:** file a follow-up to either harden the path and re-enable, or delete the path and retire the flag

**Kill switch coverage requirement:** any code path whose failure would trigger a P1/P2 incident MUST have an ops flag before it ships to production. "We'll add one if something goes wrong" is not a mitigation.

## Phase 5: Remove the Flag

Flag removal is a feature, not a chore. Schedule it at creation. Execute it at expiry.

**Removal checklist sequence:**

1. Confirm the winning state (on or off) with the flag owner
2. Hardcode the winning branch; delete the losing branch and its dead code
3. Delete the flag definition from all environments (dev, staging, prod)
4. Delete mock/stub helpers from the test suite
5. Search for stray references: `grep -r "payments.new_checkout_flow" .` — must return zero results
6. Close the removal ticket
7. Deploy and verify the dead code path is gone from production

```bash
# Verify no stale references remain
grep -r "payments.new_checkout_flow" . --include="*.ts" --include="*.tsx" --include="*.py"
# Expected output: (none)
```

**Flag debt audit** — run this monthly on any codebase with more than 10 active flags:

```
For each active flag:
  - Is expiry date past? → remove or escalate to owner
  - Is percentage == 100 % for > 30 days? → remove
  - Is percentage == 0 % for > 30 days? → remove or document why it exists
  - Is owner still on the team? → reassign or escalate
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "We'll clean up the flag after launch" — launch never ends; the flag never dies
- "It's just a quick flag, no need for a removal ticket" — every flag ever abandoned started as a quick flag
- "I'll test the on-state; the off-state is just the old behavior" — the old behavior now has a new code path; test it
- "We can skip the gradual rollout, it's a small change" — every outage caused by a flag skip felt small before the skip
- "The flag has been at 100 % for months, it's fine" — fine means remove it
- "I don't know who owns this flag" — that is the emergency

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "We'll remove the flag once things are stable" | Stable never comes. Stability is the flag not being touched. Schedule the date at creation or it will never happen. |
| "The off-path is just the old code, it doesn't need tests" | The old code is now behind a new branch condition. Any refactor can silently break it. Test both states. |
| "A kill switch isn't needed for this feature, it's low risk" | Kill switches are for when you are wrong about risk. You cannot predict which features will fail. |
| "Only 1 % rollout, so bugs won't matter much" | 1 % of 10 million users is 100,000 users seeing the bug. It matters. |
| "The flag owner left the team, but the flag still works" | Nobody will remove it. Nobody will know what happens if it breaks. Reassign immediately. |
| "We keep this flag for emergency rollback forever" | That is an ops flag. Name it correctly, document it, and give it a review cadence — not indefinite drift. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Who owns this flag?" — The flag was created without an owner in the definition
- "Why is this flag still here?" — Expiry was set but removal was never executed; check the removal ticket
- "The feature is fully rolled out but the flag code is everywhere" — Phase 5 was skipped; begin removal now
- "Users are seeing inconsistent behavior" — Percentage rollout is hashing on session ID, not user ID; fix the hash key
- "I can't tell what this flag does" — The flag definition lacks a description of both on and off behavior; add it now

**When you see these:** STOP. Return to the phase where the gap lives.

## Related Skills

- **devops-release-engineer** — use alongside for deployment pipeline integration; flags gate deploys, deploys gate rollouts
- **incident-responder** — use when a kill switch activation escalates to a full incident; this skill hands off to that one
- **test-engineer** — use to enforce that both flag states have test coverage before any flag ships
- **tech-debt-tracker** — use during monthly flag debt audits; stale flags are tracked tech debt
- **spec-first-development** — use before creating an experiment flag; the hypothesis and success metrics must be in a spec

## Verification

Before marking any flag work complete:

- [ ] Flag definition includes `flag_key`, `type`, `owner`, `team`, `expiry`, and `removal_ticket`
- [ ] Both on-state and off-state behavior are written in plain language in the definition
- [ ] Flag key is namespaced (`domain.flag_name`), not a flat name
- [ ] A removal ticket exists in the issue tracker and is linked from the flag definition
- [ ] Flag implementation wraps the minimum diverging surface area — no flag wrapping unrelated logic
- [ ] Test suite covers both flag-on and flag-off states
- [ ] Rollout is configured to hash on stable user/org ID, not session ID
- [ ] Gradual rollout schedule is defined with named pause points and metric thresholds
- [ ] For ops flags: kill-switch procedure is documented and the team knows it exists
- [ ] For experiment flags: hypothesis and success metrics are written before the flag ships
- [ ] At 100 % rollout: removal is scheduled and the removal ticket is in the current sprint
- [ ] Post-removal: `grep` for stale flag references returns zero results
