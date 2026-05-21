---
name: epic-orchestrator
description: "Multi-squad orchestration: task decomposition, resource optimization, routing, error recovery, cross-squad dependencies. Use when planning or managing large epics."
version: 2.0.0
platforms: [linux, macos]
---

# Epic Orchestrator v2

## Overview

Epic Orchestrator is the orchestration skill for large-scale projects that run for days or weeks, require 5-50+ sub-agents, and involve the coordinated effort of multiple independent squads. **Benchmark-proven: without structured decomposition rules, models produce vague timelines with no dependency DAGs, token budgets, or failure recovery strategies.**

**Core Principle:** FOR SMALL TASKS, USE SUBAGENT-ORCHESTRATOR; FOR LARGE TASKS, USE EPIC ORCHESTRATOR.

## Iron Laws (NEVER Violate)

1. **Never begin without epic decomposition** — Do not spawn the first sub-agent before breaking the project down into epics, epics into stories, and stories into atomic tasks.
2. **Give each squad only the context it requires** — Each squad receives memory and context restricted to its assigned epic.
3. **Each squad must be able to work independently** — If two squads block each other's output for more than 1 hour, the decomposition was designed incorrectly.
4. **Failure is a data point, not an endpoint** — Every error is routed through automatic retry, circuit breaker, and fallback patterns.
5. **Every epic produces a learning artifact** — Conduct a post-mortem, update the pattern catalog, and define new skills as necessary.
6. **Token budgets are hard contracts** — Enforce a maximum token limit for each squad: issue a warning at 80%, and halt execution at 95%. Budget overruns indicate decomposition failures.
7. **Monitoring is always active** — Maintain a 15-minute check interval; 3 consecutive silent periods triggers a stall alarm and activates the automatic circuit breaker.

## MANDATORY Output Schema

Every orchestration plan MUST conform strictly to the following YAML format:

```yaml
# EPIC ORCHESTRATION PLAN
project:
  goal: "[Single-sentence description]"
  constraints: [list of constraints]
  success_criteria: [measurable criteria]
  total_token_budget: "[e.g., 8M]"
  max_concurrent_squads: [number]

epics:
  - id: epic-1
    name: "[Name]"
    estimated_hours: [number]
    depends_on: [epic_id or empty]
    token_budget: "[e.g., 800K]"
    squad_profile: "[backend/frontend/data/security]"
    stories:
      - id: S1.1
        tasks: [list of atomic tasks]
        acceptance: [acceptance criteria]

dependency_dag: |
  [Mermaid or ASCII DAG diagram]

critical_path: [longest dependency chain as hours]

squads:
  - id: squad-[name]
    epic: [assigned epic]
    roles: [architect, implementer, reviewer, tester]
    token_budget: "[e.g., 500K]"
    max_retries_per_task: 3
    handoff_contracts: [format, SLA, on_stale behavior]

timeline:
  day_1: {active_squads: [], milestones: []}
  day_2: {active_squads: [], milestones: []}
  ...

monitoring:
  check_interval: "15m"
  alerts:
    - token_warning: "token_used > 0.8 * budget"
    - squad_stall: "0 tasks_completed in 3 check_intervals"
    - circuit_breaker: "3 consecutive failures"

recovery_patterns:
  transient_error: {pattern: retry_with_backoff, max: 3}
  squad_death: {pattern: respawn_with_checkpoint, max_respawns: 2}

post_mortem_template:
  planned_vs_actual: {token, time, quality}
  lessons: [list of patterns]
  metrics_for_future: {complexity_score, token_per_story, optimal_squad_size}
```

## LLM Anti-Patterns (BENCHMARK FINDINGS)

| Anti-Pattern | Model Error | Countermeasure |
|-------------|-------------|----------------|
| **Vague timeline** | "Day 1-2: Setup, Day 3-5: Migration" | Every day: active_squads + milestones + deliverables |
| **No token budget** | Budget never calculated | For each squad: context_window × turns × sub-agents = estimated tokens |
| **Missing DAG** | "Epic 2 depends on Epic 1" (plain text only) | Render: Mermaid DAG, calculate critical path |
| **No failure plan** | "If something fails, we'll fix it" | For each epic: retry strategy + fallback + escalation path |
| **Squad over-staffing** | 8 agents assigned to a single epic | Ideal size is 3-5. 7+ = coordination cost > work output |
| **Forgotten monitoring** | No alert rules defined | Define at least 3 alerts: token, stall, circuit_breaker |
| **No post-mortem** | Proje finished, next task | Perform planned_vs_actual + lessons + metrics_for_future at the end of every epic |

