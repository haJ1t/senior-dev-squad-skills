# Skill-Set Overhaul — Design Spec

**Date:** 2026-05-21
**Project:** senior-dev-squad-skills
**Goal:** Make the skill set publishable for others as Claude Code plugins — correct packaging, consistent metadata, high content quality, and expanded coverage.
**Topology decision:** Hybrid (Option C) — one core plugin + 20 standalone domain plugins under one marketplace.

---

## 1. Background & motivation

`senior-dev-squad-skills` is a large collection of AI-agent skills (the "senior dev squad") plus 20 domain `*-pro` packages. It is intended for **public distribution** so others can install and run it as Claude Code plugins.

The content is in good shape, but **packaging is broken** and **metadata is inconsistent**, so the repo cannot actually be installed via Claude Code today.

### Verified current-state findings

Content (audit of 104 `SKILL.md`):
- All 104 have valid YAML frontmatter; every `name` matches its directory.
- No stub/thin skills (line counts min/median/max = 89 / 190 / 693).
- No empty or oversized descriptions.
- Exactly **1 duplicate**: `cross-model-reviewer` exists in both `plugins/cross-model-reviewer/` and `plugins/senior-dev-squad/skills/cross-model-reviewer/`.

Packaging / metadata (broken):
- Only **1 real plugin** exists (`plugins/senior-dev-squad/` has `.claude-plugin/plugin.json`). **55 top-level `plugins/<name>/` dirs are bare `SKILL.md` with no `plugin.json`** → not installable.
- `plugin.json` uses a **non-standard schema**: a `skills{}` object map plus `user-invocable` / `always` / `model` keys. Claude Code **auto-discovers** skills from `skills/<name>/SKILL.md`; no such map is used. It also lists only 19 skills (47 exist), is `version: 1.0.0`, and its description says "12 skills".
- `marketplace.json` uses the **`skills.sh` schema**, not Claude Code's. Claude Code needs `.claude-plugin/marketplace.json` with `name` + `owner{}` + `plugins[]`.
- **Count chaos**: README title says 102 but body says both 102 and 103, and both "82 skills" and "83 skills"; `marketplace.json` says 103/83; roadmap says "100+".
- **Honesty risk for a public repo**: README/`PIPELINE.md` claim auto-triggering skill chains and "always-on, never invoked" guardrails. Standard Claude Code skills do **not** auto-chain and are **not** always-on (that requires hooks). This overclaims mechanics the runtime doesn't provide.

### Authoritative Claude Code packaging format (confirmed against official docs)

- Marketplace: `.claude-plugin/marketplace.json` → `{ name, owner{name,email?}, metadata?{pluginRoot}, plugins:[{name, source, description, version?}] }`. One marketplace can list many plugins; `source` must be a relative path **with `./` prefix** (e.g. `./plugins/foo`). NOTE: bare names + `metadata.pluginRoot` are **rejected** by `claude plugin validate` — use explicit `./plugins/<name>` (confirmed against real installed marketplaces).
- Plugin: `.claude-plugin/plugin.json` → `{ name, description, version?, author?, homepage?, repository?, license?, keywords? }`. **Skills auto-discovered** from `skills/`; no `skills` map required.
- Skill: `skills/<kebab-name>/SKILL.md`, frontmatter requires `description` (drives auto-triggering; concise/trigger-rich). `name` matches folder. Optional `disable-model-invocation`.
- Install: `/plugin marketplace add <git-url-or-repo>` → `/plugin install <plugin>@<marketplace>`. Invoke `/<plugin>:<skill>`.
- Validate: `claude plugin validate .` (marketplace) and `claude plugin validate ./plugins/<x>` (plugin).
- Docs: code.claude.com/docs/en/plugins-reference, /plugin-marketplaces, /plugins.

---

## 2. Target architecture (Hybrid / Option C)

```
senior-dev-squad-skills/                  # repo root == the marketplace
├── .claude-plugin/
│   └── marketplace.json                  # ONE marketplace, 21 plugin entries
├── plugins/
│   ├── senior-dev-squad/                 # CORE plugin (~81 skills)
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/<skill>/SKILL.md        # auto-discovered
│   ├── nextjs-pro/                        # domain plugin (1 skill each)
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/nextjs-pro/SKILL.md
│   └── … 19 more *-pro plugins
├── templates/SKILL-template.md           # former _template, NOT shipped as a skill
├── README.md  LICENSE  PIPELINE.md  references/  scripts/
```

### Core vs domain split

- **Domain plugins (20, standalone):** ai-app-security-pro, ai-ml-pro, blockchain-web3-pro, data-engineering-pro, devtools-pro, django-pro, docker-k8s-pro, ecommerce-pro, fastapi-pro, fintech-pro, game-dev-pro, healthtech-pro, mobile-pro, nextjs-pro, node-express-pro, observability-pro, postgres-pro, saas-pro, supabase-pro, terraform-pro.
- **Core plugin (everything else):** 47 real skills already in `senior-dev-squad/skills/` + 35 non-domain top-level skills moved in (36 non-domain dirs minus the `cross-model-reviewer` dup, deleted not moved). 6 empty stub dirs in core were removed (they had masked the real top-level copies). = **82 skills**.

