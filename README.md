# 🧠 senior-dev-squad-skills v4.0.0

> **107 production-grade AI agent skills across 27 installable Claude Code plugins** (1 lean core `senior-dev-squad` plugin with 54 skills + 26 specialty plugins with 53 skills). Complete SDLC pipeline: spec → architecture → frontend/backend → security → testing → DevOps → review → ship. Plus guardrails, orchestration, design systems, security frameworks, repo automation, MCP integration, agent platforms, marketing, product management, cross-provider teams, AI/ML engineering, compliance, distributed-systems architecture, and epic orchestration.

**54 core skills + 53 specialty plugin skills = 107 skills across 27 installable plugins** that turn any AI coding agent into a disciplined, production-ready development squad.

## Structure

| Layer | Count | Description |
|-------|:-----:|-------------|
| **Core plugin (`senior-dev-squad`)** | 54 skills | Cross-domain SDLC skills usable on any project |
| **Specialty plugins (26)** | 53 skills | Framework, database, infra, domain, product, marketing, security, AI/ML, MCP, agent platform |
| **Total** | **107 skills / 27 plugins** | |

## Philosophy

| # | Principle |
|---|-----------|
| 1 | **No code without spec.** Agent extracts purpose, user flow, data model, edge cases, acceptance criteria first. |
| 2 | **No implementation without plan.** Plan breaks into atomic tasks. Each task has test + verification method. |
| 3 | **Every feature proven by test.** Unit, integration, e2e, a11y, security, performance — separate skills enforce each. |
| 4 | **Security at every stage.** Not a final review — auth, input validation, secrets, RLS, dependencies, CI, deployment — automatic gates. |
| 5 | **Research before code.** Compile context, search web, analyze alternatives, verify versions before writing a single line. |
| 6 | **Guardrails.** Context management, git hygiene, memory preservation, safety boundaries — model-invoked from their descriptions, or wired as hooks to run automatically. |
| 7 | **Parallel subagents when possible.** Break work into independent streams, execute concurrently, aggregate results. |
| 8 | **Cross-model verification.** One model writes, another reviews — catches issues a single model would miss. |
| 9 | **Design is code too.** Generate UIs from specs using production-grade design systems. Accessibility is non-negotiable. |
| 10 | **Reviewer is ruthlessness.** "It works" is not enough. Code smell, overengineering, missing tests, race conditions, security bugs, edge cases. |

---

## Core Skills Catalog (54)

### 🔍 Discovery & Spec (3)

| # | Skill | What It Does |
|---|-------|-------------|
| 1 | **grill** | Relentlessly interviews the user one question at a time to reach shared understanding before any code is written |
| 2 | **spec-first-development** | Turns ideas into product specs with user stories, acceptance criteria, and edge cases |
| 3 | **research-first** | Compiles context, searches web, analyzes alternatives, and verifies versions before writing a single line |

### 🏗️ Architecture & Tech Stack (4)

| # | Skill | What It Does |
|---|-------|-------------|
| 4 | **architecture-planner** | Full-stack architecture: ADRs, tradeoff tables, mermaid diagrams, CAP awareness, deployment topology |
| 5 | **distributed-systems-architect** | Microservices, event-driven design, data consistency, fault tolerance, multi-region, observability |
| 6 | **tech-stack-advisor** | Interactive tech stack selection: decision trees, tradeoff tables, stack templates |
| 7 | **design-pattern-advisor** | Pattern catalog with selection guide: recommends design patterns with code sketches |

### 🎨 Frontend & UI (5)

| # | Skill | What It Does |
|---|-------|-------------|
| 8 | **frontend-senior-engineer** | Production-grade React/Next.js: responsive, a11y, states, forms, performance |
| 9 | **ui-generator** | Generates production-ready UI components from specs, design system oriented |
| 10 | **responsive-layout-engine** | Generates responsive layouts with design system tokens for each breakpoint — mobile-first through wide screen |
| 11 | **accessibility-optimizer** | WCAG 2.2 AA/AAA auditing, automated fixing, and UI accessibility quality gate |
| 12 | **design-system-manager** | Design system catalog, selection, theming, token generation from brand, and cross-system mapping/migration |

