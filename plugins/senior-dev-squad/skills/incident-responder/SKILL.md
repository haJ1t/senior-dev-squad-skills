---
name: incident-responder
description: "Drives production incident response end to end: detect, declare, classify, stabilize, communicate, and postmortem. Use when a production system is degraded, an alert fires, customers report failures, or an on-call engineer needs structure."
---

# Incident Responder

## Overview

Production incidents are not debugging sessions — they are time-critical coordination problems. This skill provides the command structure to move a team from chaos to resolution: detect and declare fast, assign clear roles, stabilize the system before hunting root cause, maintain a comms cadence so stakeholders are never in the dark, and close every incident with a blameless postmortem that turns pain into prevention.

**Core principle:** Stabilize first, diagnose second — no amount of root-cause elegance matters while customers are down.

## The Iron Law

```
STOP THE BLEEDING BEFORE YOU READ THE CHART.
EVERY INCIDENT GETS A BLAMELESS POSTMORTEM WITH TRACKED ACTION ITEMS.
```

## When to Use

**Use this when:**
- A production alert fires or a monitoring dashboard turns red
- Customers or support start reporting failures, errors, or degraded performance
- A deploy, migration, or config change causes unexpected breakage
- An on-call engineer needs a coordination framework under pressure
- A partial outage risks cascading into a full outage

**Use this ESPECIALLY when:**
- The blast radius is growing and multiple engineers are jumping in without roles assigned
- The team is spending time diagnosing root cause while the system is still down
- Stakeholders are asking "what's going on?" with no clear answer
- A previous incident recurred because the postmortem had no action items

**Never skip when:**
- "It only hit a small percentage of users" — severity guides scope, not whether the process runs
- "We already know the cause" — stabilize and postmortem still required; knowing the cause doesn't skip the steps

## Severity Classification

| SEV | Customer Impact | Response Target | Example |
|-----|----------------|-----------------|---------|
| SEV1 | Complete outage or data loss; all/most users blocked | Immediate; IC assigned in <5 min | Site down, payments failing for all |
| SEV2 | Major feature broken; significant user population impacted | IC assigned in <15 min | Checkout broken for 30% of users |
| SEV3 | Partial degradation; workaround exists | Acknowledged in <1 h | Slow search; reports delayed |
| SEV4 | Minor bug; minimal impact | Triaged within business hours | Cosmetic error on non-critical page |

Upgrade severity immediately if impact is spreading or unknown. Downgrade only after stability is confirmed.

## Workflow

### Phase 1: Detect and Declare