### Final counts (verify exactly at build)

- **105 skills** total = 85 core + 20 domain (was 102 after Phase 1/2; Phase 3 added 3 bucket-D skills).
- **21 plugins** = 1 core + 20 domain.
- (README's old 83/103 was nearly right; true core count is 82 — my initial disk estimate of 88 was inflated by 6 empty stub dirs + `_template`. Validator-confirmed: 102 skills / 21 plugins.)
- All README / `marketplace.json` / `plugin.json` / `PIPELINE.md` / roadmap standardized to these numbers.

### Conventions / decisions

- Domain plugin's single skill keeps the domain name → invoked `/nextjs-pro:nextjs-pro` (minor redundancy, accepted).
- Core skills invoked `/senior-dev-squad:<skill>`.
- The old `skills.sh`-schema `marketplace.json` is **replaced** by the Claude Code `.claude-plugin/marketplace.json` (single source of truth). If skills.sh publishing is wanted later, regenerate separately.
- `_template` moves to `templates/SKILL-template.md` so it is not discovered/shipped as a skill.

---

## 3. Phased plan

### Phase 1 — Packaging & consistency (foundation; makes it installable)

1. Move the 35 non-domain top-level skill dirs into `plugins/senior-dev-squad/skills/` (the 36th, `cross-model-reviewer`, is the dup — deleted in step 2, not moved).
2. Dedupe `cross-model-reviewer`: diff both copies, keep the better, delete the top-level one.
3. Convert each of the 20 domain dirs into a valid plugin: `plugins/<x>-pro/.claude-plugin/plugin.json` + `plugins/<x>-pro/skills/<x>-pro/SKILL.md`.
4. Move `_template` → `templates/SKILL-template.md`.
5. Generate metadata:
   - Correct `senior-dev-squad/.claude-plugin/plugin.json` (proper schema; drop the `skills{}` map; real version/description/author/license/keywords).
   - 20 domain `plugin.json` files.
   - Root `.claude-plugin/marketplace.json` (name, owner, `metadata.pluginRoot: ./plugins`, 21 plugin entries). Remove old `marketplace.json`.
6. Validate: `claude plugin validate .` and each plugin until clean.
7. Consistency sweep: README / `PIPELINE.md` / roadmap counts + version agree (101 skills / 21 plugins). Fix honesty overclaims — reword auto-trigger "chains" as *recommended sequencing*, and "always-on guardrails" as *model-invoked via description, or wired via hooks*.

**Phase 1 exit criteria:** `claude plugin validate` passes for marketplace + all 21 plugins; a test `/plugin marketplace add <local path>` + `/plugin install senior-dev-squad@…` succeeds; no duplicate skills; all docs agree on counts; no false runtime claims.

### Phase 2 — Content quality (executed in category waves)

8. Conformance audit: score all 101 skills against `templates/SKILL-template.md` sections — Overview/Core principle, Iron Law, When-to-Use, Red Flags, Common Rationalizations, Human-Partner Signals, Verification checklist, Related Skills. Produce a gap table.
9. Bring non-conformant skills up to the bar (add missing sections, strengthen weak ones).
10. Optimize every `description` for auto-triggering (third-person, trigger-rich, concise); keep `SKILL.md` ↔ `plugin.json` ↔ `marketplace.json` descriptions in sync.
11. Fix `Related Skills` cross-links to use namespaced invocation (`/<plugin>:<skill>`).

**Phase 2 exit criteria:** every skill hits the template bar; descriptions consistent across all three metadata layers; cross-links valid.

### Phase 3 — Expansion (skill list decided with the user)

12. Fresh gap analysis (the original `gap-analysis-project-architect.md` items are mostly built now); identify genuinely missing, high-value skills for a public SDLC squad. **Agree the list with the user before building.**
13. Build new skills from the template; register them in `plugin.json`/`marketplace.json`; update all counts.

**Phase 3 exit criteria:** agreed new skills built to template bar, validated, and reflected in all metadata/counts.

---

## 4. Execution order

Phase 1 fully first (delivers an installable, consistent, validated repo), then Phase 2 in category waves, then Phase 3 after the new-skill list is agreed.

## 5. Out of scope (this round)

- Publishing to non–Claude-Code marketplaces (e.g. skills.sh) — can regenerate later.
- Renaming domain plugins' inner skills to verb-style names (kept as-is for minimal disruption).
- Building Phase 3 skills before the list is agreed.

## 6. Open items

- Final skill count (validator-confirmed): 105 skills / 21 plugins (85 core + 20 domain). Phase 1/2 = 102; Phase 3 added 3 (i18n-localization-engineer, realtime-systems-engineer, finops-cost-optimizer).
- Repo is **not** git-initialized (`git init` = false). Spec is written but not committed; run `git init` if version control is wanted before publishing.
- Phase 3 new-skill list — to be decided with the user.

## 7. Risks

- Large core plugin (~82 skills) loads ~82 descriptions into every user session once installed (always-on cost). Accepted under Option C; mitigated by tight descriptions in Phase 2.
- Bulk directory moves risk path breakage in docs/scripts referencing old paths — Phase 1 step 7 covers reference fixes; validate after moves.