## Few-Shot Examples (MANDATORY Reference)

### ❌ BAD Output

```markdown
## Epic Orchestration Plan
Day 1-3: Extract services
Day 4-5: Test and deploy
Squads: 3 squads of 2-3 devs each
```
**Why it is bad:** No epic decomposition, no dependency DAG, no token budgeting, no monitoring, and no failure recovery defined.

### ✅ GOOD Output

```yaml
project:
  goal: "Migrate 250K-line Rails monolith to microservices"
  constraints: ["zero-downtime", "PCI-DSS for payments", "maintain existing API contracts"]
  success_criteria:
    - "All 4 bounded contexts independently deployable"
    - "PCI-DSS audit passed on payment context"
    - "Existing API contracts unchanged (contract tests pass)"
    - "Rollback to monolith possible within 15 minutes"
  total_token_budget: "6M"
  max_concurrent_squads: 3

epics:
  - id: epic-1
    name: "Foundation & Infrastructure"
    estimated_hours: 16
    depends_on: []
    token_budget: "600K"
    squad_profile: "devops"
    stories:
      - id: S1.1
        name: "Service template + CI/CD"
        tasks: [create-docker-template, setup-github-actions, health-check-endpoint, deploy-to-staging]
        acceptance: "New service can be created from template and deployed to staging in under 10 minutes"
      - id: S1.2
        name: "API Gateway + Service Mesh"
        tasks: [deploy-kong, configure-mtls, setup-rate-limiting, configure-routes]
        
  - id: epic-2
    name: "User/Auth Context Extraction"
    estimated_hours: 24
    depends_on: [epic-1]
    token_budget: "1.2M"
    squad_profile: "backend"
    
  - id: epic-3
    name: "Orders Context Extraction"  
    estimated_hours: 32
    depends_on: [epic-1]
    token_budget: "1.5M"
    squad_profile: "backend"
    
  - id: epic-4
    name: "Payments Context Extraction (PCI-DSS)"
    estimated_hours: 40
    depends_on: [epic-1, epic-2]
    token_budget: "2M"
    squad_profile: "backend+security"
    
  - id: epic-5
    name: "Notifications Context + Integration Testing"
    estimated_hours: 20
    depends_on: [epic-2, epic-3, epic-4]
    token_budget: "700K"
    squad_profile: "fullstack"

dependency_dag: |
  epic-1 (Foundation)
    ├── epic-2 (Auth) ──┐
    ├── epic-3 (Orders) ─┤── epic-5 (Integration)
    └── epic-4 (Payments) ┘        ↑
         ↑ (depends on epic-2 for auth)

critical_path: epic-1 → epic-2 → epic-4 → epic-5 = 100 hours (~4 days)

squads:
  - id: squad-backend
    epic: epic-2  # then epic-3
    roles: [architect, 2x implementer, reviewer, tester]
    token_budget: "1.2M"
    max_retries_per_task: 3
    
  - id: squad-payments
    epic: epic-4
    roles: [architect, implementer, security-reviewer, tester]
    token_budget: "2M"
    handoff_contracts:
      - from: squad-backend
        artifact: "auth-token-format"
        format: "OpenAPI spec"
        sla: "updated within 1 hour of change"

monitoring:
  check_interval: "15m"
  alerts:
    - token_warning: {condition: "token_used > 0.8 * budget", action: "notify + scope_review"}
    - squad_stall: {condition: "0 tasks in 3 intervals", action: "ping_commander + root_cause"}
    - circuit_breaker: {condition: "3 consecutive failures", action: "pause + notify_human"}

recovery_patterns:
  data_corruption: {pattern: "rollback_to_checkpoint", trigger: "hash_mismatch"}
  squad_death: {pattern: "respawn_with_snapshot", max_respawns: 2}
  dependency_timeout: {pattern: "use_stub", max_wait: "2h"}
```

