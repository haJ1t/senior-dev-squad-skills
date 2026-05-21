---
name: mutation-testing
description: "Mutation testing to measure test quality — kill mutants, identify weak tests, and improve test coverage effectiveness. Use when auditing test suite reliability."
version: 1.0.0
platforms: [linux, macos]
---

# Mutation Testing

## What It Does
Measures test suite quality through mutation testing — automatically introducing bugs (mutants) into source code and checking if tests catch them. Mutants that survive indicate gaps in test coverage or weak assertions. Provides a mutation score that is a stronger quality signal than code coverage, and generates specific recommendations for strengthening tests.

## Iron Laws (NEVER violate)
1. **Coverage ≠ quality** — 100% code coverage with 20% mutation score means tests execute code but don't verify behavior. Mutation score is the real metric.
2. **Every survived mutant is a bug waiting to happen** — A mutant that no test catches is a real bug that no test would catch. Fix the test gap.
3. **Equivalent mutants must be documented** — Mutants that can't be killed (semantically identical to original) must be explicitly marked equivalent with justification.
4. **Mutation testing in CI** — Run mutation tests in CI with a minimum score gate. Falling below the threshold fails the build.

## Red Flags (STOP immediately)
- **Mutation score < 60%** — Test suite is dangerously weak; prioritize strengthening
- **Surviving mutant cluster** — Many surviving mutants in one module → module has systemic testing gap
- **Timeout mutants** — Tests pass but take 10x longer with mutant → performance-sensitive code without timing assertions
- **Equivalent mutant ratio > 10%** — Too many unkillable mutants → mutation operators too aggressive or code too redundant

## Common Rationalizations (self-deception)
- "We have 90% code coverage, our tests are good" → Code coverage measures execution, not verification. Mutation score measures verification.
- "Mutation testing is too slow for CI" → Run on changed files only, use incremental mutation testing, or run nightly.
- "Equivalent mutants mean mutation testing is broken" → Equivalent mutants reveal code redundancy. They're a different signal, not noise.

## When To Use
- Auditing test suite quality beyond code coverage metrics
- Identifying specific weak tests that need strengthening
- Setting quality gates for critical code (auth, payments, data integrity)
- Comparing test effectiveness before/after refactoring
- Teaching developers what "good tests" actually means

## Human Partner Signals (escalate to human)
- **Test architecture change** — Mutation testing reveals need for fundamental test restructuring → team discussion
- **Resource tradeoff** — Achieving 80%+ mutation score requires significant test investment → prioritization call
- **Equivalent mutant review** — Large number of equivalent mutants needs human review → may indicate code smells
- **False confidence** — Team believed tests were strong; mutation score reveals weakness → expectations reset

## Pipeline
1. Configure: select mutation operators (arithmetic, logical, conditional, return value, etc.) and target files
2. Baseline: run initial mutation analysis to establish current mutation score
3. Analyze: review surviving mutants grouped by file and mutation type
4. Prioritize: rank modules by risk — high business impact + low mutation score first
5. Strengthen: add targeted tests to kill prioritized surviving mutants
6. Gate: set minimum mutation score threshold in CI (suggest starting at 70%, target 80%+)
7. Monitor: track mutation score trend over time; prevent regression

## Verification Checklist
- [ ] Mutation score measured and tracked per module
- [ ] Minimum mutation score threshold enforced in CI (≥70% recommended)
- [ ] All equivalent mutants documented with justification
- [ ] No module with business-critical logic below 60% mutation score
- [ ] Surviving mutants reviewed and triaged (fix test / mark equivalent / accept risk)
- [ ] Incremental mutation testing configured for PR workflows



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
- `test-engineer` — Test design and TDD practices that mutation testing validates
- `test-driven-development` — TDD cycle extended with mutation testing verification
- `chaos-engineer` — Mutation testing for code; chaos engineering for infrastructure
- `systematic-debugging` — Surviving mutants reveal debugging blind spots
