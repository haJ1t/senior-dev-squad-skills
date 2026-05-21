---
name: skill-marketplace
description: "Internal skill discovery, installation, version management, context-aware skill suggestions. Use when finding or installing skills for a project."
version: 1.0.0
platforms: [linux, macos]
---

# Skill Marketplace

## What It Does
Provides an internal marketplace for discovering, installing, rating, and managing agent skills. Agents can search/browse available skills, check version compatibility, view usage statistics, and receive context-aware skill suggestions based on the current task. Acts as the package manager for the skill ecosystem.

## Iron Laws (NEVER violate)
1. **Version pinning** — Every installed skill must be pinned to a specific version. No floating "latest" in production.
2. **Compatibility gate** — Skill installation must verify compatibility with current agent runtime version and dependency skills.
3. **Provenance verification** — Every skill must have verifiable origin (author, repo, hash). No anonymous skills.
4. **Breaking change alert** — Any skill update with breaking changes must notify all dependent skills and the human.

## Red Flags (STOP immediately)
- **Dependency conflict** — Skill A requires skill B v1, skill C requires skill B v2 → resolution required
- **Orphaned skill** — Skill has no maintainer, no updates in 6+ months → mark as deprecated
- **Version rollback** — Skill update causes regression → auto-rollback to last known good version
- **Circular dependency** — Skill A depends on B, B depends on A → architecture violation

## Common Rationalizations (self-deception)
- "Latest version is always best" → Breaking changes in latest can destroy workflows. Pin versions.
- "This skill is simple, skip the dependency check" → Transitive dependencies cause hidden breaks.
- "We don't need ratings, just install everything" → Unrated skills accumulate technical debt silently.

## When To Use
- User asks "what skills do I have for X?"
- Installing a new skill from the ecosystem
- Checking if an update is safe to apply
- Agent auto-suggests relevant skills based on task context
- Managing skill dependencies across a large ecosystem

## Human Partner Signals (escalate to human)
- **Breaking change approval** — Skill update will break 3+ dependent skills → human must approve
- **License conflict** — New skill license incompatible with project license → legal review needed
- **Security advisory** — Installed skill version has known CVE → force upgrade or remove
- **Unmaintained dependency** — Critical dependency skill abandoned by maintainer → human must decide fork/replace

## Pipeline
1. Discover: search/browse marketplace by category, keyword, rating, popularity
2. Analyze: check compatibility matrix, dependency tree, breaking change impact
3. Install: download skill, verify hash, register in skill registry, update dependency graph
4. Suggest: based on task context, recommend skills that could improve outcomes
5. Maintain: track installed versions, notify of updates, flag deprecated/unmaintained skills
6. Audit: periodic scan for CVEs, license issues, orphaned skills

## Verification Checklist
- [ ] All installed skills have pinned versions (no floating tags)
- [ ] Dependency graph is a DAG with no cycles
- [ ] Every skill has verified provenance (author + hash matched)
- [ ] Breaking change impact analysis runs before any update
- [ ] Context-aware suggestions fire for relevant task types
- [ ] Security audit flags any skill with known CVEs



## Output Schema (MANDATORY)

```yaml
# Orchestration Plan
project: {goal, constraints, success_criteria, token_budget}
epics: [{id, name, hours, depends_on, budget, stories: [{tasks, acceptance}]}]
dependency_dag: [ASCII or mermaid]
critical_path: [hours]
squads: [{id, epic, roles, budget, handoff_contracts}]
timeline: {day_N: {squads, milestones}}
monitoring: {interval, alerts: [token, stall, circuit_breaker]}
recovery: {patterns per failure type}
post_mortem: {planned_vs_actual, lessons, metrics}
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| No decomposition | Vague plan | Project→Epic→Story→Task chain |
| Missing DAG | Hidden dependencies | Visual dependency graph + critical path |
| No token budget | Resource blind | Per-squad token estimate |
| "Retry on failure" only | Incomplete recovery | Retry + fallback + escalate + circuit breaker |
| No monitoring | Flying blind | 3+ alerts with conditions |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Decomposition depth | None | Epics only | Epic→Story→Task |
| Dependency DAG | None | Text only | Visual + critical path |
| Token budgeting | None | Total only | Per-squad calculated |
| Squad design | "N squads" | Roles listed | Roles+budget+handoffs |
| Failure recovery | None | "Retry" | Retry+fallback+escalate+CB |
| Monitoring | None | 1 alert | 3+ with conditions |

**Pass: 8/12**
## Related Skills
- `agent-skill-package-authoring` — How to create skills that appear in this marketplace
- `hermes-agent-skill-authoring` — Hermes-specific skill authoring conventions
- `supply-chain-verifier` — Security scanning of skill dependencies
- `release-manager` — Version management and release workflow for skills