## Model-Specific Calibration

| Model | Tendency | Calibration |
|-------|---------|-------------|
| **Claude Sonnet 4** | Extremely structural plans, draws DAGs naturally but sometimes adds excessive detail | "Keep each epic description to 3-5 lines max — detail goes in stories" |
| **GPT-4o** | Realistic timelines, assigns squad roles well but tends to skip token budgets | "Calculate token budget for EVERY squad: context_window × turns × subagents" |
| **Gemini 2.5 Pro** | Concise, excellent monitoring rules, but weaker failure recovery strategies | "For each epic, define: retry strategy + fallback + escalation path" |
| **DeepSeek V3** | Strong dependency DAG, but tends to omit the post-mortem templates | "Always include post_mortem_template with planned_vs_actual + lessons" |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| **Epic decomposition** | No division into epics | Epics defined but no stories/tasks | Complete Epic $\rightarrow$ Story $\rightarrow$ Task chain |
| **Dependency DAG** | None | Plain text "X depends on Y" | Mermaid/ASCII DAG + calculated critical path |
| **Token budgeting** | Not calculated | Total project budget only | Calculated separately for each squad |
| **Squad design** | "3 squads" | Roles listed | Roles + budget + handoff contracts defined |
| **Timeline** | "5 days" | Divided into days | Daily breakdown: active_squads + milestones |
| **Failure recovery** | None | Vague "retry" | Retry + fallback + escalation + circuit breaker |
| **Monitoring rules** | None | 1 alert defined | Minimum 3 alerts with specific conditions |
| **Post-mortem** | None | Simple "lessons learned" | Complete template: planned_vs_actual + lessons + future metrics |

**Pass: 12/16**

- **Token budget exhaustion signal** — If estimated token usage exceeds 80% of budget, instantly prioritize or reduce scope.
- **Inter-squad deadlock** — If Squad A blocks on Squad B, and Squad B blocks on Squad A: flatten the dependency graph by introducing stubs/mocks.
- **Stall alert** — If no completed tasks are generated in 3 check intervals (15 mins each), pause all squads and conduct root-cause analysis.
- **Context leakage** — If a squad's context contains irrelevant details from other squads, re-establish context isolation and restart the squads.
- **Repetitive failure loops** — If the same bug type occurs 3 times across different squads, pause, extract the fix pattern, and distribute it to all squads.
- **Human intervention bottleneck** — If more than 3 tasks are blocked waiting for human input, the epic decomposition or squad escalation strategy is flawed.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "This project is too simple, epic decomposition is overkill" | What starts simple today easily scales to 3 epics and 15 stories tomorrow. Plan first. |
| "We will resolve inter-squad dependencies as we go" | Resolving dependencies ad-hoc is a direct route to project deadlock. Map them in a DAG. |
| "Estimating token budgets is a waste of time" | 70% of projects launched without token budgeting stall due to context exhaustion. |
| "Let's run 10 squads simultaneously to speed up delivery" | The coordination cost of 10 concurrent squads consumes twice the output speed of 5 squads. |
| "We will conduct the post-mortem once the project finishes" | At the end of the project, exhaustion sets in and critical lessons are forgotten. Run post-mortems after each epic. |
| "Let's give all squads access to the entire repository" | Spawning 50 sub-agents with 100K token contexts consumes 5M tokens immediately. Budget will run out. |

## When To Use

**USE WHEN:**
- The project can be divided into 5+ independent workflows (each with at least 3-4 sub-tasks).
- Total estimated token usage is 1M+ (exceeds single-agent context limits).
- The work requires distinct areas of expertise (e.g., frontend squad + backend squad + DevOps squad + security squad).
- Time is critical and parallel execution is required (e.g., executing 3 days of work in 1 day).
- The project runs for multiple days and requires precise milestone/checkpoint tracking.
- Similar projects were completed successfully, providing valid post-mortem patterns.

**DO NOT USE (use `subagent-orchestrator` instead):**
- The work can be divided into 3-5 sub-tasks and a single area of expertise is sufficient.
- Estimated token usage is under 200K.
- All tasks are strictly linear (parallelism is impossible).
- The work completes in 1-2 hours.
- A single squad is sufficient.

