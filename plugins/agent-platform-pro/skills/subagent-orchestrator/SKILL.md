---
name: subagent-orchestrator
description: "Parallel subagent execution, dependency management, mid-run steering, result aggregation. Use when coordinating multiple subagents on a single task."
---

# Subagent Orchestrator

## Overview

This is an orchestration skill designed to divide complex tasks into independent sub-components, execute each in parallel using separate subagents, resolve dependencies automatically, update instructions or add tasks dynamically mid-run, and aggregate results from all subagents. Inspired by Oh-My-Pi's subagent system and Apra Fleet's multi-agent coordination.

**Core principle:** WHAT ONE AGENT DOES ALONE IN 10 TURNS, 5 SUBAGENTS CAN DO IN 2 TURNS EACH — BUT COORDINATION OVERHEAD MUST NOT CONSUME THE GAINS.

## The Iron Law

```
NO SUBAGENT CAN ACCESS CONTEXT IT DOES NOT REQUIRE;
NO SUBAGENT RESULT CAN MIX INTO THE MAIN WORKFLOW WITHOUT AGGREGATION.
```

## When to Use

**Use this when:**
- A task can be divided into 3+ independent sub-tasks.
- Each sub-task generates a testable standalone output.
- Different sub-tasks require different fields of expertise (e.g., researcher, implementer, reviewer, tester).
- The total token/context budget is too large to fit into a single agent's context.
- Real-time progress tracking and mid-run steering are required.

**Use this ESPECIALLY when:**
- Discovery, implementation, and verification loops can run concurrently (e.g., the researcher audits documentation while the implementer starts writing code).
- 3+ alternative approaches need to be tested and compared for a single decision.
- Deadlines are tight and time gained from parallel execution is critical.

**Don't skip when:**
- The task is strictly linear (every step depends directly on the output of the prior step).
- The number of sub-tasks is less than 2 — orchestration overhead consumes the benefits.
- Inter-agent communication is more complex than the task itself.

## Phase 1: Task Decomposition

**BEFORE proceeding:**

1. **Analyze the main task** — identify inputs, outputs, dependencies, and fields of expertise.
2. **Define sub-tasks** — ensuring each is independent, has clear boundaries, and produces a single output.
3. **Map out the dependency graph** — which sub-task must wait for another to complete?
4. **Assign subagent types** — choose the appropriate subagent role for each task (e.g., researcher, implementer, reviewer, tester).

```yaml
tasks:
  - id: research-auth
    type: researcher
    description: "Audit and document the existing authentication infrastructure"
    depends_on: []
    max_turns: 3
    tools: [file_read, web_search]

  - id: implement-auth
    type: implementer
    description: "Write the JWT-based authentication middleware"
    depends_on: [research-auth]
    max_turns: 5
    tools: [file_read, file_write, terminal]

  - id: test-auth
    type: tester
    description: "Develop and execute tests for the auth middleware"
    depends_on: [implement-auth]
    max_turns: 4
    tools: [file_read, file_write, terminal]

  - id: review-auth
    type: reviewer
    description: "Perform a security code review on the auth implementation"
    depends_on: [implement-auth]
    max_turns: 2
    tools: [file_read]
```

## Phase 2: Dependency Resolution

**BEFORE proceeding:**

1. **Perform topological sorting** — resolve the depends_on chain and identify parallel execution waves.
2. **Form execution waves** — group independent sub-tasks that can be initiated concurrently.
3. **Identify the critical path** — locate the longest dependency chain (determining total execution duration).
4. **Calculate resource constraints** — configure max_concurrent, max_turns_per_agent, and total_token_budget values.

```
Execution Flow Example:
  Wave 1 (parallel): [research-api, research-auth, research-db]
  Wave 2 (parallel): [implement-api, implement-auth] -> once research-api and research-auth complete
  Wave 3 (parallel): [implement-db, test-api, test-auth] -> once their dependencies complete
  Wave 4 (single):   [review-all] -> once all preceding waves complete
```

## Phase 3: Subagent Spawning

**BEFORE proceeding:**

1. **Enforce context isolation** — each subagent receives ONLY the files, instructions, and context required for its specific task. Do not allow unnecessary token usage.
2. **Initiate progress tracking** — monitor status changes: queued -> running -> blocked/done/failed.
3. **Define timeout and retry policies** — set timeout durations, retry attempt counts, and increase detail level on retries.
4. **Assign a unique session_id** to each subagent to prevent output overlapping.

```python
# Pseudocode: subagent spawning
for wave in dependency_waves:
    for task in wave:
        agent = spawn_subagent(
            task_id=task.id,
            agent_type=task.type,
            context=isolate_context(task, global_context),
            tools=task.tools,
            max_turns=task.max_turns,
            on_complete=aggregate_result,
            on_fail=retry_or_escalate
        )
    wait_for_wave_completion(wave)
```

## Phase 4: Mid-Run Steering

**BEFORE proceeding:**

1. **Maintain progress monitoring** — display a real-time status of all subagents, showing active steps, outputs, and blocks.
2. **Inject new tasks** — append newly discovered sub-tasks to the dependency graph mid-run, triggering execution once dependencies are met.
3. **Modify running tasks** — update instructions or tools if a subagent is drifting; terminate and restart if necessary.
4. **Resolve blocks** — if a subagent stalls on a decision, request clarification and route the choice back to the subagent.

```yaml
# Mid-run steering commands
steer add-task:    "Inject a new task and configure its dependencies"
steer modify-task: "Update instructions or tools for task-X"
steer cancel-task: "Terminate task-X and reschedule its dependent tasks"
steer unblock:     "Resolve a decision point the subagent is stuck on"
```

