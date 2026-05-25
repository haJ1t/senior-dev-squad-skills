# Incident Responder — Worked Example

A narrated SEV1 walkthrough from detection to postmortem.
See `SKILL.md` for the full process and verification checklist.

---

## SEV1 Walkthrough: Payment Processing Outage

**Scenario:** An e-commerce platform's payment service begins returning 503 errors. Checkout is broken for all users.

---

### 09:14 UTC — Detection

The alerting system fires: `payment-service error rate > 5% for 3 minutes`. PagerDuty pages the on-call engineer, @alice.

@alice acknowledges the alert in PagerDuty within 2 minutes and opens `#inc-20240315-payments` on Slack.

```
[09:14 UTC] 🚨 SEV1 DECLARED — Payment service down. Error rate 47%. All checkout blocked.
IC: @alice | Tech Lead: @bob | Comms: @carol | Scribe: @dave
Bridge: meet.example.com/inc-20240315
```

Severity call: all users blocked from completing checkout → SEV1. No ambiguity; declare immediately.

---

### 09:16 UTC — Classify and Assign

@alice posts a formal declaration:

```
SEV1 — Checkout broken for 100% of users.
Impact: ~$8k/min estimated revenue loss. All regions affected.
IC: @alice | Tech Lead: @bob | Comms: @carol
Bridge open. Join now if you are relevant.
```

@carol opens the status page and posts within 3 minutes of declaration:

```
[09:17 UTC] Investigating — We are aware of an issue affecting checkout. Our team is actively investigating.
Next update: 09:30 UTC.
```

---

### 09:17 UTC — Stabilize First

@alice calls the stabilization checklist on the bridge. **No one starts digging logs yet.**

**Step 1 — Rollback:** @bob checks the deploy log. Last deploy was `payment-service v2.14.1` at `09:03 UTC` — 11 minutes before the alert fired. Correlation is strong.

```bash
kubectl rollout undo deployment/payment-service -n payments
# watching...
kubectl rollout status deployment/payment-service -n payments
# Waiting for rollout to finish: 2 out of 5 new replicas have been updated...
# deployment "payment-service" successfully rolled out
```

@bob monitors error rate in Datadog. At `09:22 UTC`, error rate drops from 47% to 0.3% — baseline restored.

@alice announces on the bridge and in the channel:

```
[09:22 UTC] STABILIZED — Rollback to v2.14.0 successful. Error rate back to baseline.
System is stable. Root-cause investigation begins now.
Next stakeholder update: 09:30 UTC as scheduled.
```

Total time to stabilization: **8 minutes from declaration.**

---

### 09:22–09:55 UTC — Diagnose Root Cause

With the system stable, @bob leads root-cause investigation. @alice continues IC duties (cadence, coordination, bridge).

@bob pulls logs from the failed deployment window:

```bash
kubectl logs deployment/payment-service \
  --since-time="2024-03-15T09:03:00Z" \
  --until-time="2024-03-15T09:22:00Z" \
  | grep -E "ERROR|FATAL|panic"
```

Findings:
- `v2.14.1` introduced a new database connection pool config that set `max_connections=5` (was `50`).
- Under production load, all 5 connections were exhausted within seconds.
- The service returned 503 to every request rather than queuing or degrading gracefully.

Contributing factors identified (not just "bad config"):
1. The config value was hardcoded in the deploy manifest, not sourced from the environment config.
2. Staging ran with a synthetic load of 10 rps; production runs at 1,200 rps — the pool exhausted instantly in prod, never in staging.
3. No alert existed for connection pool saturation — the error surfaced only as a generic 503.
4. The runbook for payment-service rollback did not exist; @bob had to recall the kubectl command from memory.

---

### 09:30 UTC — Comms Cadence (First Scheduled Update)

@carol sends the 15-minute internal update:

```
[09:30 UTC] STATUS UPDATE — SEV1: Payment Service Outage
Impact: Checkout was fully blocked 09:14–09:22 UTC (~8 minutes). System is now STABLE.
Status: Investigating root cause.
Last action: Rolled back v2.14.1 to v2.14.0 at 09:22 UTC. Error rate nominal.
Next update: 09:45 UTC.
```

@carol also updates the public status page from "Investigating" to "Monitoring".

---

### 09:55 UTC — Confirm Stability and Resolve

@alice checks: error rate stable at < 0.2% for 33 minutes. Monitoring green across all regions.

```
[09:55 UTC] RESOLVED — SEV1: Payment Service Outage
Impact window: 09:14–09:22 UTC (8 minutes). All users in that window experienced failed checkout.
System confirmed stable since 09:22 UTC.
Final status page update posted. Postmortem scheduled: 2024-03-17 14:00 UTC.
```

Incident channel archived with postmortem issue link.

---

### 2024-03-17 14:00 UTC — Blameless Postmortem

**Postmortem: Payment Service Outage 2024-03-15**
**Severity:** SEV1 | **Duration:** 8 min | **IC:** @alice | **Attendees:** IC, Tech Lead, Comms, SRE lead, Engineering manager

```markdown
## Impact
- Users affected: ~14,000 (all active checkout sessions during 09:14–09:22 UTC)
- Estimated revenue impact: ~$64k
- SLO burn: 1.4% of monthly error budget consumed in 8 minutes

## Timeline (UTC)
| Time  | Event                                                          |
|-------|----------------------------------------------------------------|
| 09:03 | payment-service v2.14.1 deployed                               |
| 09:14 | Alert fired: error rate > 5%. PagerDuty pages @alice           |
| 09:14 | @alice acknowledges; #inc-20240315-payments opened             |
| 09:16 | SEV1 declared; roles assigned; bridge open                     |
| 09:17 | Status page updated; rollback investigation begins             |
| 09:19 | kubectl rollout undo issued against payment-service            |
| 09:22 | Rollback complete; error rate returns to baseline              |
| 09:22 | Stabilization announced; root-cause investigation begins       |
| 09:30 | Scheduled comms update sent; status page updated to Monitoring |
| 09:55 | System confirmed stable 33+ min; incident declared resolved    |

## Contributing Factors
1. Connection pool `max_connections` hardcoded to 5 in deploy manifest (was 50)
2. Staging load (10 rps) too low to expose pool exhaustion vs production (1,200 rps)
3. No alert for connection pool saturation — failure surfaced only as generic 503
4. No rollback runbook for payment-service; on-call engineer relied on memory

## What Went Well
- Alert fired within 3 minutes of degradation; acknowledgement in 2 minutes
- Rollback decision made immediately; no time lost debating root-cause first
- Comms cadence started before stabilization was confirmed — stakeholders never in the dark
- 8-minute MTTR is a strong result for a full checkout outage

## Action Items
| Item                                              | Owner  | Due        | Ticket |
|---------------------------------------------------|--------|------------|--------|
| Source connection pool config from env, not manifest | @bob | 2024-03-22 | #4421  |
| Add staging load test to deployment pipeline (≥500 rps) | @sre | 2024-03-29 | #4422  |
| Add Datadog alert: connection pool utilization > 80% | @sre | 2024-03-22 | #4423  |
| Write rollback runbook for payment-service        | @alice | 2024-03-20 | #4424  |
| Review all service manifests for hardcoded resource limits | @bob | 2024-04-01 | #4425  |
```

**Facilitation note:** @alice opens with "We are here to understand the system, not to assign blame. The deploy config was a systemic gap — hardcoded values in manifests will always eventually drift. Let's fix the system." No individual was named as a cause.