**NEVER USE (delegate to human instead):**
- The project scope is completely undefined (run `project-discovery` first).
- Critical business decisions are still outstanding (run `opportunity-solver` + `validation-designer` first).
- Domain knowledge is entirely absent (run `research-first` to discover domain context first).

## Pipeline (Workflow — 10 Phases)

### Phase 0: Project Ingestion and Scoping

**NO SUB-AGENTS ARE SPAWNED IN THIS PHASE.** Analysis only.

1. **Parse Project Brief** — Identify goals, constraints, deadlines, budget, and quality requirements.
2. **Validate Scope** — Resolve ambiguities using clear clarifying questions.
3. **Define Success Criteria** — Draft testable, measurable success conditions.
4. **Record Constraints** — Log mandatory technologies, design decisions, and non-negotiable elements.

```yaml
project_brief:
  goal: "Migrate e-commerce billing to Stripe"
  constraints:
    - "Zero downtime"
    - "PCI-DSS compliance must be preserved"
    - "Complete within 3 days"
  budget:
    max_tokens: "8M"
    max_squads: 5
    max_concurrent_squads: 3
  success_criteria:
    - "All payment flows active on the new system"
    - "Rollback scenario verified"
    - "Legacy system completely decommissioned"
    - "PCI-DSS compliance audit passed"
```

### Phase 1: Epic Decomposition

Break down the project into **epics**, epics into **stories**, and stories into **atomic tasks**.

1. **Define Epics** — Scope 1-3 day work packages that produce independent, testable value.
2. **Break into Stories** — Write user stories in the INVEST format.
3. **Define Atomic Tasks** — Ensure each story is composed of tasks that 3-5 sub-agents can complete in 2-3 turns.
4. **Draw Dependency DAG** — Establish which epics block others and which can run in parallel.
5. **Calculate Critical Path** — The longest dependency path defines the minimum duration of the project.

```yaml
epics:
  - id: epic-1
    name: "Stripe API Integration"
    estimated_hours: 24
    depends_on: []
    stories:
      - id: S1.1
        name: "Stripe SDK Installation & Configuration"
        tasks: [setup-sdk, configure-webhooks, test-connectivity]
      - id: S1.2
        name: "Payment Intent Endpoint"
        tasks: [design-api, implement-create-intent, add-validation, write-tests]
    squad_profile: "backend"

  - id: epic-2
    name: "Migration from Legacy System"
    estimated_hours: 36
    depends_on: [epic-1]
    stories:
      - id: S2.1
        name: "Data Migration Scripts"
        tasks: [audit-existing-data, write-migration-script, dry-run, validate-integrity]
    squad_profile: "data-engineering"

  - id: epic-3
    name: "Update Frontend Payment Flows"
    estimated_hours: 20
    depends_on: [epic-1]
    can_start_after: "S1.1"  # Can start as soon as SDK configuration is complete
    stories: [...]
    squad_profile: "frontend"

critical_path: [epic-1, epic-2]  # 60 hours
parallel_opportunities:
  - [epic-1, epic-4]  # Epics 1 and 4 can start concurrently
  - [epic-3, epic-5]  # Epics 3 and 5 can run in parallel once S1.1 completes
```

### Phase 2: Squad Design

Design the optimal squad composition for each epic.

1. **Determine Role Requirements** — Identify needed expertise (e.g., architect, implementer, reviewer, tester, security, devops).
2. **Optimize Squad Size** — 3-5 sub-agents is ideal. 2 is too few (lacks rigorous reviews); 7+ is too many (coordination cost > output).
3. **Assign Squad Leader** — Establish a single decision-maker (usually the architect role) per squad.
4. **Write Handoff Contracts** — For all cross-squad data exchanges, define the format, SLA, and stale/error behaviors.
5. **Allocate Token Budgets** — Allocate token quotas based on epic complexity.

