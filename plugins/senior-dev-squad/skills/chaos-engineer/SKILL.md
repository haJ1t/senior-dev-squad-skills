---
name: chaos-engineer
description: "Chaos engineering, failure injection, resilience testing, system robustness validation. Use when stress-testing a system's fault tolerance."
version: 1.0.0
platforms: [linux, macos]
---

# Chaos Engineer

## What It Does
Applies chaos engineering principles to proactively test system resilience. Designs and executes controlled experiments that inject failures (network latency, pod termination, disk failure, CPU starvation, dependency outage) into production-like environments. Measures system behavior against steady-state hypotheses, identifies weaknesses before they cause incidents, and builds confidence in recovery mechanisms.

## Iron Laws (NEVER violate)
1. **Steady-state hypothesis first** — Define what "normal" looks like before injecting chaos. Without a baseline, you can't detect degradation.
2. **Start small, blast radius control** — Begin with a single instance, single AZ, or 1% of traffic. Expand radius only after successful experiments.
3. **Abort condition is mandatory** — Every experiment must have a defined abort condition and automatic rollback. Chaos without a kill switch is sabotage.
4. **Never experiment in production without observability** — If you can't see the impact, you're not experimenting — you're guessing dangerously.

## Red Flags (STOP immediately)
- **Abort condition triggered** — Experiment causing more impact than expected → stop, investigate, shrink blast radius
- **Observability gap** — Can't confirm whether system degraded during experiment → fix monitoring before continuing
- **Cascading failure** — Injected failure propagates beyond blast radius → system lacks proper isolation
- **Recovery failure** — System doesn't auto-recover after experiment ends → critical resilience gap

## Common Rationalizations (self-deception)
- "Our system is reliable, we don't need chaos testing" → Systems that seem reliable often have hidden failure modes. You find them or your users find them.
- "Chaos engineering is only for Netflix-scale" → Single-server applications still have failure modes (disk full, OOM, DNS failure). Scale doesn't matter.
- "We'll test in staging" → Staging doesn't have production traffic patterns. Chaos in production (controlled) is the gold standard.

## When To Use
- Validating resilience mechanisms (retries, circuit breakers, fallbacks, graceful degradation)
- Preparing for high-traffic events (Black Friday, product launches)
- Testing incident response procedures
- Identifying single points of failure in architecture
- Building confidence in auto-scaling and self-healing mechanisms

## Human Partner Signals (escalate to human)
- **Production experiment approval** — First production chaos experiment requires stakeholder buy-in
- **Unexpected system behavior** — System reacts to failure in an unanticipated way → architecture review
- **Data integrity risk** — Experiment could corrupt data → need safeguard verification
- **Customer impact** — Experiment may cause user-visible degradation → communication plan needed

## Pipeline
1. Define: establish steady-state hypothesis — what metrics define "normal" behavior
2. Design: select failure mode, blast radius, duration, and abort conditions
3. Verify: confirm observability captures all relevant metrics during experiment
4. Execute: run experiment in progressively larger blast radius (1 instance → 1 AZ → region)
5. Observe: compare system behavior against steady-state hypothesis during and after experiment
6. Analyze: identify gaps — what failed that shouldn't have? What recovered that might not next time?
7. Remediate: fix discovered weaknesses, improve observability, update runbooks
8. Repeat: schedule regular chaos experiments (Game Days) to prevent regression

## Verification Checklist
- [ ] Steady-state hypothesis defined with measurable metrics before experiment
- [ ] Blast radius limited and controlled (start with 1 instance/1%)
- [ ] Abort condition defined and tested before experiment execution
- [ ] Observability confirmed — all relevant metrics visible during experiment
- [ ] Recovery verified — system returns to steady state after experiment ends
- [ ] Experiment findings documented with remediation items tracked
- [ ] Game Day schedule established (quarterly recommended)



## Output Schema (MANDATORY)

```markdown
# [Review Type]: [Target]
## CRITICAL Findings
### C1: [Title] | [Framework]: [ID]
**Finding:** [What]
**Impact:** [Why matters]
**Fix:** [Concrete fix — code, not words]
## HIGH Findings
[Same format]
## MEDIUM / LOW
[Same format]
## Summary
- CRITICAL: N, HIGH: N, MEDIUM: N
- Verdict: PASS/FAIL
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague fixes ("add validation") | Not actionable | Show exact code |
| Missing severity tag | No prioritization | Always CRITICAL/HIGH/MEDIUM/LOW |
| Single-focus blindness | Misses related issues | Scan ALL categories separately |
| No framework mapping | Can't track compliance | Map to OWASP/MITRE/NIST |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Finding completeness | Missed major issues | Found most | All issues found |
| Severity accuracy | None/random | Some correct | All correctly rated |
| Fix quality | "Fix it" | Partial code | Complete, runnable fix |
| Framework mapping | None | Some mapped | All mapped to framework |
| Output format | Free text | Partial structure | Schema-compliant |

**Pass: 8/10**
## Related Skills
- `mutation-testing` — Mutation testing for code; chaos engineering for infrastructure
- `load-testing` — Chaos + load testing reveals failure modes under stress
- `systematic-debugging` — Debugging unexpected chaos experiment results
- `observability-pro` — Observability is a prerequisite for chaos engineering
