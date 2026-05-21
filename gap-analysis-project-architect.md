# Gap Analysis: project-architect vs senior-dev-squad-skills

Generated: analyzing /tmp/project-architect/references/*.md files

---

## EXECUTIVE SUMMARY

**project-architect** is a **document pipeline generator** — it produces 5 interconnected documents (SPECIFICATION.md, IMPLEMENTATION.md, TASKS.md, BRANDING.md, PROMPT.md) through an interactive discovery process, optimized for Claude Code execution.

**senior-dev-squad-skills** is a **code quality enforcement system** — 10+ skills that each enforce a specific quality gate (spec-first, test-first, security review, edge case hunting, etc.) with iron laws, red flags, and checklists.

The two packages are **largely complementary**, but there are 13 distinct concepts/features in project-architect that have NO equivalent in our package.

---

## 1. Interactive Discovery / Elicitation System

**project-architect has:** `references/elicitation-guide.md`
**We have:** NOTHING

| Feature | Details |
|---------|---------|
| 3-tier question system | Tier 1 (Blockers/must-ask), Tier 2 (Important), Tier 3 (Depth) |
| 8-step discovery flow | Project Identity -> Technical Direction -> Data & Storage -> Features & Scope -> Architecture Preferences -> Operations & Deployment -> Scale & Performance -> Project Meta |
| AskUserQuestion patterns | Every question has ready-to-use options with trade-offs |
| Adaptive Questioning Matrix | User signal (1-liner, detailed brief, "help me", "quick spec", existing doc) -> depth adjustment |
| Batch questioning | Group 1-3 related questions per interaction, never 5+ |
| Decision summarization | After discovery, summarizes all decisions before generating |

**Example: Adaptive Questioning Matrix (p.189-198 of elicitation-guide.md):**
```
| User Signal | Questions to Ask | Depth |
| "I want to build X" (1 line) | Steps 1-5 fully, 6-8 selectively | High |
| Detailed 3+ paragraph brief | Gaps in Steps 1-3 only | Low |
| "Just need a quick spec" | Step 1-2 only, sensible defaults | Minimal |
| Uploads existing doc | Extract all answers, ask only gaps | Varies |
```

**Value add:** We need an interactive elicitation skill that asks structured questions before any spec generation, with adaptive depth based on user input detail.

---

## 2. Interactive Tech Stack Advisor

**project-architect has:** `references/tech-stacks.md`
**We have:** NOTHING — we have domain plugins (django-pro, nextjs-pro, etc.) but no INTERACTIVE advisor

| Feature | Details |
|---------|---------|
| Decision tree by project type | Web App/API Service, CLI Tool, Library/SDK — each with different options |
| 8 decision categories | Language, Framework, Database, Frontend, Auth, ORM, Testing, Deployment |
| Trade-off tables | Every option has "Best For" + "Trade-off" columns (e.g., TypeScript vs Go vs Python vs Rust) |
| Stack templates | 5 pre-built templates: Modern Full-Stack, High-Performance API, CLI Tool, Real-time, Self-Hosted |
| Version Verification Protocol | Web search for latest versions before recommending |
| Per-language framework guides | TypeScript (Next/Fastify/Hono/Express/NestJS/AdonisJS), Go (Chi/Echo/Fiber/Gin/Buffalo), Python (FastAPI/Django/Flask/Litestar) |

**Example stack template (p.281-300):**
```
### High-Performance API Service
Go + Chi/Echo + PostgreSQL + sqlc + Docker + GitHub Actions

### Developer CLI Tool
Go + Cobra + SQLite (if storage needed) + goreleaser
```

**Value add:** An interactive tech stack advisor skill that walks users through decisions with trade-offs, recommends stack templates, and verifies latest versions.

---

## 3. Design Pattern Catalog with Selection Guide

**project-architect has:** `references/design-patterns.md`
**We have:** NOTHING

| Feature | Details |
|---------|---------|
| 7 pattern categories | Architecture, Structural, Behavioral, Data, API, Concurrency, Security, Frontend, Testing |
| 35+ individual patterns | Each with: When to use, Structure, Trade-off, Skip-when, Common uses |
| Pattern Selection Guide | Table: Project Characteristic -> Recommended Patterns |
| Code sketches | 5-15 lines showing pattern applied to project's domain |
| Concrete code examples | Interfaces, type signatures, structural examples in TypeScript |

**Example selection guide (p.296-311):**
```
| Project Characteristic | Recommended Patterns |
| Simple CRUD API | Layered Architecture, Service Layer, DTO, RESTful Resources |
| Complex business logic | Clean Architecture, Repository, Service Layer, State Machine |
| Multiple external APIs | Adapter, Circuit Breaker, Retry with Backoff, Strategy |
| Real-time features | Observer/Event Emitter, Worker Pool, WebSocket handler |
```

**Value add:** A design pattern advisor that recommends and shows code sketches for patterns matching project needs. Our architecture-planner mentions ADR but has no pattern catalog.

---

## 4. Multi-Document Pipeline with Cross-References

**project-architect has:** SPEC -> IMPL -> TASKS -> BRANDING -> PROMPT
**We have:** Individual skills that don't chain into a pipeline

| Feature | Details |
|---------|---------|
| 5 interconnected documents | Each feeds the next in sequence |
| Section numbering for refs | SPEC.md §3.1, IMPLEMENTATION.md §2 — used for cross-references |
| Pause-and-review flow | Generate each doc, wait for approval before next |
| Sequential generation | SPEC before IMPL before TASKS before BRANDING before PROMPT |
| Partial entry points | "Just the spec", "Skip to tasks", "Just give me a prompt" |

**Example pipeline (SKILL.md p.32-43):**
```
[Discovery] -> SPECIFICATION.md -> IMPLEMENTATION.md -> TASKS.md -> BRANDING.md
                  (The What)         (The How)         (The Work)   (Identity)
                       |                  |                   |
                       +------------------+-------------------+
                                          |
                                     PROMPT.md
                              (Claude Code Single-Shot)
```

**Value add:** Our skills are standalone. We need an orchestrator skill that chains them into a pipeline with cross-referencing documents.

---

## 5. Comprehensive IMPLEMENTATION.md Generator

**project-architect has:** `references/implementation-guide.md` (406 lines)
**We have:** architecture-planner covers some of this but is much less comprehensive

| Feature | Details |
|---------|---------|
| Tech stack summary table | Layer, Technology, Version, Rationale — 14 rows |
| ADR-lite decision format | Context, Options Considered, Choice, Rationale, Consequences |
| Dependency inventory | Package, Purpose, License, Justification |
| Design patterns with code sketches | 3-8 patterns with project-specific examples |
| Complete directory layout | Every file represented or implied |
| Module breakdown | Path, Responsibility, Exports, Imports, Key Files |
| Module dependency graph | ASCII diagram showing coupling |
| Full database schema | Complete SQL CREATE TABLE statements |
| Migration strategy | Tool, naming convention, rollback approach |
| Data access patterns | Actual code examples, not pseudocode |
| Caching strategy | What's cached, TTL, invalidation approach |
| Error handling classification | Category, Example, HTTP Code, Logged As, User Sees |
| Configuration schema | Key, Type, Default, Env Var, Description |
| Test pyramid | Level, Tool, Scope, Target |
| Development workflow | Local setup, code standards, git workflow |
| Quality checklist | 11-item checklist |

**Example error classification (p.284-295):**
```
| Category | Example | HTTP Code | Logged As | User Sees |
| Validation | Bad email format | 400 | Debug | Field error |
| Auth | Invalid token | 401 | Info | "Please sign in" |
| Internal | DB crash | 500 | Error | "Something went wrong" |
```

**Value add:** Our architecture-planner has some of this (API contract, DB model, auth) but lacks: dependency inventory, caching strategy, error classification, config schema, test pyramid, dev workflow, quality checklists.

---

## 6. Task Breakdown Generator (TASKS.md)

**project-architect has:** `references/tasks-guide.md` (318 lines)
**We have:** NOTHING — no skill generates ordered task lists

| Feature | Details |
|---------|---------|
| Task = Claude Code session | Each task completable in one focused session (2-8 hours) |
| Dependency order = build order | No task references work from later tasks |
| Exact file lists | Every task names every file to create/modify |
| Acceptance criteria per task | 3-6 verifiable, specific, machine-testable criteria |
| Phase structure | Foundation, data layer, core logic, API, auth, testing, release |
| Phase structure per project type | Standard Backend, Full-Stack Web App, CLI Tool, Library/SDK |
| Dependency graph | ASCII diagram of task dependencies |
| Milestones tracking | Foundation, Data Layer, Core Features, MVP, Release |
| Claude Code optimization | Exact files, patterns to follow, test commands, self-contained context |

**Example task (p.273-303):**
```
### Task 7: User Registration Endpoint
**Files:** src/handlers/auth.ts, src/services/auth-service.ts, ...
**Implementation:** 1. Create Zod schema, 2. AuthService.register(), ...
**Pattern:** Service Layer pattern from IMPLEMENTATION.md §2.2
**Tests:** Unit + Integration with specific scenarios
**Acceptance Criteria:**
- [ ] POST with valid data returns 201 + user JSON
- [ ] POST with duplicate email returns 409 + EMAIL_EXISTS
- [ ] POST with invalid email returns 400 + VALIDATION_ERROR
```

**Value add:** A task-breakdown skill that converts specs/architecture into ordered, executable work items for agents.

---

## 7. Branding Document Generator

**project-architect has:** `references/branding-guide.md` (195 lines)
**We have:** NOTHING

| Feature | Details |
|---------|---------|
| Name & identity | Pronunciation, etymology, code name, prose capitalization |
| Taglines | Primary, Technical, Marketing variants |
| Logo concept | Visual metaphor, AI generation prompt |
| Color palette | Brand colors, neutrals, semantic colors, dark mode, CSS variables |
| Typography | Font stack, type scale |
| Voice & tone | Personality adjectives, writing rules, vocabulary |
| Visual language | Border radius, shadows, spacing, icons |
| Assets checklist | Logo SVG/PNG, icon, favicon, OG image, social banner |
| Depth by project type | CLI (light) vs SaaS (full) vs Internal tool (minimal) |

**Value add:** A branding skill that generates identity docs consistent with project type.

---

## 8. Single-Shot Agent Prompt Generator (PROMPT.md)

**project-architect has:** `references/claude-code-prompt.md` (271 lines)
**We have:** NOTHING — THIS IS THE BIGGEST GAP

| Feature | Details |
|---------|---------|
| Self-contained | Everything inline — no "see SPEC.md", no external refs |
| Version-locked dependencies | Exact versions for npm/go/etc |
| Complete config files | Full tsconfig.json, Dockerfile, docker-compose.yml content |
| Code sketches for complex patterns | 10-30 line structural examples (auth flow, state machine, middleware) |
| Explicit edge cases | Invalid input, missing/null data, duplicates, HTTP codes |
| Test-driven hints | Write test first, then implement |
| Checkpoint markers | Verification points every 3-5 tasks |
| Task count by project size | 10-20 tasks (weekend hack) to 100+ (enterprise) |
| Split prompts for large projects | PROMPT-foundation.md, PROMPT-features.md, PROMPT-release.md |
| Build order from TASKS.md | Execution order matches task sequence |

**Example checkpoint (p.231-236):**
```
**?: Checkpoint:** At this point, `npm run build` should succeed and `npm test` should
pass with [N] tests. If not, fix before proceeding.
```

**Example prompt structure (p.30-184):**
```
1. Project Overview (from SPEC.md ?1.1)
2. Tech Stack (from IMPL.md ?1.1 - exact versions)
3. Project Structure (full directory tree)
4. Dependencies (exact install commands)
5. Configuration Files (full tsconfig, eslint, Dockerfile, etc.)
6. Implementation Order (all tasks from TASKS.md)
7. Data Model (complete SQL schema)
8. API Reference (route table)
9. Error Handling (classification table)
10. Auth Flow (step by step)
11. Environment Variables
12. Testing Requirements
13. Quality Checks (lint, test, build, API, migration, Docker, README)
```

**Value add:** This is the crown jewel of project-architect. We have NO equivalent. A skill that synthesizes all other documents into a single, self-contained prompt that an agent can execute to build the entire project from scratch.

---

## 9. Partial Entry Point / Workflow Support

**project-architect has:** SKILL.md "Handling Partial Input" section
**We have:** NOTHING

| Scenario | Action |
|----------|--------|
| Vague 1-liner | Full elicitation flow |
| Detailed brief | Extract answers, ask only gaps |
| Existing spec uploaded | Validate, suggest improvements |
| "Just the spec" | Generate SPECIFICATION.md only |
| "Skip to tasks" | Lightweight spec+impl, then tasks |
| "Just give me a prompt" | Condensed discovery -> PROMPT.md |
| "Help me choose a stack" | Run tech stack advisor |

**Value add:** A dispatcher skill that routes user input to the right workflow based on detail level and stated need.

---

## 10. Version Verification Protocol

**project-architect has:** In tech-stacks.md (p.304-314)
**We have:** NOTHING

Explicit instruction to web search for latest stable versions before including in documents. Notes version explicitly in tech stack table, mentions migration considerations for major version changes.

**Value add:** A version-checking routine that prevents recommending outdated dependencies.

---

## 11. Adaptive Depth Scaling

**project-architect has:** Across elicitation-guide.md and claude-code-prompt.md
**We have:** NOTHING

Project size determines:
- Number of discovery questions (5-8 for weekend hack, 15-25 for full product)
- Prompt length (2K-5K words for small, 15K-40K for large)
- Task count (10-20 for small, 50-100+ for enterprise)

**Value add:** A sizing heuristic that adjusts document depth and task granularity based on project scope.

---

## 12. Document Quality Checklists

**project-architect has:** Quality checklists at the end of spec-guide, impl-guide, tasks-guide, branding-guide, prompt-guide
**We have:** NOTHING comparable

Each checklist is a runnable verification:
- spec: 9 items (testable AC, data model coverage, non-goals, no vague language, etc.)
- impl: 11 items (rationale for every choice, file-level complete, cross-references, etc.)
- tasks: 10 items (executable order, no forward deps, verifiable criteria, etc.)
- prompt: 12 items (self-contained, version-locked, complete configs, etc.)

**Value add:** Post-generation quality verification for every document type.

---

## 13. Integrated Plugin-Aware Architecture

**project-architect has:** SKILL.md "Plugin-Aware Integration" section (p.156-169)
**We have:** NOTHING

Checks if user has other skills installed (react-app-planner, language skills, brand skills) and suggests integrating them. Mentions them naturally: "You have a react-app-planner skill — want me to use it for deeper React architecture decisions?"

**Value add:** A cross-skill awareness mechanism that creates a cohesive experience across installed skills.

---

## COMPARISON TABLE

| # | Feature/Concept | project-architect | senior-dev-squad-skills |
|---|----------------|-------------------|------------------------|
| 1 | Interactive discovery/elicitation | Full (8-step flow, 3 tiers, adaptive matrix) | NONE |
| 2 | Interactive tech stack advisor | Full (8 decisions, trade-offs, templates, version verify) | NONE |
| 3 | Design pattern catalog | Full (35+ patterns, selection guide, code sketches) | NONE |
| 4 | Multi-doc pipeline with cross-refs | Full (5 docs, sequential, numbered sections) | Individual skills only |
| 5 | IMPLEMENTATION.md generator | Full (16 sections, 406 lines template) | Partial (architecture-planner covers ~40%) |
| 6 | Task breakdown generator | Full (project-type phases, deps, milestones) | NONE |
| 7 | Branding document generator | Full (colors, typography, voice, assets) | NONE |
| 8 | Single-shot agent prompt generator | Full (self-contained, checkpoints, task order) | NONE (BIGGEST GAP) |
| 9 | Partial entry points | 7 scenarios supported | NONE |
| 10 | Version verification protocol | Explicit web search routine | NONE |
| 11 | Adaptive depth scaling | Question count, doc length, task count vary | NONE |
| 12 | Document quality checklists | Every doc has 9-12 item checklist | NONE |
| 13 | Plugin-aware integration | Suggests other skills in context | NONE |

## WHAT WE HAVE THAT project-architect DOESN'T

Fairness: our skills cover areas project-architect doesn't touch:

1. **Spec-first development** (6-phase feature spec with Given/When/Then) — project-architect has spec doc but no phase-based spec writing skill
2. **Edge case hunting** (8-dimension matrix) — unique concept
3. **Code reviewing** (PR checks with blocking/suggestion levels) — unique
4. **Security reviewing** (STRIDE + OWASP per stage) — unique
5. **Refactor simplification** (10 simplification rules) — unique
6. **Performance engineering** (CWV, N+1, caching strategy) — unique
7. **Ship readiness checklist** (7-gate release process) — unique
8. **Domain-specific plugins** (django-pro, fastapi-pro, nextjs-pro, etc.) — unique

## RECOMMENDED NEW SKILLS TO BUILD

Priority order:

1. **P0 — project-discovery** (interactive elicitation with 3-tier questions, adaptive matrix, 8-step flow)
2. **P0 — tech-stack-advisor** (decision tree, trade-offs, templates, version verification)
3. **P0 — task-breaker** (spec/architecture -> ordered agent tasks with phases, milestones, deps)
4. **P0 — agent-prompt-builder** (synthesize all docs into single-shot agent prompt with checkpoints)
5. **P1 — design-pattern-advisor** (pattern catalog with selection guide and code sketches)
6. **P1 — branding-generator** (identity docs with color, typography, voice, assets)
7. **P1 — quality-checker** (post-generation checklists for each document type)
8. **P2 — workflow-orchestrator** (partial entry points, cross-skill awareness, adaptive depth)