```yaml
squads:
  - id: squad-backend
    epic: epic-1
    commander_role: "architect"
    roles:
      - architect: "API design, Stripe integration patterns"
      - implementer: "Endpoint implementation"
      - reviewer: "Security and error handling reviews"
      - tester: "Integration tests with mock Stripe API"
    token_budget: "800K"
    max_retries_per_task: 3
    escalate_on: ["circuit_breaker_open", "dependency_timeout", "quality_gate_failed"]

  - id: squad-data
    epic: epic-2
    commander_role: "data-engineer"
    roles:
      - data-engineer: "Migration script, data verification"
      - reviewer: "Data integrity verification"
      - tester: "Dry-run and rollback testing"
    token_budget: "600K"
    handoff_contracts:
      - from: squad-backend
        artifact: "stripe-customer-id-mapping"
        format: "JSON (customer_id → stripe_customer_id)"
        sla: "Update within 5 minutes"
        on_stale: "retry 3x, then escalate"

  - id: squad-frontend
    epic: epic-3
    commander_role: "frontend-senior"
    can_start_trigger: "epic-1.story.S1.1.status == 'completed'"
    roles: [...]
    token_budget: "500K"
```

### Phase 3: Resource Planning and Optimization

1. **Simulate Token Budgets** — Estimate token consumption (context window × turns × sub-agent count).
2. **Create Timeline** — Break down daily active squads and milestones.
3. **Identify Bottlenecks** — Identify the critical path. Can resources be shifted to optimize it?
4. **Map Parallelism** — Identify concurrent execution windows.

```yaml
resource_plan:
  total_token_budget: "8M"
  allocated: "1.9M"  # Initial assignment
  reserve: "6.1M"    # Reserved for retries, escalations, or unexpected scope
  timeline:
    day_1:
      active_squads: [squad-backend]
      milestones: ["Stripe SDK configured", "Initial payment endpoint active"]
    day_2:
      active_squads: [squad-backend, squad-frontend]
      milestones: ["All payment endpoints complete", "Frontend integration active"]
    day_3:
      active_squads: [squad-data, squad-frontend]
      milestones: ["Migration dry-run complete", "Frontend code in review"]
    day_4:
      active_squads: [squad-data, squad-security]
      milestones: ["Live migration complete", "PCI-DSS audit passed"]
  bottleneck_analysis:
    critical_path: squad-backend  # 2 days (longest duration)
    optimization: "Add 1 implementer to squad-backend → reduces path to 1.5 days"
```

### Phase 4: Squad Spawn and Monitoring Initialization

1. **Spawn Squads Sequentially** — Trigger ready squads based on dependency DAG milestones.
2. **Provide Subagent Orchestrator** — Let the squad's internal subagent-orchestrator manage direct tasks.
3. **Establish Monitoring Dashboard** — Track progress percentages, token expenditures, error counts, and average latencies.
4. **Set Checkpoints** — Determine milestones requiring explicit human sign-off.
5. **Configure Alerts** — Set rules: 80% token budget warning, 3-retry circuit breaker, 30-minute silent stall ping.

```yaml
monitoring:
  check_interval: "15m"
  metrics:
    - squad_progress_pct
    - token_consumed / token_budget
    - error_rate_per_hour
    - tasks_completed / tasks_total
    - avg_response_time_ms
  alerts:
    - name: "token_warning"
      condition: "token_consumed > 0.8 * token_budget"
      action: "notify_commander + scope_review"
    - name: "squad_stall"
      condition: "tasks_completed == 0 for 3 check_intervals"
      action: "ping_squad_commander + root_cause_analysis"
    - name: "circuit_breaker"
      condition: "consecutive_failures >= 3"
      action: "pause_squad + notify_human + fallback_activation"
    - name: "dependency_timeout"
      condition: "waiting_for_upstream > 2h"
      action: "check_upstream_status + consider_stub + notify"
```

### Phase 5: Mid-Flight Steering (Real-Time Routing)

Interventions supported during live execution:

1. **Task Injection** — Inject new requirements. Which squad? Does it block work? What is the priority?
2. **Shift Priorities** — Reprioritize a squad's epic, pausing or slowing down secondary squads.
3. **Squad Rebalancing** — Transfer idle sub-agents from complete squads to struggling ones.
4. **Scope Reduction/Expansion** — Cancel low-priority stories if token budgets are nearing depletion.
5. **Toggle Circuit Breakers** — Re-engage paused squads once root-cause fixes are deployed.