### ⚙️ Backend & Data (8)

| # | Skill | What It Does |
|---|-------|-------------|
| 13 | **backend-senior-engineer** | Production-grade API: input validation, transaction safety, structured logging, idempotency, error schema |
| 14 | **data-modeling-designer** | Designs schemas from access patterns and invariants: normalization, constraints, indexing, relational vs document tradeoffs |
| 15 | **database-migration-planner** | Plans and executes safe schema changes on live databases using expand-contract |
| 16 | **caching-strategist** | Designs deliberate, invalidation-first caching across browser, CDN, app, and DB layers |
| 17 | **realtime-systems-engineer** | WebSocket, SSE, WebTransport, reconnect, backpressure, Redis pub/sub, fan-out, presence, horizontal scaling |
| 18 | **i18n-localization-engineer** | ICU MessageFormat, RTL/bidi layout, Intl API, locale fallback chains, pseudo-localization, TMS handoff |
| 19 | **error-message-optimizer** | Improves error messages for clarity, actionability, context, and debugging speed |
| 20 | **performance-engineer** | Bundle size, lazy loading, N+1 queries, indexes, caching, Core Web Vitals |

### 🧪 Testing & Debugging (3)

| # | Skill | What It Does |
|---|-------|-------------|
| 21 | **test-engineer** | Test strategy: unit, integration, e2e, regression, edge cases, flaky prevention |
| 22 | **edge-case-hunter** | 8-dimension edge case matrix: concurrency, time, state, scale, empty/overflow, network failure |
| 23 | **systematic-debugging** | Diagnoses bugs to verified root cause using reproduce-minimize-hypothesize-bisect-confirm |

### 👁️ Review & Refactor (3)

| # | Skill | What It Does |
|---|-------|-------------|
| 24 | **code-reviewer** | PR, API design, and planning-document review: blocking issues, missing tests, security, API consistency |
| 25 | **cross-model-reviewer** | Cross-provider AI review loop: doer-reviewer pattern with a different AI model |
| 26 | **refactor-simplifier** | Simplify after it works: remove clever code, duplication, and dead abstraction without changing behavior |

### 🔒 Security (3)

| # | Skill | What It Does |
|---|-------|-------------|
| 27 | **security-reviewer** | OWASP Top 10, injection, XSS, IDOR, secrets, SSRF, prompt injection, LLM anti-patterns |
| 28 | **agent-shield** | Runtime security: prompt injection, credential leakage, data exfiltration, dangerous operation detection |
| 29 | **supply-chain-verifier** | Dependency CVE scanning, provenance verification, license compliance across package ecosystems |

### 🚀 DevOps & Reliability (9)

| # | Skill | What It Does |
|---|-------|-------------|
| 30 | **devops-release-engineer** | Docker, CI/CD, secrets, deployment checklist, rollback, health checks |
| 31 | **sre-slo-engineer** | Defines reliability targets: SLIs from real user journeys, SLOs with error budgets, multi-window burn-rate alerts |
| 32 | **incident-responder** | Drives production incident response end-to-end: detect, declare, classify, stabilize, communicate, postmortem |
| 33 | **chaos-engineer** | Chaos engineering: controlled failure injection, steady-state hypotheses, resilience testing |
| 34 | **backup-dr-planner** | Designs backup and disaster-recovery strategy: RPO/RTO targets, 3-2-1 rule, encryption, tested restore drills |
| 35 | **finops-cost-optimizer** | Cloud FinOps: tagging, rightsizing, autoscaling, purchase options, storage tiering, egress reduction |
| 36 | **monorepo-manager** | Structures and operates monorepos with explicit package boundaries, affected-only CI builds, and shared tooling |
| 37 | **dependency-upgrader** | Safely upgrades project dependencies: audit, changelog review, one-at-a-time bumps, tests green between each |
| 38 | **feature-flag-manager** | Manages feature flags across full lifecycle: creation, targeting, rollout, kill-switch, and removal |

### 📋 Planning & Automation (7)

