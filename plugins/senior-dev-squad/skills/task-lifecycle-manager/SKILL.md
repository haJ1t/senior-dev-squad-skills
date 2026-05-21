---
name: task-lifecycle-manager
description: "Full task lifecycle management, epic decomposition, deployment tracking, dependency resolution. Use when managing tasks end-to-end across a project."
version: 1.0.0
platforms: [linux, macos]
---

# Task Lifecycle Manager

## What It Does
Manages the complete lifecycle of agent-executable tasks — from epic decomposition through execution to deployment verification. Tracks task status across a Kanban-style pipeline (backlog → in-progress → review → done), resolves dependency chains, handles blocked tasks, and auto-retries on transient failures with exponential backoff.

## Iron Laws (NEVER violate)
1. **Atomic tasks only** — Every task must be completable by a single agent in a single session. No multi-session tasks.
2. **Explicit dependencies** — Every blocking relationship must be declared. Implicit dependencies are bugs.
3. **Idempotent retry** — Any task retry must produce the same outcome. No double-deploy, no double-charge.
4. **Status is single source of truth** — Task status in the lifecycle manager overrides any agent's self-report.

## Red Flags (STOP immediately)
- **Circular block** — Task A blocked by B, B blocked by A → deadlock requiring human intervention
- **Zombie task** — Task in "in-progress" for >2x estimated duration → agent may have died silently
- **Status inversion** — Task marked "done" but verification fails → trust boundary violated
- **Dependency cascade** — 5+ tasks blocked by one failing task → architectural bottleneck

## Common Rationalizations (self-deception)
- "This task is almost done, no need to update status" → Stale status causes cascading blocks.
- "I'll handle the dependency manually" → Manual dependency management doesn't scale past 5 tasks.
- "Just retry it again, it'll work this time" → Blind retry without root cause wastes tokens.

## When To Use
- Any project with 5+ discrete tasks that have dependencies
- Multi-agent workflows where task handoff tracking is critical
- User wants automated retry on transient failures (API timeouts, rate limits)
- Need to track progress across multiple parallel workstreams

## Human Partner Signals (escalate to human)
- **Persistent failure** — Task fails 3+ retries with same error → root cause needs human analysis
- **Scope explosion** — Task estimated at 2h takes 8h+ → task wasn't properly decomposed
- **Priority conflict** — Two P0 tasks block each other → human must decide ordering
- **Resource starvation** — More tasks than available agent capacity for >1 hour

## Pipeline
1. Ingest: receive epic/user story, decompose into atomic tasks
2. Analyze: detect dependencies, estimate effort, assign priority (P0-P4)
3. Schedule: queue tasks respecting dependency DAG, agent capacity, priority
4. Execute: dispatch tasks to agents, monitor status, handle retries
5. Verify: run verification checks, update dependency graph, mark complete
6. Report: generate burndown, identify bottlenecks, surface risks

## Verification Checklist
- [ ] Task dependency graph is a DAG (no cycles)
- [ ] Every task has estimated duration and verification criteria
- [ ] Failed tasks auto-retry with exponential backoff (max 3 attempts)
- [ ] "Done" tasks pass verification before status update
- [ ] Zombie tasks detected and escalated within 2x estimated duration
- [ ] Burndown report shows accurate progress vs plan



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
- `squad-builder` — Tasks are assigned to squads built by squad-builder
- `agent-teammate` — Individual agents execute lifecycle-managed tasks
- `kanban-orchestrator` — Visual Kanban board representation of the same pipeline
- `subagent-driven-development` — Task lifecycle as the backbone of subagent workflows