```yaml
steering_commands:
  inject_task:
    - target_squad: squad-backend
      task: "Add Stripe webhook signature validation"
      priority: "P0"
      insert_position: "after_current"
      reason: "Security vulnerability identified"

  rebalance:
    - from_squad: squad-frontend
      to_squad: squad-data
      agent_count: 1
      agent_role: "tester"
      reason: "Frontend testing completed early; data squad requires additional validation resources"

  reprioritize:
    - epic: epic-3
      new_priority: "P0"
      reason: "Demo date moved forward; payment UI must be complete tomorrow"
      impact: "Deferred P1 stories in squad-backend; concentrated effort on epic-3"
```

### Phase 6: Error Recovery and Resilience

3-tier recovery strategy designed for every error:

```
TIER 1: AUTOMATIC RETRY (same squad, same task)
  → Maximum 3 attempts, exponential backoff (1s, 5s, 25s)
  → Applicable only to transient errors (timeouts, rate limits, network drops)
  → Do not retry deterministic errors (validation errors, auth failures)

TIER 2: FALLBACK (same squad, alternative approach)
  → Re-attempt the task using an alternative pattern
  → E.g., API call fails → read from cache
  → E.g., Full migration fails → chunked batch migration

TIER 3: ESCALATE (cross-squad or human partner)
  → Escalate task to a more specialized squad/agent
  → Or consult human: "Task failed; please recommend alternative approach"
  → Circuit breaker: Halt squad after 3 escalations, freeze the epic
```

```yaml
recovery_patterns:
  transient_error:
    pattern: "retry_with_backoff"
    max_retries: 3
    backoff: [1s, 5s, 25s]
    on_exhaust: "fallback"

  dependency_failure:
    pattern: "circuit_breaker"
    failure_threshold: 3
    cooldown_period: "10m"
    half_open_probe: true
    fallback: "use_cached_result || escalate"

  data_corruption:
    pattern: "rollback_and_retry"
    rollback_to: "last_known_good_checkpoint"
    integrity_check: "hash_validation"
    on_failure: "escalate_to_human"

  squad_death:
    pattern: "respawn_with_checkpoint"
    checkpoint_artifact: "squad_context_snapshot.json"
    respawn_strategy: "last_completed_task + 1"
    max_respawns: 2
    on_exhaust: "merge_into_sibling_squad"
```

### Phase 7: Result Consolidation and Verification

When all squads complete their tasks:

1. **Collect Artifacts** — Gather all code, documents, test suites, and configurations produced by the squads.
2. **Cross-Squad Integration Testing** — Verify that Squad A's API integrates correctly with Squad B's frontend.
3. **Consistency Verification** — Check for conflicting decisions (e.g., Squad A used UTC, Squad B used local timezones).
4. **Quality Gates** — Ensure all test suites pass, security scans are green, and performance budgets are respected.
5. **Human Sign-Off** — Summarize deliverables and present to the human for final production approval.

```yaml
merge_validation:
  integration_tests:
    - "end-to-end payment flows"
    - "rollback scenarios"
    - "load testing (10K requests/min)"
  consistency_checks:
    - "Do all APIs return unified error formats?"
    - "Are all services aligned on the same timezone?"
    - "Is authorization token formatting consistent?"
    - "Are logging levels standardized?"
  quality_gates:
    - test_coverage: "> 80%"
    - security_scan: "0 critical, 0 high"
    - performance: "p95 < 200ms"
    - accessibility: "WCAG 2.2 AA"
```

### Phase 8: Post-Mortem and Learning

Executed immediately AFTER every epic (non-negotiable):

1. **Compare Planned vs. Actual** — Analyze duration, token usage, and quality deltas.
2. **Root-Cause Analysis** — Pinpoint why failures occurred (e.g., poor decomposition, resource shortages, domain gaps).
3. **Extract Patterns** — Log reproducible success patterns; document repeating failures as anti-patterns.
4. **Update Skills** — Patch extracted patterns back into the respective skills. Define new skills if necessary.
5. **Log Historical Metrics** — Record metrics to calibrate future planning: "This complexity profile consumed X tokens and Y hours."