| # | Skill | What It Does |
|---|-------|-------------|
| 39 | **task-breaker** | Converts spec + implementation plan into ordered, agent-executable tasks with dependency chains |
| 40 | **agent-prompt-builder** | Synthesizes all docs into a single-shot, self-contained agent prompt with task decomposition |
| 41 | **pr-babysitter** | PR monitoring: CI error correction, review replying, merge conflict resolution, rebase management |
| 42 | **issue-triage-bot** | Issue classification, prioritization, duplicate detection, reproducibility checks |
| 43 | **auto-changelog** | Commit analysis, change categorization, breaking change detection, semver recommendation |
| 44 | **release-manager** | Release management: tagging, changelog generation, package publishing |
| 45 | **tech-debt-tracker** | Scanning, categorizing, prioritizing, and reporting technical debt using Harness Craft methodology |

### 🛡️ Guardrails & Workflow (6)

| # | Skill | What It Does |
|---|-------|-------------|
| 46 | **instincts-guardrails** | Always-on guardrails: context management, git hygiene, memory preservation, quality gates, security boundaries |
| 47 | **session-memory** | Cross-session memory: past decisions, mistakes, repository context preservation |
| 48 | **setup-senior-dev-squad** | Interactive onboarding wizard that captures project conventions and writes them into CONTEXT.md |
| 49 | **documentation-generator** | Auto-generates docs from code: API references, READMEs, architecture docs, and ADRs |
| 50 | **onboarding-automator** | Automated developer onboarding: environment setup, first PR walkthrough, codebase familiarization |
| 51 | **dev-environment-manager** | Reproducible, containerized dev environments: devcontainers, dotfiles, tooling, configuration as code |

### ✅ Ship & Task Lifecycle (3)

| # | Skill | What It Does |
|---|-------|-------------|
| 52 | **ship-readiness-checklist** | Final gate: tests pass, lint/build clean, env documented, migrations safe, rollback possible |
| 53 | **task-lifecycle-manager** | Full task lifecycle management, epic decomposition, deployment tracking, dependency resolution |
| 54 | **data-retention-manager** | Data retention policy, lifecycle management, archival, secure deletion, compliance automation |

---

## Specialty Plugins (26)

### 🖥️ Framework Pro (4 plugins, 4 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **nextjs-pro** | nextjs-pro | Next.js App Router, Server Components, Server Actions, ISR, streaming, middleware |
| **fastapi-pro** | fastapi-pro | FastAPI patterns, Pydantic, async SQL, dependency injection, WebSocket, testing |
| **node-express-pro** | node-express-pro | Express.js patterns, middleware architecture, error handling, validation, file uploads |
| **django-pro** | django-pro | Django ORM, DRF, signals, management commands, Celery, testing |

### 🗄️ Database Pro (2 plugins, 2 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **supabase-pro** | supabase-pro | Supabase auth, RLS, realtime, storage, edge functions, database design |
| **postgres-pro** | postgres-pro | Advanced PostgreSQL: indexing, CTEs, window functions, partitioning, full-text search |

### 🏗️ Infra Pro (2 plugins, 2 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **docker-k8s-pro** | docker-k8s-pro | Multi-stage Docker, K8s manifests, Helm, service mesh, scaling, monitoring |
| **terraform-pro** | terraform-pro | Terraform modules, remote state, workspaces, CI/CD for IaC, security scanning |

