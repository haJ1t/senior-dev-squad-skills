---
name: roadmap-prioritizer
description: "Data-driven roadmap prioritization using RICE/ICE/MoSCoW, dependency mapping, and capacity planning. Use when scoring and ordering a product backlog."
version: 1.0.0
platforms: [linux, macos]
---

# Roadmap Prioritizer

## What It Does
Prioritizes product initiatives using data-driven frameworks (RICE, ICE, MoSCoW, Cost of Delay). Facilitates stakeholder alignment, maps initiative dependencies to avoid deadlocks, sequences work for maximum value delivery, and performs capacity planning against team velocity to produce realistic, defensible roadmaps.

## Iron Laws (NEVER violate)
1. **Score before debate** — Calculate objective scores before subjective prioritization discussions. Data anchors the conversation.
2. **Capacity is a hard constraint** — Never plan more work than team velocity can deliver. Overcommitment destroys credibility.
3. **One priority framework** — Pick ONE framework (RICE, ICE, etc.) and apply it consistently. Mixing frameworks = gaming the system.
4. **Dependencies before dates** — Resolve dependency chains before committing to dates. Dates without dependency resolution are fiction.

## Red Flags (STOP immediately)
- **HiPPO override** — Highest Paid Person's Opinion overrides data-driven scores → prioritization theater
- **Everything is P0** — If everything is critical, nothing is. Force distribution: max 20% P0, 30% P1, 50% P2/P3.
- **Dependency chain > 3 deep** — Initiative depends on A→B→C→D → too fragile; restructure or accept risk
- **Zero capacity buffer** — Roadmap uses 100% of capacity → no room for bugs, incidents, or opportunities

## Common Rationalizations (self-deception)
- "We'll figure out dependencies later" → Undiscovered dependencies are the #1 cause of roadmap slip.
- "This is a special case, it doesn't need scoring" → Special cases multiply. Score everything or the system breaks.
- "The team can stretch for this quarter" → Stretch plans become baseline expectations. Capacity is capacity.

## When To Use
- Quarterly or sprint roadmap planning
- Stakeholder asks "why is X prioritized over Y?"
- Need to sequence 5+ initiatives with dependencies
- Capacity planning against known team velocity
- Resolving priority conflicts between stakeholders

## Human Partner Signals (escalate to human)
- **Strategic tradeoff** — Two initiatives are mutually exclusive due to resource constraints → executive decision
- **Stakeholder deadlock** — Two stakeholders with equal authority disagree on priority → escalate to shared manager
- **Scope vs timeline** — Only way to hit date is to cut scope; only way to keep scope is to push date → decision needed
- **Team health** — Capacity plan requires sustained overtime → unsustainable; flag for leadership

## Pipeline
1. Collect: gather all candidate initiatives with descriptions, goals, and rough effort estimates
2. Score: apply chosen framework consistently (Reach × Impact × Confidence ÷ Effort for RICE)
3. Map: build dependency graph, identify blockers and prerequisite chains
4. Sequence: order by score, respecting dependencies and capacity constraints
5. Challenge: stress-test with stakeholders — what if we're wrong? What's the cost of delay?
6. Commit: publish roadmap with confidence levels (committed vs planned vs aspirational)
7. Track: monitor progress, update scores as new information emerges, re-prioritize quarterly

## Verification Checklist
- [ ] All initiatives scored with the same framework (no mixed methods)
- [ ] P0 items ≤ 20% of total initiatives
- [ ] Dependency graph is a DAG with no chain deeper than 3
- [ ] Capacity plan includes ≥15% buffer for unplanned work
- [ ] Roadmap published with confidence levels (committed/planned/aspirational)
- [ ] Cost of delay calculated for any initiative deferred beyond current quarter



## Output Schema (MANDATORY)

Structure your response with:
1. **Analysis** — What you found/designed
2. **Concrete output** — Code, YAML, tables (not just descriptions)
3. **Tradeoffs/risks** — What you chose and why, what could go wrong
4. **Verification** — How to confirm correctness

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague recommendations | Not actionable | Concrete examples, specific steps |
| Missing tradeoffs | One-sided analysis | Every choice: "X over Y because..." |
| "Consider doing X" | No commitment | "Do X. Why: [reason]" |
| No verification criteria | Can't confirm quality | "Verify by: [test/check]" |
| Generic response | Not tailored | Domain-specific vocabulary, exact tool names |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Specificity | Generic advice | Some specifics | Concrete, actionable output |
| Tradeoff awareness | None | Mentioned | Documented with alternatives |
| Output format | Free text | Partial structure | Structured, scannable |
| Verification | None | Vague | Specific test/criteria |
| Domain accuracy | Wrong terms | Mostly correct | Precise domain vocabulary |

**Pass: 7/10**
## Related Skills
- `opportunity-solver` — Scored opportunities are the input to prioritization
- `validation-designer` — Validated hypotheses get higher confidence scores
- `user-story-refiner` — Prioritized initiatives become refined user stories
- `task-lifecycle-manager` — Roadmap items decompose into lifecycle-managed tasks
