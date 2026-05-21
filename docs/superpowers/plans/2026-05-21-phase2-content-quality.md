# Phase 2 — Content Quality Implementation Plan

> Section-presence + description-triggering pass. Deep content rewrite deferred to Phase 2.5/3.

**Goal:** Every core skill hits the 7-section template bar; every domain plugin hits the lighter domain bar; all descriptions are trigger-optimized.

**Bar definitions:**
- **Core (7/7):** Overview/Core principle, The Iron Law, When to Use, Red Flags, Common Rationalizations, Human-Partner Signals, Verification checklist, Related Skills.
- **Domain (lighter):** strong description, Purpose/Overview, When to Use, structured pattern sections (already present), Related Skills. NO forced Iron Law/Rationalizations/Human-Signals.

**Exemplar:** `plugins/senior-dev-squad/skills/spec-first-development/SKILL.md` (canonical section formats).

**Rules:**
- ADD missing sections only; do NOT rewrite existing good sections.
- Content must be SPECIFIC to each skill — no generic filler, no placeholders/TBD.
- Match exemplar heading text exactly (e.g. `## Your Human Partner's Signals You're Doing It Wrong`).
- No git (not a repo).

## Wave 1 — Core sub-bar (17 skills → 7/7)

Per-skill missing sections (from audit):
- ship-readiness-checklist: when, redflag, ration, human, verif, related
- backend-senior-engineer: redflag, ration, human, related
- edge-case-hunter: redflag, ration, human, related
- refactor-simplifier: when, human, verif, related
- devops-release-engineer: human, verif, related
- design-pattern-advisor: redflag, ration, human
- performance-engineer: when, human, related
- code-reviewer: when, ration, human
- branding-generator: iron, ration, human
- quality-checker: ration, human
- agent-prompt-builder: ration, human
- task-breaker: ration, human
- architecture-planner: human, related
- project-discovery: human
- agent-shield: ration
- tech-stack-advisor: human
- security-reviewer: human

## Wave 2 — Domain lighter bar (20 plugins)

Add **When to Use** + **Related Skills** to all 20 `plugins/<x>/skills/<x>/SKILL.md` (ai-app-security-pro needs only Related). Related Skills should cross-link relevant core skills (e.g. nextjs-pro → frontend-senior-engineer, performance-engineer).

## Wave 3 — Description triggering (102 skills)

Rewrite each frontmatter `description` to trigger-rich third-person form: `<what it does>. Use when <trigger cues>.` Keep concise (<~200 chars). Sync description into `plugin.json` (domain) + `marketplace.json` after.

## Verification

- Re-run conformance audit: core 82/82 at 7/7; domain 20/20 have when+related.
- `claude plugin validate .` passes.

## Deferred (not this round)
- Strip stray cruft (wrong "Output Schema", "Scoring Rubric", "LLM Anti-Patterns" copy-paste; legacy `model/user-invocable/always` frontmatter in domains).
- Reword in-skill "Chaining (Auto-Trigger)" → recommended (honesty), matching Phase 1.
