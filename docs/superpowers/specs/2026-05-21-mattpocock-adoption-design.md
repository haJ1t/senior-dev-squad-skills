# Phase 4 — Adopt mattpocock/skills Strengths (A + B)

**Date:** 2026-05-21
**Goal:** Adopt the highest-ROI strengths from mattpocock/skills (98k★) into senior-dev-squad-skills: an interactive setup skill, skill lifecycle + index discipline, and the CONTEXT.md/ADR cohesion model with a grilling alignment skill.
**Scope:** Buckets **A** (setup + lifecycle) and **B** (CONTEXT/ADR cohesion). **Deferred:** C (progressive-disclosure split), D (deepen flagships).

## Why
mattpocock skills win on: ecosystem cohesion (shared glossary + ADRs read by every skill), interactive personalization (setup), and maintenance discipline (lifecycle buckets, enforced index). We have breadth (105 skills) + valid packaging but lack these. A+B close the biggest gaps without open-ended rewriting.

## Design items

### A · Setup + lifecycle discipline
1. **New core skill `setup-senior-dev-squad`** — `plugins/senior-dev-squad/skills/setup-senior-dev-squad/SKILL.md`. Interactive: asks issue tracker (GitHub / GitLab / Linear / local files), triage labels, and doc paths (where CONTEXT.md, docs/adr/, specs live). Writes the choices into a `CONTEXT.md` config block in the user's project. Lean single SKILL.md (trackers handled inline; no per-tracker variant files this round). Full 7-section template bar.
2. **Lifecycle dirs OUTSIDE `plugins/`** — `incubator/` (in-progress skills) and `attic/` (deprecated), each with a `README.md` explaining the convention. Non-shipped skills live here so they never enter `marketplace.json` / a plugin's `skills/` (mirrors mattpocock's personal/in-progress/deprecated rule). Created empty (READMEs only) this round.
3. **Index-consistency guard** — `scripts/check-consistency.py`: asserts every shipped core/domain skill is discoverable, counts match README headline, all frontmatter valid, no duplicate skill names, marketplace sources resolve. Repo-root **`CLAUDE.md`** documents maintenance rules (counts source of truth, version-bump rule, lifecycle dirs, run check-consistency before publish).

### B · CONTEXT + ADR cohesion
4. **New core skill `grill`** — relentless one-question-at-a-time alignment interview before building; challenges user terms against the project glossary; records resolved terms in `CONTEXT.md` and decisions as ADRs inline. Full 7-section template bar.
5. **Format specs** — `templates/CONTEXT-FORMAT.md` (ubiquitous-language glossary shape) + `templates/ADR-FORMAT.md` (ADR shape) so generated docs are consistent.
6. **Weave glossary/ADR awareness** into ~10 flagship core skills (spec-first-development, architecture-planner, code-reviewer, test-engineer, debugging or edge-case-hunter, refactor-simplifier, security-reviewer, performance-engineer, task-breaker, project-discovery): add a short `## Project Context` section — "If `CONTEXT.md` exists, use its glossary for naming; respect `docs/adr/`. If absent, consider `/senior-dev-squad:grill` or `/senior-dev-squad:setup-senior-dev-squad` first."

## File plan
- Create: `plugins/senior-dev-squad/skills/setup-senior-dev-squad/SKILL.md`
- Create: `plugins/senior-dev-squad/skills/grill/SKILL.md`
- Create: `templates/CONTEXT-FORMAT.md`, `templates/ADR-FORMAT.md`
- Create: `incubator/README.md`, `attic/README.md`
- Create: `scripts/check-consistency.py`, repo-root `CLAUDE.md`
- Modify: ~10 flagship `SKILL.md` (add `## Project Context`)
- Modify: `README.md` (counts 105→107, v3.4.0, changelog row, mention setup/grill + lifecycle), `.claude-plugin/marketplace.json` (metadata desc + core version 3.4.0), core `plugin.json` (version 3.4.0)

## Counts after
- **107 skills / 21 plugins** (85→87 core), v3.4.0. (Marketplace lists plugins, not skills → new core skills auto-included; no per-skill marketplace edit needed, only counts/version.)

## Verification
- New skills at 7/7 template bar + trigger-rich descriptions.
- `scripts/check-consistency.py` passes.
- `claude plugin validate .` passes (marketplace + all 21 plugins).
- `incubator/`/`attic/` contain only READMEs (not shipped).

## Out of scope (this round)
- C: splitting fat skills into SKILL.md + reference files.
- D: deep rewrites of diagnose/tdd/grill-tier flagships.
- Per-issue-tracker variant files for setup (inline for now).
- Actually moving any skill into incubator/attic (dirs + convention only).
