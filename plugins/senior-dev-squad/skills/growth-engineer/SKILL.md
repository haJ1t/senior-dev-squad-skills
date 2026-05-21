---
name: growth-engineer
description: "Data-driven growth engineering — funnels, A/B testing, viral loops, retention, and PLG metrics. Use when designing or analyzing growth experiments."
version: 1.0.0
platforms: [linux, macos]
---

# Growth Engineer

## What It Does
Applies engineering rigor to growth — building measurement infrastructure, running A/B tests, analyzing conversion funnels, optimizing viral coefficients, and tracking retention cohorts. Focuses on Product-Led Growth (PLG) metrics: activation, adoption, retention, expansion, and referral loops.

## Iron Laws (NEVER violate)
1. **Sample size before conclusion** — Never declare a winner until statistical significance (p < 0.05, min sample size met).
2. **One variable at a time** — A/B tests change exactly one variable. Multi-variate tests require factorial design.
3. **Metric hierarchy** — North Star Metric > OKRs > vanity metrics. Never optimize for a metric that doesn't map to NSM.
4. **Peeking penalty** — Checking A/B test results early invalidates statistical validity. Set duration, don't peek.

## Red Flags (STOP immediately)
- **Metric manipulation** — Change that improves metric but harms user experience → gaming the metric
- **Simpson's paradox** — Aggregate metric improves but every segment worsens → hidden segmentation issue
- **p-hacking** — Running multiple tests and cherry-picking significant ones → multiple comparison problem
- **Cannibalization** — New feature grows but kills existing revenue stream → net negative

## Common Rationalizations (self-deception)
- "The trend is clear, we don't need full sample size" → Early trends reverse 30% of the time. Wait for significance.
- "This metric is going up, we're winning" → Vanity metrics rise while retention falls. Check the full hierarchy.
- "We'll instrument later, ship first" → Without instrumentation, you're flying blind. Build measurement in from day 0.

## When To Use
- Setting up growth experimentation infrastructure
- Analyzing conversion funnel drop-off points
- Designing and running A/B tests
- Calculating viral coefficient and optimizing referral loops
- Building retention cohort analysis
- Setting up PLG metrics dashboards

## Human Partner Signals (escalate to human)
- **Revenue impact** — Test may affect paying users' experience → stakeholder approval needed
- **Ethical boundary** — Growth tactic approaches dark pattern territory → ethics review
- **Statistical ambiguity** — Results are borderline significant → decision requires business judgment
- **Resource tradeoff** — Growth experiment requires significant engineering investment → prioritization call

## Pipeline
1. Instrument: set up event tracking, funnel analytics, cohort analysis, attribution
2. Analyze: identify biggest drop-off points, segment users, calculate baseline metrics
3. Hypothesize: form testable hypotheses with predicted impact and measurement plan
4. Experiment: design A/B test, calculate required sample size and duration, implement
5. Measure: monitor experiment without peeking, calculate statistical significance at end
6. Ship or Kill: roll out winners to 100%, document learnings from failures
7. Iterate: compound wins, build growth loops, continuously raise the baseline

## Verification Checklist
- [ ] North Star Metric defined and all experiments map to it
- [ ] A/B testing infrastructure supports proper randomization and isolation
- [ ] Sample size calculator used before every experiment launch
- [ ] Peeking prevention enforced (no result checks before planned duration)
- [ ] Retention cohort analysis running for at least 90-day windows
- [ ] Experiment log tracks all tests including failures (for organizational learning)

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

## Related Skills
- `content-strategist` — Content performance data feeds growth analysis
- `validation-designer` — Growth experiments are validation experiments applied to growth metrics
- `social-media-manager` — Social channels are growth channels with measurable conversion
- `weights-and-biases` — Experiment tracking infrastructure for ML/growth experiments
