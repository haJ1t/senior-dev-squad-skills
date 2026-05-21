---
name: multi-agent-debate
description: "Structured debate between multiple LLMs using Proposer→Opponent→Judge protocol for optimal solutions. Use when stress-testing a decision with adversarial reasoning."
version: 1.0.0
platforms: [linux, macos]
---

# Multi-Agent Debate

## What It Does
Orchestrates structured debates between multiple LLMs to find optimal solutions to complex problems. Uses a formal Proposer → Opponent → Judge protocol with round-based argumentation. Builds consensus through structured critique, preserves minority reports when consensus isn't reached, and produces a complete debate transcript as an audit trail for human review.

## Iron Laws (NEVER violate)
1. **Role integrity** — Each model stays in its assigned role for the entire debate. Proposer advocates; Opponent critiques; Judge decides. No role-switching mid-debate.
2. **Evidence over rhetoric** — Every argument must cite specific evidence (code, data, precedent). Rhetorical flourishes without evidence are ignored by the Judge.
3. **Minority report preserved** — If consensus isn't reached, the minority position must be documented with equal prominence. Suppressed dissent is lost insight.
4. **Debate has an endpoint** — Maximum rounds defined upfront. Infinite debate is analysis paralysis. After N rounds, Judge issues final ruling.

## Red Flags (STOP immediately)
- **Ad hominem in debate** — A model critiques the other model rather than the argument → protocol violation; reset that round
- **Judge bias** — Judge consistently favors one model regardless of argument quality → judge rotation needed
- **Circular argument** — Round 3 rehashes Round 1 without new evidence → debate has converged; end it
- **Proposer-opponent collusion** — Models agree too quickly on a suboptimal solution → inject adversarial challenge

## Common Rationalizations (self-deception)
- "One model can play all three roles" → Self-critique is weaker than adversarial critique. Separate models for honest debate.
- "Debate takes too long for simple decisions" — True. Reserve debate for high-stakes, non-obvious decisions only.
- "Consensus means the answer is correct" — Consensus can mean shared blind spots. The process improves confidence, not certainty.

## When To Use
- High-stakes architectural decisions with multiple viable approaches
- Security design where adversarial thinking is critical
- Algorithm selection with tradeoffs (performance vs readability vs maintainability)
- User wants to stress-test an approach before committing
- Resolving disagreement between human team members (use AI debate as input)

## Human Partner Signals (escalate to human)
- **Persistent disagreement** — After max rounds, models still disagree → human tiebreaker needed
- **Novel domain** — Debate topic is outside all models' known expertise → human domain expert needed
- **Ethical dimension** — Debate touches on ethics, fairness, or societal impact → human values judgment required
- **Cost threshold** — Debate token usage exceeds budget → human decision: continue or accept current result

## Pipeline
1. Frame: define the decision to be made, success criteria, and debate constraints (max rounds, time limit)
2. Assign roles: select Proposer model (creative/generative strength), Opponent model (critical/analytical strength), Judge model (balanced/evaluative strength)
3. Round 1 — Propose: Proposer presents solution with supporting evidence
4. Round 1 — Oppose: Opponent critiques with counter-evidence and alternative risks
5. Round 1 — Judge: Judge evaluates both arguments, identifies gaps, frames Round 2 question
6. Round N: iterate with focused sub-questions until convergence or max rounds
7. Final ruling: Judge issues decision with confidence score and key reasoning
8. Archive: save complete debate transcript with minority report if applicable

## Verification Checklist
- [ ] Roles assigned before debate begins (no mid-debate switching)
- [ ] Max rounds defined and enforced
- [ ] Every argument cites specific evidence (no unsupported claims)
- [ ] Judge rulings include reasoning, not just conclusions
- [ ] Minority report preserved when consensus not reached
- [ ] Complete debate transcript archived for audit
- [ ] Token budget tracked per debate and enforced

## Related Skills
- `cross-model-reviewer` — Cross-model review is a simpler form of multi-perspective evaluation
- `provider-router` — Selects which models participate in each debate role
- `code-reviewer` — Debate format applied to contentious code review decisions
- `systematic-debugging` — Debate format for competing root cause hypotheses