```yaml
post_mortem:
  epic: "Stripe Migration"
  planned_vs_actual:
    token_planned: "1.9M"
    token_actual: "2.3M"
    delta: "+21%"
    root_cause: "Stripe API documentation was more complex than anticipated; consumed extra research tokens"
    time_planned: "4 days"
    time_actual: "3.5 days"
    note: "Completed ahead of schedule due to parallelization optimizations"
  lessons:
    - pattern: "stripe-integration-blueprint"
      description: "Sequence: install SDK → endpoints → webhook mappings → migration scripts; configure webhooks last"
      saved_to_skill: "stripe-integration-patterns"
    - antipattern: "premature-webhook-activation"
      description: "Activating webhooks before endpoints are fully functional triggers 400 errors and retry storms"
      saved_to_skill: "stripe-integration-patterns (red flags)"
  metrics_for_future:
    complexity_score: 7.5/10
    token_per_story: "~380K"
    optimal_squad_size: 4
    recommended_parallelism: 3
```

### Phase 9: Closing and Archiving

1. **Package Deliverables** — Archive codebases, documents, test outputs, and post-mortems.
2. **Archive Squad Contexts** — Save squad history for reference in future projects.
3. **Register Skills** — Create or update skills with newly extracted patterns.
4. **Write Historical Benchmarks** — Save performance data to the central repo log.
5. **Deliver Final Summary** — Present a professional summary of goals, metrics, lessons, and suggestions to the human partner.

## Human Partner Signals (Escalate to Human)

**Escalate Immediately:**
- Architecture disagreements between squads (e.g., REST vs. GraphQL, SQL vs. NoSQL) that cannot be resolved automatically.
- Token consumption reaches 95% of the allocated budget while critical tasks remain incomplete.
- A circuit breaker remains open for more than 30 minutes, indicating a systematic environment failure.
- Doubts regarding data integrity (e.g., missing records after migration, hash mismatch).
- A security vulnerability is identified that cannot be patched automatically.

**Inform at Checkpoints:**
- Progress summary: % completion, remaining estimated duration, and critical path status.
- Token expenditure: spent / budget ratios, including justifications for any deviations.
- Risk registry: newly identified risks and mitigation statuses.
- Open questions: outstanding items requiring business/design decisions.

## Verification Checklist

- [ ] Epic decomposition is complete; INVEST criteria met for all stories.
- [ ] Dependency DAG is mapped; critical path is calculated.
- [ ] Role assignments, token budgets, and handoff contracts are defined for each squad.
- [ ] Resource plan is finalized (timeline + bottleneck analysis).
- [ ] Monitoring dashboard is established (metrics + alert conditions).
- [ ] Error recovery strategy is defined per failure type (retry, fallback, escalate).
- [ ] Mid-flight steering mechanisms are ready (inject, rebalance, reprioritize, rescope).
- [ ] Cross-squad integration tests are passing.
- [ ] Quality gates are satisfied (coverage, security, performance, accessibility).
- [ ] Post-mortem is documented; extracted patterns are registered in the skill system.
- [ ] Final summary report is delivered and approved by human partner.
- [ ] Squad contexts are archived; historical benchmarks are registered.

## Chaining (Auto-Trigger)

**Complete → auto-trigger:**
- `squad-builder` — Squad composition and role assignment.
- `task-lifecycle-manager` — Kanban task tracking.
- `agent-teammate` — Creation of persistent squad members.
- `skill-marketplace` — Registration of newly extracted patterns as skills.
- `post-mortem` $\rightarrow$ `skill_manage` — Generate or patch skills.

## Related Skills

- **subagent-orchestrator** — Sub-task parallelization. Used inside each squad under Epic Orchestrator.
- **squad-builder** — Squad composition design. Referenced during Epic Orchestrator's Phase 2.
- **task-lifecycle-manager** — Kanban task tracking. Powers the Epic Orchestrator monitoring dashboard.
- **agent-teammate** — Persistent AI teammate. Squad members are created using this skill.
- **project-discovery** — Discovery and requirement scoping. Executed BEFORE Epic Orchestrator.
- **architecture-planner** — Architectural planning. Guides the technical decisions made by squads.
- **spec-first-development** — Specification authoring. Helps break epics into user stories.
- **agent-introspector** — Agent behavior debugging. Used to triage squad performance bottlenecks.
- **session-memory** — Cross-session memory. Essential for post-mortems and learning loops.
- **skill-marketplace** — Skill discovery and versioning. Used to publish newly extracted patterns as active skills.