## Phase 5: Conflict Resolution

**BEFORE proceeding:**

1. **Detect conflicts** — identify when two subagents produce conflicting outputs for the same target (e.g., divergent API designs).
2. **Gather evidence** — request arguments, references, and logic from both sides.
3. **Evaluate decisions** — review both options; select the optimal choice or construct a hybrid solution.
4. **Document decisions** — record the final choice along with the reasons for rejecting alternatives.
5. **Notify downstream agents** — propagate the decision to dependent subagents down the execution chain.

```
Conflict: implement-auth specified "Use JWTs" while implement-auth-alt specified "Use session cookies"
Evidence Gathering:
  - implement-auth: "JWTs are better suited for mobile app and third-party integrations"
  - implement-auth-alt: "Session cookies are more secure if server-side token revocation is required"
Orchestrator Decision: "Mobile app support is on the project roadmap -> JWTs selected.
                       A refresh token blacklist mechanism will be implemented for revocation."
```

## Phase 6: Result Aggregation

**BEFORE proceeding:**

1. **Verify subagent outputs** — ensure outputs satisfy the target sub-task goals without missing components.
2. **Merge outputs** — combine files or directories written by different subagents, resolving merge conflicts.
3. **Check dependencies** — verify that outputs from upstream agents integrate cleanly as inputs for downstream ones.
4. **Generate the final report** — summarize succeeded/failed tasks, decision records, and resources spent.
5. **Report failures** — if retry limits are exceeded, notify the human supervisor with detailed diagnostic logs.

```yaml
# Example aggregation report
summary:
  total_tasks: 8
  completed: 7
  failed: 1
  total_turns_used: 24
  total_tokens_used: 128000
  wall_clock_time: "4m 32s"
  failures:
    - task: test-auth
      reason: "Could not establish database connection in test environment (tried 3 retries)"
      resolution: "Manual intervention required — check database connection strings"
```

## Phase 7: Final Verification

Before marking complete:

- [ ] Did every sub-task produce a standalone, verifiable output?
- [ ] Has every dependency edge in the graph been verified for output-input compatibility?
- [ ] Were conflicts documented and resolved?
- [ ] Is context isolation preserved (no subagent accessed unneeded context data)?
- [ ] Has the total token budget been preserved?
- [ ] Are retry events and their root causes logged?
- [ ] Are mid-run steering decisions logged?
- [ ] Is the final aggregation report clear and actionable for the user?
- [ ] Have concurrent execution limits and turn limits been respected?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "These tasks are simple; there is no need to draw a dependency graph."
- "Let's pass the same context to every subagent, tokens are cheap" — **Context isolation violation! This guarantees token bloat and confusion.**
- "To add a task right now, we have to stop all running subagents." — **No, this is what mid-run steering is designed for.**
- "Both subagents are saying the same thing anyway, let's merge them." — **Do not merge without verifying conflicts.**
- "I'll orchestrate manually, it will be faster." — **No, follow the process. Manual management guarantees omissions and mistakes.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Wouldn't it be better to combine these sub-tasks?" — Decomposition is too fine; orchestration overhead consumes the benefits.
- "Why is task X still running while task Y is waiting on it?" — You configured the dependency graph incorrectly.
- "Why did this subagent see this file?" — There is a context isolation violation.
- "Two different outputs were returned, which is correct?" — Conflict resolution was skipped.
- "Why are we starting over from scratch?" — Mid-run steering was not utilized, or was used unnecessarily.
- "Was orchestration necessary for this?" — The task is too small; you should not have used this skill.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Parallel execution is always faster." | No. Coordination and context switching overhead consume the benefits for small tasks. Try linear execution first, then decompose. |
| "We can handle context isolation later." | You cannot. Context will bloat, subagents will get confused, and outputs will overlap. |
| "The dependency graph is simple; no need to draw it." | Graphs that look simple become complex after the second wave. Always draw it. |
| "No need for retry logic; it will work on the first try." | It won't. All systems experience errors. Without retry logic, the entire orchestration fails on a single error. |
| "We won't need mid-run steering anyway." | In complex tasks, you always do. Configure it upfront and use it when necessary. |
| "If a conflict occurs, we'll handle it later." | You will get stuck between conflicting answers at the merge step. Resolve conflicts immediately. |

## Related Skills

- **task-breaker** — to divide tasks into sub-tasks (input for subagent-orchestrator)
- **agent-shield** — to prevent subagents from performing insecure actions
- **edge-case-hunter** — to locate edge cases missed by subagents
- **research-first** — protocol followed by researcher subagents when gathering info
- **code-reviewer** — protocol followed by reviewer subagents
- **test-engineer** — protocol followed by tester subagents
- **architecture-planner** — to map out the baseline dependency graph architecture before starting

## Self-Review

After completing this process:

1. **Completeness:** Does each sub-task fully cover a portion of the main task? Are there missing pieces?
2. **Dependency Audit:** Is every dependency in the graph actually required? Are there unnecessary wait times?
3. **Efficiency Check:** Is the time gained from parallelism greater than the orchestration overhead?
4. **Context Check:** Did any subagent access context it did not need?
5. **Quality Check:** Does the aggregated output satisfy the Iron Law standards (independent parts, consistent whole)?
6. **Failure Recovery:** Are all retry and failure scenarios logged? Is the human action clear?
7. **Repeatability:** Would running the same inputs and dependency graph yield the same result?