### 🏢 Domain Pro (10 plugins, 10 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **saas-pro** | saas-pro | Multi-tenant architecture, billing, subscription management, onboarding, RBAC |
| **fintech-pro** | fintech-pro | Payments, compliance, auditing, reconciliation, fraud detection, ledger |
| **ecommerce-pro** | ecommerce-pro | Cart, catalog, inventory, payments, checkout, orders, search, personalization |
| **healthtech-pro** | healthtech-pro | HIPAA compliance, FHIR, EHR integration, audit, PHI protection |
| **mobile-pro** | mobile-pro | React Native / Flutter / SwiftUI: state management, navigation, offline, push, stores |
| **game-dev-pro** | game-dev-pro | Unity, Unreal, Godot: game architecture, ECS, multiplayer, optimization, CI/CD |
| **ai-ml-pro** | ai-ml-pro | ML workflows, training pipelines, model evaluation, deployment, experiment tracking |
| **ai-app-security-pro** | ai-app-security-pro | LLM security: prompt injection, guardrails, PII redaction, model access control, audit |
| **blockchain-web3-pro** | blockchain-web3-pro | Smart contracts, dApps, DeFi, NFT, testing, security, gas optimization |
| **data-engineering-pro** | data-engineering-pro | ETL pipelines, data warehousing, streaming, orchestration, quality, governance |
| **devtools-pro** | devtools-pro | CLI tools, VS Code extensions, SDKs, developer experience, API design |
| **observability-pro** | observability-pro | Monitoring, logging, tracing, alerting, dashboards, SLOs, incident response |

### 📦 Product Pro (1 plugin, 4 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **product-pro** | opportunity-solver | JTBD-based product opportunity discovery, customer interview analysis, competitive landscape mapping |
| | roadmap-prioritizer | Data-driven roadmap prioritization using RICE/ICE/MoSCoW, dependency mapping, capacity planning |
| | validation-designer | Design validation experiments, Lean Canvas, MVP scoping, success metrics, statistical analysis |
| | growth-engineer | Data-driven growth engineering: funnels, A/B testing, viral loops, retention, PLG metrics |

### 📣 Marketing Pro (1 plugin, 4 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **marketing-pro** | branding-generator | Brand identity docs, color palettes, typography, voice guidelines, logo prompts, asset checklist |
| | content-strategist | Multi-channel content strategy, audience analysis, SEO briefs, performance optimization |
| | geo-optimizer | Generative Engine Optimization for AI search — optimize for ChatGPT, Perplexity, Gemini |
| | social-media-manager | Cross-platform social media management, platform-specific adaptation, analytics, community engagement |

### 🔐 Security & Compliance Pro (1 plugin, 8 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **security-compliance-pro** | cloud-security-auditor | AWS, GCP, Azure security auditing, IaC scanning, IAM analysis, network security, compliance mapping |
| | forensic-investigator | DFIR: memory dumps, log analysis, timeline mapping, root cause analysis |
| | gdpr-compliance-scanner | Automated GDPR compliance scanning: data flows, consent management, right-to-access, privacy by design |
| | mitre-attack-mapper | Maps code patterns and vulnerabilities to MITRE ATT&CK techniques |
| | nist-csf-scanner | NIST Cybersecurity Framework (CSF 2.0) compliance scanner across 6 core functions |
| | policy-as-code | Policy-as-code with OPA: compliance, security, and operational rules as versioned Rego |
| | purple-team-analyzer | Purple Team analysis combining red team (attack) and blue team (defense) perspectives |
| | soc2-audit-prep | SOC 2 audit prep, trust services criteria mapping, control documentation, evidence collection |

### 🤖 AI/ML Engineering Pro (1 plugin, 5 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **ai-ml-eng-pro** | dataset-curator | Dataset creation, cleaning, augmentation, versioning, QA for ML/AI pipelines |
| | embedding-manager | Embedding generation, vector storage, similarity search optimization, and model selection |
| | model-evaluator | Systematic LLM and ML model evaluation: benchmarks, metrics, regression detection, model comparison |
| | prompt-engineer | Systematic prompt design, optimization, and evaluation framework for LLM applications |
| | rag-architect | End-to-end RAG system design: chunking strategies, embedding selection, retrieval optimization, reranking |

### 🔌 MCP Tools Pro (1 plugin, 4 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **mcp-tools-pro** | mcp-api-tester | HTTP endpoint tests, smoke testing, contract verification, and integration tests via MCP |
| | mcp-db-connector | Querying, schema inspection, and data analysis using live database connections via MCP |
| | mcp-infra-scanner | Cloud resources, IaC configs, CIS benchmarks, compliance rules via MCP |
| | mcp-server-hub | Organizing, managing, and invoking 38+ dockerized security tools as MCP servers |