1. **Acknowledge the alert** — claim ownership in the incident channel within 5 minutes. Silence means no one is on it.
2. **Open an incident channel** — `#inc-YYYYMMDD-<slug>` (or your org's convention). All incident communication happens here; no side channels.
3. **Assign Incident Commander (IC)** — one person owns the incident end to end. IC is coordinator, not necessarily the fixer. If you are alone, you are the IC.
4. **Assign supporting roles** — Communications Lead (stakeholder updates), Tech Lead (hands-on investigation), Scribe (timeline log). For SEV3/4 a single engineer can hold all roles.
5. **Declare severity** — use the table above. Announce: `SEV2 declared — checkout broken for ~30% of users. IC: @alice. Tech Lead: @bob. Bridge: [link].`

### Phase 2: Stabilize (Before Diagnosing)

**BEFORE opening any root-cause investigation**, run through these mitigations in order:

1. **Rollback the last change** — if a deploy or config change correlates with the incident start time, revert it first. This is the fastest path to recovery in most incidents.
   ```bash
   # Example: revert the last Kubernetes deployment
   kubectl rollout undo deployment/<service-name> -n <namespace>
   # Verify rollout status
   kubectl rollout status deployment/<service-name> -n <namespace>
   ```
2. **Kill the feature flag** — if the degraded path is behind a feature flag, disable it immediately.
3. **Trigger failover** — route traffic to a healthy region, replica, or fallback service if available.
4. **Scale up** — if the failure is resource exhaustion (CPU, memory, connection pool), scale horizontally as a bridge while the real fix is prepared.
5. **Shed load** — enable rate limiting, disable non-critical background jobs, or return a degraded-mode response rather than errors.

Once the system is stable (error rate back to baseline, monitoring green), announce stabilization in the channel before switching to diagnosis.

### Phase 3: Communicate

Run a cadence appropriate to severity. Stakeholders need updates on a schedule, not on demand.

| SEV | Internal cadence | Status page |
|-----|-----------------|-------------|
| SEV1 | Every 15 min in incident channel | Post within 10 min of declaration; update every 30 min |
| SEV2 | Every 30 min | Post within 30 min; update every 1 h |
| SEV3 | Every 1–2 h | Optional; post if customer-facing |
| SEV4 | Single update when resolved | Not required |

**Update template (use every cycle):**

```
[HH:MM UTC] STATUS UPDATE — SEV<N>: <title>
Impact: <what users are experiencing>
Status: Investigating / Stabilizing / Monitoring / Resolved
Last action: <what the team just did>
Next update: <HH:MM UTC or "when status changes">
```

When resolved, send a final update: impact window, user count affected, and link to the postmortem.

### Phase 4: Diagnose Root Cause

Only begin deep diagnosis after stabilization. Assign the Tech Lead to own this; IC continues coordination and comms.

1. **Build the timeline** — reconstruct events from logs, deploy records, alerts, and team messages. Every timestamp matters.
   ```bash
   # Pull structured logs for the incident window
   kubectl logs deployment/<service> --since-time="<ISO8601-start>" | grep -E "ERROR|WARN"
   ```
2. **Identify contributing factors** — resist the urge to pick one cause. Incidents have multiple contributing factors (code bug AND monitoring gap AND missing runbook AND capacity headroom).
3. **Test your hypothesis** — confirm the root cause in a staging environment or with a targeted probe before declaring it.
4. **Implement a permanent fix** — create a ticket/issue, link it to the incident, assign an owner and due date.

### Phase 5: Resolve and Close

1. Confirm monitoring is green and has been stable for at least 15 minutes.
2. Send the final status update to stakeholders and update the status page to "Resolved."
3. Archive the incident channel with a link to the postmortem issue.
4. Schedule the postmortem within 5 business days (48 h for SEV1).

### Phase 6: Blameless Postmortem

**Every SEV1 and SEV2 is mandatory. SEV3 is encouraged.**

The postmortem is a learning document, not a blame assignment. The goal is systemic improvement.

Structure:

```markdown
## Postmortem: <title>
**Date:** YYYY-MM-DD  **Severity:** SEV<N>  **Duration:** Xh Ym  **IC:** @name

### Impact
- Users affected: ~N
- Revenue impact: $X (if known)
- SLO burn: X% of error budget

### Timeline (all times UTC)
| Time | Event |
|------|-------|
| HH:MM | Alert fired |
| HH:MM | IC declared SEV<N> |
| HH:MM | Rollback initiated |
| HH:MM | System stabilized |
| HH:MM | Root cause confirmed |
| HH:MM | Incident resolved |

### Contributing Factors
- (not "root cause" singular — list all factors)

### What Went Well
- (detection was fast, rollback worked, comms were clear)

### Action Items
| Item | Owner | Due | Ticket |
|------|-------|-----|--------|
| Add circuit breaker to payment service | @eng | YYYY-MM-DD | #123 |
| Add alert for connection pool saturation | @sre | YYYY-MM-DD | #124 |
| Update runbook for failover procedure | @ic | YYYY-MM-DD | #125 |
```

Action items without owners and due dates are not action items.

## Worked Example

See [REFERENCE.md](./REFERENCE.md) for a complete narrated SEV1 walkthrough: payment service outage, detection to blameless postmortem. Key decisions illustrated: rollback chosen over diagnosis, comms cadence started before stabilization confirmed, four contributing factors identified (not one root cause), all action items ticketed with owners.

## Decision Tree

```
ALERT / REPORT RECEIVED
│
├── Is the system currently degraded or down?
│   NO → SEV4 triage during business hours. Skip to Phase 4.
│   YES ↓
│
├── CLASSIFY SEVERITY
│   ├── All/most users blocked OR data loss risk? → SEV1 (IC in <5 min)
│   ├── Major feature broken, significant % of users? → SEV2 (IC in <15 min)
│   ├── Partial degradation, workaround exists? → SEV3 (ack in <1 h)
│   └── Minor / cosmetic, minimal impact? → SEV4 (triage in biz hours)
│       ⚠ Unsure? → Classify UP. Downgrade only after stability confirmed.
│
├── STABILIZE — pick the fastest path:
│   ├── Recent deploy correlates with incident start? → ROLLBACK FIRST
│   │     kubectl rollout undo / git revert / terraform apply previous
│   ├── Degraded path is behind a feature flag? → KILL THE FLAG
│   ├── Healthy region / replica / fallback available? → FAILOVER
│   ├── Resource exhaustion (CPU/mem/connections)? → SCALE OUT
│   └── None of the above? → SHED LOAD (rate limit / degrade gracefully)
│       then escalate to domain expert while shedding
│
├── PAGE / ESCALATE?
│   ├── SEV1 / SEV2 → page IC immediately; page domain expert if stabilization
│   │     stalls after 15 min
│   ├── SEV3 → notify IC; page domain expert only if impact is spreading
│   └── SEV4 → no page; ticket and assign
│
├── ROLLBACK vs FORWARD-FIX vs FAILOVER
│   ├── Known bad change AND rollback is low-risk → ROLLBACK (fastest)
│   ├── Rollback would cause data loss or is blocked → FAILOVER if available;
│   │     else FORWARD-FIX with targeted patch under IC coordination
│   └── Data corruption suspected → STOP ALL WRITES; engage data team
│
└── DECLARE RESOLVED?
    ├── Monitoring green? YES
    ├── Error rate at baseline for ≥ 15 min? YES
    ├── Status page updated? YES
    └── Postmortem scheduled? YES → RESOLVED ✓
        Any NO → keep monitoring; do not declare resolved
```

## Red Flags — STOP and Follow Process

- "Let me dig into the logs before we do anything" — you are diagnosing before stabilizing; return to Phase 2 immediately
- "We don't need an IC, we all know what to do" — uncoordinated engineers duplicate work, miss mitigations, and contradict each other in the war room
- "Two of us will just figure it out together" — shared IC is no IC; one person must own the decision authority
- "Skip the status page, it's almost resolved" — stakeholders hearing from customers before you tell them is a trust-destroying failure mode
- "Let's stay in a side channel / DM to coordinate" — incident communication must be in the incident channel; side channels split the timeline
- "The postmortem can wait, we're too busy" — the next incident will be identical if you wait long enough to forget this one
- "We know who caused this" — blameless means systemic causes, not human blame; naming a person shuts down honest disclosure in every future postmortem
- "Action items are obvious, no need to write them down" — untracked action items close at 0%; the evidence is every postmortem you have ever seen
- "We're still investigating, no update needed yet" — silence during a SEV1 is itself an incident for stakeholders; send the cadence update regardless

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We know the root cause, just fix it" | Knowing the cause doesn't mean the system is stable. Stabilize first — the forward-fix can land cleanly after the bleeding stops. |
| "We'll write the postmortem later" | Later never comes. Schedule within 48 h for SEV1; memory degrades fast and the team moves on. |
| "It was just one bad deploy, no need for process" | Skipping process is how one bad deploy becomes a recurring outage pattern. The process also protects the deployer from blame. |
| "Customers didn't notice" | Absence of complaints ≠ absence of impact. Check error rates, drop in conversions, silent data corruption. |
| "We fixed it so fast a postmortem is overkill" | Fast resolution is exactly the scenario to document — the postmortem captures what made it fast, so next time isn't lucky. |
| "The postmortem will demoralize the team" | Blameless postmortems build trust. Cultures that skip postmortems hide incidents, accumulate technical debt, and repeat them. |
| "We have two commanders coordinating" | Two ICs mean no IC. Every contested decision escalates; one person must break ties and own outcomes. |
| "Staging didn't show this problem" | Staging gaps are a contributing factor, not an excuse. Add a postmortem action item: close the fidelity gap. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why are we still down?" — You started diagnosing before stabilizing; return to Phase 2.
- "Does anyone know what's happening?" — You skipped the IC assignment and comms cadence; return to Phase 1.
- "We never followed up on the last incident's action items" — Postmortem action items aren't tracked; add them to your issue tracker now.
- "This is the third time this has happened" — Postmortem contributing factors were not addressed; revisit Phase 6 action items.

**When you see these:** STOP. Return to the relevant phase.

## Related Skills

- **ship-readiness-checklist** — run before deploys to prevent incidents rather than react to them
- **forensic-investigator** — deep log and artifact analysis once the system is stable and you're in root-cause phase
- **chaos-engineer** — proactively surface failure modes before they become incidents in production
- **devops-release-engineer** — coordinate the deploy pipeline that often triggers SEV events; aligns rollback and rollforward procedures
- **soc2-audit-prep** — incident records and postmortems are primary evidence for SOC 2 CC7 (security monitoring) controls

## Verification

- [ ] Incident channel opened and IC declared within 5 minutes of detection
- [ ] Severity level assigned and announced with impact statement
- [ ] Stabilization attempted (rollback / flag kill / failover) BEFORE root-cause investigation began
- [ ] Comms cadence met — stakeholder updates sent on schedule for the declared severity
- [ ] Status page updated within the target window for the severity
- [ ] System confirmed stable for at least 15 minutes before declaring resolved
- [ ] Final resolution update sent to all stakeholders
- [ ] Postmortem scheduled within 5 business days (48 h for SEV1)
- [ ] Postmortem includes a timeline, contributing factors (plural), and action items with owners + due dates
- [ ] All action items tracked in the issue tracker with assigned owners
