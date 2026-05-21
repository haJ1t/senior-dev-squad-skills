# 🔗 Cross-Skill Pipeline — Recommended Chains

> **These chains are RECOMMENDED sequencing, not runtime automation.** Claude Code does not auto-run the next skill. Invoke the next skill yourself, or wire chaining via hooks. The `[auto]` notes and "trigger" wording below mean "recommended next step", not automatic execution.

Each chain shows the recommended next skill to invoke when one completes.

## Main SDLC Pipeline

```
USER STORY
  │
  ├─→ spec-first-development
  │     └─→ [auto] project-discovery (if scope is not clear)
  │     └─→ [auto] edge-case-hunter (capture edge cases in the specification)
  │
  ├─→ architecture-planner
  │     └─→ [auto] distributed-systems-architect (if microservice/distributed)
  │     └─→ [auto] tech-stack-advisor (if technology decision is not made)
  │     └─→ [auto] design-pattern-advisor (if pattern selection is required)
  │
  ├─→ [PARALLEL] frontend-senior-engineer + backend-senior-engineer
  │     ├─→ [auto] accessibility-optimizer (after frontend)
  │     ├─→ [auto] responsive-layout-engine (after frontend)
  │     └─→ [auto] api-design-reviewer (after backend)
  │
  ├─→ [PARALLEL] test-engineer + security-reviewer
  │     ├─→ [auto] edge-case-hunter (after testing)
  │     ├─→ [auto] mitre-attack-mapper (after security)
  │     ├─→ [auto] nist-csf-scanner (if compliance is required)
  │     ├─→ [auto] supply-chain-verifier (if dependency exists)
  │     └─→ [auto] contract-testing (if API exists)
  │
  ├─→ performance-engineer
  │     └─→ [auto] load-testing (if performance is critical)
  │
  ├─→ code-reviewer
  │     ├─→ [auto] cross-model-reviewer (if high-risk PR)
  │     └─→ [auto] refactor-simplifier (if code smell exists)
  │
  ├─→ devops-release-engineer
  │     ├─→ [auto] cloud-security-auditor (if cloud deployment)
  │     ├─→ [auto] chaos-engineer (before production)
  │     └─→ [auto] visual-regression (if UI change exists)
  │
  └─→ ship-readiness-checklist
        └─→ [auto] release-manager (if release approval exists)
```

## Security Chain

```
CODE/DEPLOY
  │
  ├─→ security-reviewer
  │     ├─→ [auto] mitre-attack-mapper
  │     ├─→ [auto] purple-team-analyzer (if red/blue team exists)
  │     └─→ [auto] forensic-investigator (if incident exists)
  │
  ├─→ supply-chain-verifier
  │
  └─→ cloud-security-auditor
```

## Orchestration Chain

```
LARGE PROJECT
  │
  ├─→ epic-orchestrator
  │     ├─→ [auto] squad-builder (for squad design)
  │     ├─→ [auto] task-lifecycle-manager (for task tracking)
  │     └─→ [auto] agent-teammate (for squad members)
  │
  └─→ subagent-orchestrator (for single tasks)
```

## AI/ML Chain

```
ML PROJECT
  │
  ├─→ dataset-curator
  │     └─→ [auto] embedding-manager (if embedding is required)
  │
  ├─→ model-evaluator
  │     └─→ [auto] prompt-engineer (if LLM)
  │
  └─→ rag-architect
```

## Trigger Rules

| When Skill Completed | Condition | Recommended Next |
|-------------------|-------|-----------------|
| spec-first-development | Always | architecture-planner |
| architecture-planner | Microservice architecture | distributed-systems-architect |
| backend-senior-engineer | New API endpoint | api-design-reviewer |
| frontend-senior-engineer | UI implementation | accessibility-optimizer |
| security-reviewer | Always | mitre-attack-mapper |
| security-reviewer | Dependency change | supply-chain-verifier |
| code-reviewer | High-risk PR | cross-model-reviewer |
| code-reviewer | Code smell detection | refactor-simplifier |
| epic-orchestrator | Squad creation | squad-builder |

## Guardrails (recommended at every step)

These are not part of the chain. They are model-invoked from their descriptions, and can be wired as hooks for true always-on behavior:
- **instincts-guardrails** — Context, git, memory, safety
- **agent-shield** — Prompt injection, credential leaks
- **research-first** — Pre-decision research
- **session-memory** — Cross-session learning
