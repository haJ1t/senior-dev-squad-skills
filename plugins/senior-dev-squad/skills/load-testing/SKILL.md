---
name: load-testing
description: "Load and stress testing with k6/locust — performance baselines, capacity planning, and breaking point discovery. Use when load testing or benchmarking services."
version: 1.0.0
platforms: [linux, macos]
---

# Load Testing

## What It Does
Designs and executes load, stress, soak, and spike tests to validate system performance under realistic and extreme conditions. Uses k6 or Locust to generate configurable load patterns, measures performance against defined SLAs (latency p50/p95/p99, error rate, throughput), identifies breaking points, and provides capacity planning recommendations. Integrates performance testing into CI/CD to prevent performance regressions.

## Iron Laws (NEVER violate)
1. **SLA before load** — Define acceptable performance before running tests. "As fast as possible" is not measurable. p95 < 200ms, error rate < 0.1%.
2. **Production-like data and traffic** — Load tests with synthetic data and uniform traffic patterns are fantasy. Use production traffic replay or realistic distributions.
3. **Test environment = production scaled-down** — Load test environment must match production configuration. Different instance types = invalid results.
4. **Never load test without observability** — Running load without monitoring CPU, memory, DB connections, and queue depth is testing blind.

## Red Flags (STOP immediately)
- **Performance cliff** — Throughput crashes at specific concurrency level → resource exhaustion or contention; identify bottleneck
- **Error rate spike** — 1% errors at low load, 20% at high load → system degrades non-linearly
- **Resource leak** — Memory/connections grow monotonically during soak test → leak will cause production outage
- **Cascading failure** — Load test takes down dependent services → system lacks proper isolation/circuit breakers

## Common Rationalizations (self-deception)
- "We don't have enough traffic to need load testing" → Low traffic systems fail harder under unexpected load. Black Friday doesn't warn you.
- "We tested in staging with 10 users" → 10 users don't reveal connection pool exhaustion at 1000 concurrent users.
- "Our cloud will auto-scale" → Auto-scaling has a ramp-up time. Spike tests reveal if you survive the gap.

## When To Use
- Preparing for high-traffic events (launch, promotion, seasonal peak)
- Capacity planning — how many users can current infrastructure support?
- Detecting performance regressions in CI/CD
- Validating auto-scaling configuration
- Finding memory leaks and resource exhaustion through soak testing
- Stress testing to find system breaking point

## Human Partner Signals (escalate to human)
- **Breaking point below target** — System fails below required capacity → architecture change or infrastructure investment
- **Cost inflection** — Meeting SLA requires 3x infrastructure → cost optimization vs performance tradeoff
- **Third-party bottleneck** — External dependency is the bottleneck → vendor escalation or architecture change
- **Production load test** — Need to test in production for accurate results → stakeholder approval and communication plan

## Pipeline
1. Define: establish performance SLAs — latency percentiles, error rate, throughput targets
2. Design: create load profiles — ramp-up, constant load, spike, soak; realistic user scenarios
3. Script: write test scripts in k6 or Locust — user flows, think times, data parameterization
4. Environment: configure test environment to match production at reduced scale
5. Execute: run load profiles in order — baseline → load → stress → soak → spike
6. Analyze: compare results against SLAs, identify bottlenecks, correlate with system metrics
7. Report: performance test report with pass/fail against SLAs, bottleneck analysis, capacity prediction
8. Automate: integrate baseline load tests into CI/CD for regression detection

## Verification Checklist
- [ ] Performance SLAs defined before load test execution (p50/p95/p99 latency, error rate, throughput)
- [ ] Test scripts use realistic data distributions (not uniform)
- [ ] Test environment matches production configuration at reduced scale
- [ ] Full observability stack active during tests (CPU, memory, DB, queues, app metrics)
- [ ] Soak test runs for ≥2 hours to detect memory leaks
- [ ] Spike test verifies auto-scaling response time
- [ ] Breaking point documented — max concurrent users before SLA violation
- [ ] Baseline load test integrated into CI/CD pipeline



## Output Schema (MANDATORY)

```markdown
# [Test Type]: [Target]
## Findings
### [ID]: [Title]
**Scenario:** [Given/When/Then]
**Expected:** [What should happen]
**Actual:** [What happens / what could break]
**Severity:** [CRITICAL/HIGH/MEDIUM]
**Fix:** [Concrete fix]
## Summary
- Total findings: N
- By severity: C=, H=, M=
- Coverage: [dimensions/categories covered]
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Happy path only | Misses failures | Test error/edge/empty states |
| Vague scenarios | Not reproducible | Exact Given/When/Then |
| Missing severity | Can't prioritize | CRITICAL/HIGH/MEDIUM on every finding |
| "Fix later" | Never gets fixed | Concrete fix with every finding |
| Single dimension | Blind spots | Cover all categories systematically |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Coverage breadth | 1-2 dimensions | 4-6 | All categories |
| Scenario specificity | Vague | Partial | Exact Given/When/Then |
| Severity accuracy | None | Some | All correctly rated |
| Fix quality | "Fix it" | Partial | Complete fix |
| Reproducibility | Can't reproduce | Hard | Easy to reproduce |

**Pass: 8/10**
## Related Skills
- `chaos-engineer` — Combine load + chaos to test resilience under stress
- `performance-engineer` — Performance optimization based on load test findings
- `observability-pro` — Observability infrastructure for load test monitoring
- `devops-release-engineer` — Auto-scaling and infrastructure configuration validation