### 🤝 Agent Platform Pro (1 plugin, 8 skills)

| Plugin | Skill | What It Does |
|--------|-------|-------------|
| **agent-platform-pro** | agent-introspector | Self-introspection, reasoning analysis, decision trace, internal state inspection |
| | agent-teammate | Persistent AI teammate, cross-session memory, personality, project context continuity |
| | epic-orchestrator | Multi-squad orchestration: task decomposition, resource optimization, routing, error recovery |
| | multi-agent-debate | Structured debate between multiple LLMs using Proposer→Opponent→Judge protocol |
| | provider-router | Intelligent LLM provider selection based on task characteristics, cost-latency-quality optimization |
| | skill-marketplace | Internal skill discovery, installation, version management, context-aware skill suggestions |
| | squad-builder | Assemble and orchestrate agent squads with defined roles for complex multi-agent tasks |
| | subagent-orchestrator | Parallel subagent execution, dependency management, mid-run steering, result aggregation |

---

## Pipeline

```
User Idea
  → grill (align on what we're actually building)
    → research-first / tech-stack-advisor
      → spec-first-development
        → architecture-planner / distributed-systems-architect / design-pattern-advisor
          → task-breaker → agent-prompt-builder
            → [Parallel] frontend-senior-engineer + backend-senior-engineer
              → test-engineer + edge-case-hunter + systematic-debugging
              → security-reviewer + agent-shield
              → chaos-engineer
              → cross-model-reviewer
              → performance-engineer
              → code-reviewer
              → refactor-simplifier
                → devops-release-engineer
                  → ship-readiness-checklist
                    → 🚀 PRODUCTION

Cross-Cutting:
  epic-orchestrator (agent-platform-pro) → Manages entire epic execution with multi-squad coordination
```

**Guardrails (recommended at every step):** instincts-guardrails + session-memory + agent-shield are designed to run throughout — model-invoked from their descriptions, or wired as hooks for true always-on behavior.
**Subagent orchestrator** (agent-platform-pro) handles parallelism when >2 independent workstreams exist.
**Epic orchestrator** (agent-platform-pro) handles projects spanning multiple days with 5-50+ subagents across multiple squads.
**Supply-chain-verifier** scans dependencies at every merge.

## Quality Format (Superpowers-Quality)

Every skill follows the superpowers-quality format:

- **Iron Laws** — NEVER-violate rules (numbered, bold law names)
- **Red Flags** — STOP-immediately conditions (bullet list with explanations)
- **Common Rationalizations** — Self-deception patterns with reality checks
- **Human Partner Signals** — When to escalate to human
- **When To Use** — Trigger conditions
- **Pipeline** — Numbered step-by-step workflow
- **Verification Checklist** — Checkbox list for completion verification
- **Related Skills** — Linked skills with relationship descriptions

## Installation

```bash
# 1. Add this marketplace (from GitHub or a local clone)
/plugin marketplace add haJ1t/senior-dev-squad-skills

# 2. Install the core squad + any domain plugins you want
/plugin install senior-dev-squad@senior-dev-squad
/plugin install nextjs-pro@senior-dev-squad

# 3. Invoke skills (namespaced by plugin)
/senior-dev-squad:spec-first-development
/nextjs-pro:nextjs-pro
```

## Influences

- **obra/superpowers** — subagent-driven development methodology
- **affaan-m/ECC** — instinct systems, agent shield, session memory, introspection
- **can1357/oh-my-pi** — subagent orchestration, hash-anchored edits
- **nexu-io/open-design** — agent-native design systems
- **Apra-Labs/apra-fleet** — cross-model doer-reviewer loops
- **multica-ai/multica** — multi-agent debate and provider routing
- **Anthropic** — official Claude Code skill format & plugin structure
- **Addy Osmani** — software development lifecycle patterns
- **Trail of Bits** — security review methodology
- **LambdaTest** — testing strategy & coverage patterns
- **Vercel** — frontend performance & deployment best practices
- **Supabase** — backend patterns (auth, RLS, migrations)
- **OWASP** — Top 10 Web + Top 10 for LLM/Agentic Applications
- **Snyk** — agent skill supply-chain security guidelines
- **OpenMercato** — skill marketplace design patterns
- **Harness Craft** — compliance and governance frameworks
- **Martin Kleppmann** — Designing Data-Intensive Applications (distributed systems patterns)
- **Sam Newman** — Building Microservices (service decomposition)

## File Statistics

| Metric | Value |
|--------|-------|
| Total Plugins | 27 (1 core + 26 specialty) |
| Total Skills | 107 (54 core + 53 specialty) |
| Skill Template | `templates/SKILL-template.md` (not shipped as a skill) |
| Phases | 0–7 |
| Largest Skill | grill (~288 lines); fat skills split into SKILL.md + REFERENCE.md |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-18 | Core SDLC (12 skills) + Domain Plugins (19) |
| 2.0.0 | 2026-05-19 | Phase 0-2 added: Guardrails, Orchestration, Design System, Security, Repo, MCP, Agent Platform, Marketing, Product, Cross-Provider |
| 3.0.0 | 2026-05-20 | Phase 3 added: AI/ML Pipeline, DevEx, Compliance, Advanced Testing. Domain plugins expanded to 20. ~100-skill milestone. |
| 3.1.0 | 2026-05-20 | NEW: epic-orchestrator (epic-level multi-squad orchestration, 456 lines) + distributed-systems-architect (distributed systems/microservices architecture, 592 lines) |
| **3.2.0** | **2026-05-21** | **Repackaged as an installable Claude Code marketplace: hybrid topology (1 core plugin + 20 domain plugins), valid `.claude-plugin/marketplace.json` + per-plugin `plugin.json`, deduped skills, `_template` moved out, counts corrected to 102 skills / 21 plugins, removed misleading auto-trigger/always-on claims. Content pass: all 82 core skills brought to the 7-section template bar (Iron Law / When-to-Use / Red Flags / Rationalizations / Human-Signals / Verification / Related Skills), 20 domain plugins to a lighter bar (When-to-Use + Related Skills), and all 102 descriptions trigger-optimized for auto-invocation.** |
| **3.3.0** | **2026-05-21** | **Phase 3 expansion: added 3 core skills — `i18n-localization-engineer`, `realtime-systems-engineer`, `finops-cost-optimizer` (Product/Platform bucket), each at the full 7-section template bar → 105 skills / 21 plugins.** |
| **3.4.0** | **2026-05-21** | **Adopted mattpocock/skills strengths: new `setup-senior-dev-squad` (interactive config) + `grill` (alignment interview) skills; `CONTEXT.md`/ADR cohesion convention (`templates/CONTEXT-FORMAT.md`, `templates/ADR-FORMAT.md`) woven into 10 flagship skills; lifecycle dirs (`incubator/`, `attic/`); `scripts/check-consistency.py` + maintenance `CLAUDE.md` → 107 skills / 21 plugins.** |
| **3.5.0** | **2026-05-25** | **Expansion + depth → 117 skills / 21 plugins. +10 core skills: Ops/Reliability (`incident-responder`, `sre-slo-engineer`, `backup-dr-planner`), Data/DB (`database-migration-planner`, `data-modeling-designer`, `caching-strategist`), Delivery/DX (`dependency-upgrader`, `monorepo-manager`, `feature-flag-manager`), plus the `systematic-debugging` flagship; deepened `grill` + `test-engineer` with worked examples + decision trees. Also progressive-disclosure split of all 17 fat skills into SKILL.md + REFERENCE.md, and removal of canned placeholder slop from 49 skills.** |
| **4.0.0** | **2026-05-25** | **Major restructure for quality > quantity: extracted 6 specialty plugin suites (product, marketing, security-compliance, ai-ml-eng, mcp-tools, agent-platform; 33 skills) out of the core, and merged 10 overlapping core skills into flagships (requirements→grill, api/quality review→code-reviewer, mutation/visual/contract/load testing→test-engineer, brand/token→design-system-manager). Lean core 97→54 skills; 117→107 total across 27 plugins.** |

## License

MIT
