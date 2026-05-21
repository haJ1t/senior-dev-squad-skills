# Phase 1 — Packaging & Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert `senior-dev-squad-skills` into a valid, installable Claude Code plugin marketplace (1 core plugin + 20 domain plugins) with consistent, non-misleading metadata.

**Architecture:** Hybrid topology (Option C). One `senior-dev-squad` core plugin holding 82 cross-domain skills, plus 20 standalone `*-pro` domain plugins, all listed in one root `.claude-plugin/marketplace.json`. Skills are auto-discovered from each plugin's `skills/` dir.

**Tech Stack:** Filesystem restructuring (bash), JSON metadata generation (python3), Claude Code plugin format, `claude plugin validate`.

**Working directory for ALL commands:** `/Users/halitozger/Desktop/megaskills/senior-dev-squad-skills`

**Reference spec:** `docs/superpowers/specs/2026-05-21-skillset-overhaul-design.md`

**Notes:**
- This dir is **not** a git repo. Task 0 makes a backup snapshot (moves are otherwise irreversible). Optional `git init` is Task 11.
- Scripts **compute** the move/domain lists from disk (domain set hardcoded) rather than hardcoding 35 names — deterministic and typo-proof.
- Final target: **82 core skills + 20 domain = 102 skills across 21 plugins.** (Initial estimate was 88/108; see Post-execution corrections at the bottom.)

---

## Task 0: Safety snapshot (no VCS → make a backup)

**Files:**
- Create: `../senior-dev-squad-skills.bak-20260521/` (sibling backup)

- [ ] **Step 1: Create timestamped backup**

Run from `/Users/halitozger/Desktop/megaskills`:
```bash
cd /Users/halitozger/Desktop/megaskills
rm -rf senior-dev-squad-skills.bak-20260521
cp -R senior-dev-squad-skills senior-dev-squad-skills.bak-20260521
```

- [ ] **Step 2: Verify backup integrity**

```bash
echo "orig: $(find senior-dev-squad-skills -name SKILL.md | wc -l) bak: $(find senior-dev-squad-skills.bak-20260521 -name SKILL.md | wc -l)"
```
Expected: `orig: 104 bak: 104` (counts match).

---

## Task 1: Authoritative inventory (single source of truth for later scripts)

**Files:**
- Create: `docs/superpowers/plans/_phase1-inventory.json`

- [ ] **Step 1: Write the inventory generator**

Create `docs/superpowers/plans/_inventory.py`:
```python
import os, json
DOMAINS = {"ai-app-security-pro","ai-ml-pro","blockchain-web3-pro","data-engineering-pro",
"devtools-pro","django-pro","docker-k8s-pro","ecommerce-pro","fastapi-pro","fintech-pro",
"game-dev-pro","healthtech-pro","mobile-pro","nextjs-pro","node-express-pro","observability-pro",
"postgres-pro","saas-pro","supabase-pro","terraform-pro"}
top = sorted(d for d in os.listdir("plugins")
             if os.path.isdir(f"plugins/{d}") and d != "senior-dev-squad")
direct = [d for d in top if os.path.exists(f"plugins/{d}/SKILL.md")]
domains = sorted(d for d in direct if d in DOMAINS)
nondomain = sorted(d for d in direct if d not in DOMAINS)
moves = [d for d in nondomain if d != "cross-model-reviewer"]   # dup handled in Task 2
inv = {"domains": domains, "nondomain": nondomain, "moves": moves,
       "dup": "cross-model-reviewer"}
json.dump(inv, open("docs/superpowers/plans/_phase1-inventory.json","w"), indent=2)
print("domains:", len(domains), "nondomain:", len(nondomain), "moves:", len(moves))
assert len(domains) == 20, f"expected 20 domains, got {len(domains)}"
assert len(moves) == 35, f"expected 35 moves, got {len(moves)}"
print("OK")
```

- [ ] **Step 2: Run it and verify**

```bash
python3 docs/superpowers/plans/_inventory.py
```
Expected: `domains: 20 nondomain: 36 moves: 35` then `OK`.

---

## Task 2: Dedupe `cross-model-reviewer`

**Files:**
- Compare: `plugins/cross-model-reviewer/SKILL.md` vs `plugins/senior-dev-squad/skills/cross-model-reviewer/SKILL.md`
- Delete: `plugins/cross-model-reviewer/` (after keeping the better copy)

- [ ] **Step 1: Diff the two copies**

```bash
diff plugins/cross-model-reviewer/SKILL.md plugins/senior-dev-squad/skills/cross-model-reviewer/SKILL.md && echo "IDENTICAL" || echo "DIFFER"
wc -l plugins/cross-model-reviewer/SKILL.md plugins/senior-dev-squad/skills/cross-model-reviewer/SKILL.md
```

- [ ] **Step 2: Keep the better copy in core, then remove top-level**

Rule: if the **top-level** copy has MORE lines (richer), promote it into core first; otherwise core already wins. Then delete the top-level dir.
```bash
TOP=plugins/cross-model-reviewer/SKILL.md
CORE=plugins/senior-dev-squad/skills/cross-model-reviewer/SKILL.md
if [ "$(wc -l < "$TOP")" -gt "$(wc -l < "$CORE")" ]; then cp "$TOP" "$CORE"; echo "promoted top-level into core"; else echo "core copy kept"; fi
rm -rf plugins/cross-model-reviewer
```

- [ ] **Step 3: Verify dedupe**

```bash
test ! -e plugins/cross-model-reviewer && test -e plugins/senior-dev-squad/skills/cross-model-reviewer/SKILL.md && echo "DEDUPE OK"
```
Expected: `DEDUPE OK`.

---

## Task 3: Move the 35 non-domain top-level skills into the core plugin

**Files:**
- Move: each `plugins/<skill>/` → `plugins/senior-dev-squad/skills/<skill>/` (35 dirs)

- [ ] **Step 1: Run the move (idempotent — skips if already present)**

```bash
python3 - <<'PY'
import json, os, shutil
mv = json.load(open("docs/superpowers/plans/_phase1-inventory.json"))["moves"]
dest_root = "plugins/senior-dev-squad/skills"
done = 0
for d in mv:
    src = f"plugins/{d}"
    dst = f"{dest_root}/{d}"
    if os.path.exists(dst):
        print("skip (exists):", d); continue
    assert os.path.exists(src), f"missing source {src}"
    shutil.move(src, dst); done += 1
print("moved:", done)
PY
```
Expected: `moved: 35` (or fewer if re-run, with `skip (exists)` lines).

- [ ] **Step 2: Verify core skill count**

```bash
python3 - <<'PY'
import os
core = [d for d in os.listdir("plugins/senior-dev-squad/skills")
        if os.path.isdir(f"plugins/senior-dev-squad/skills/{d}")]
real = [d for d in core if d != "_template"]
print("core dirs:", len(core), "real (excl _template):", len(real))
assert len(real) == 88, f"expected 88 real core skills, got {len(real)}"
print("CORE COUNT OK")
PY
```
Expected: `core dirs: 89 real (excl _template): 88` then `CORE COUNT OK`.

---

## Task 4: Restructure the 20 domain dirs into valid plugins

Each domain currently is `plugins/<x>/SKILL.md`; a valid plugin needs `plugins/<x>/skills/<x>/SKILL.md`.

**Files:**
- For each domain `<x>`: create `plugins/<x>/skills/<x>/`, move `plugins/<x>/SKILL.md` into it.

- [ ] **Step 1: Run the restructure (idempotent)**

```bash
python3 - <<'PY'
import json, os, shutil
domains = json.load(open("docs/superpowers/plans/_phase1-inventory.json"))["domains"]
done = 0
for d in domains:
    flat = f"plugins/{d}/SKILL.md"
    nested_dir = f"plugins/{d}/skills/{d}"
    nested = f"{nested_dir}/SKILL.md"
    if os.path.exists(nested):
        print("skip (done):", d); continue
    assert os.path.exists(flat), f"missing {flat}"
    os.makedirs(nested_dir, exist_ok=True)
    shutil.move(flat, nested); done += 1
print("restructured:", done)
PY
```
Expected: `restructured: 20`.

- [ ] **Step 2: Verify every domain has the nested skill and no stray flat SKILL.md**

```bash
python3 - <<'PY'
import json, os
domains = json.load(open("docs/superpowers/plans/_phase1-inventory.json"))["domains"]
bad = []
for d in domains:
    if not os.path.exists(f"plugins/{d}/skills/{d}/SKILL.md"): bad.append(("missing-nested", d))
    if os.path.exists(f"plugins/{d}/SKILL.md"): bad.append(("flat-remains", d))
print("problems:", bad)
assert not bad
print("DOMAIN STRUCTURE OK")
PY
```
Expected: `problems: []` then `DOMAIN STRUCTURE OK`.

---

## Task 5: Move `_template` out of `skills/`

**Files:**
- Create: `templates/SKILL-template.md`
- Delete: `plugins/senior-dev-squad/skills/_template/`

- [ ] **Step 1: Relocate the template**

```bash
mkdir -p templates
mv plugins/senior-dev-squad/skills/_template/SKILL.md templates/SKILL-template.md
rmdir plugins/senior-dev-squad/skills/_template
```

- [ ] **Step 2: Verify**

```bash
test -f templates/SKILL-template.md && test ! -e plugins/senior-dev-squad/skills/_template && echo "TEMPLATE MOVED OK"
```
Expected: `TEMPLATE MOVED OK`.

---

## Task 6: Generate correct `plugin.json` for all 21 plugins

Drops the non-standard `skills{}` map; relies on auto-discovery. Domain descriptions are read from each domain skill's existing frontmatter (no hardcoding).

**Files:**
- Overwrite: `plugins/senior-dev-squad/.claude-plugin/plugin.json`
- Create: `plugins/<domain>/.claude-plugin/plugin.json` (×20)

- [ ] **Step 1: Write the generator**

```bash
python3 - <<'PY'
import json, os, re
AUTHOR = {"name": "senior-dev-squad"}
LICENSE = "MIT"
HOME = "https://github.com/senior-dev-squad/senior-dev-squad-skills"
def desc_of(skillmd):
    t = open(skillmd, encoding="utf-8", errors="replace").read()
    m = re.search(r'^description:\s*(.*)$', t, re.M)
    return (m.group(1).strip().strip('"').strip("'")) if m else ""
def write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, "w"), indent=2); open(path,"a").write("\n")

# CORE
write("plugins/senior-dev-squad/.claude-plugin/plugin.json", {
    "name": "senior-dev-squad",
    "description": "Production-grade senior-engineer SDLC squad: spec, architecture, frontend/backend, security, testing, DevOps, review, ship, plus guardrails, orchestration, design systems, security frameworks, repo automation, MCP, agent platform, product, marketing, AI/ML, DevEx, compliance, and advanced testing skills.",
    "version": "3.2.0",
    "author": AUTHOR, "license": LICENSE, "homepage": HOME,
    "repository": HOME,
    "keywords": ["sdlc","fullstack","security","testing","devops","code-review","orchestration","design-system","ai-ml","compliance"]
})

# DOMAINS
domains = json.load(open("docs/superpowers/plans/_phase1-inventory.json"))["domains"]
for d in domains:
    write(f"plugins/{d}/.claude-plugin/plugin.json", {
        "name": d,
        "description": desc_of(f"plugins/{d}/skills/{d}/SKILL.md"),
        "version": "1.0.0",
        "author": AUTHOR, "license": LICENSE, "homepage": HOME, "repository": HOME,
        "keywords": [d.replace("-pro",""), "domain"]
    })
print("wrote", 1 + len(domains), "plugin.json files")
PY
```
Expected: `wrote 21 plugin.json files`.

- [ ] **Step 2: Verify all 21 are valid JSON with required fields**

```bash
python3 - <<'PY'
import json, glob
files = glob.glob("plugins/**/.claude-plugin/plugin.json", recursive=True)
assert len(files) == 21, f"expected 21, got {len(files)}"
for f in files:
    o = json.load(open(f))
    for k in ("name","description","version"):
        assert o.get(k), f"{f} missing {k}"
    assert "skills" not in o, f"{f} still has legacy skills map"
print("ALL 21 plugin.json VALID")
PY
```
Expected: `ALL 21 plugin.json VALID`.

---

## Task 7: Generate root `.claude-plugin/marketplace.json`

**Files:**
- Create: `.claude-plugin/marketplace.json`
- Delete: old `marketplace.json` (skills.sh schema) at repo root

- [ ] **Step 1: Write the generator (reads each plugin.json description)**

```bash
python3 - <<'PY'
import json, os
def pdesc(name):
    return json.load(open(f"plugins/{name}/.claude-plugin/plugin.json"))["description"]
domains = json.load(open("docs/superpowers/plans/_phase1-inventory.json"))["domains"]
plugins = [{"name":"senior-dev-squad","source":"senior-dev-squad","description":pdesc("senior-dev-squad")}]
for d in domains:
    plugins.append({"name":d,"source":d,"description":pdesc(d)})
mkt = {
  "name":"senior-dev-squad",
  "owner":{"name":"senior-dev-squad"},
  "metadata":{"description":"Senior dev squad: 1 core SDLC plugin + 20 domain plugins (108 skills).","version":"3.2.0","pluginRoot":"./plugins"},
  "plugins":plugins
}
os.makedirs(".claude-plugin", exist_ok=True)
json.dump(mkt, open(".claude-plugin/marketplace.json","w"), indent=2); open(".claude-plugin/marketplace.json","a").write("\n")
print("marketplace entries:", len(plugins))
assert len(plugins) == 21
PY
rm -f marketplace.json
```
Expected: `marketplace entries: 21`.

- [ ] **Step 2: Verify marketplace + that every source dir resolves**

```bash
python3 - <<'PY'
import json, os
m = json.load(open(".claude-plugin/marketplace.json"))
root = m["metadata"]["pluginRoot"].lstrip("./")
assert m["name"] and m["owner"]["name"]
for p in m["plugins"]:
    pj = os.path.join(root, p["source"], ".claude-plugin", "plugin.json")
    assert os.path.exists(pj), f"unresolved source: {pj}"
    sk = os.path.join(root, p["source"], "skills")
    assert os.path.isdir(sk), f"no skills/ dir for {p['name']}"
assert not os.path.exists("marketplace.json"), "old skills.sh marketplace.json still present"
print("MARKETPLACE OK:", len(m["plugins"]), "plugins, all sources resolve")
PY
```
Expected: `MARKETPLACE OK: 21 plugins, all sources resolve`.

---

## Task 8: Validate with Claude Code (with python fallback)

**Files:** none (validation only)

- [ ] **Step 1: Try the official validator**

```bash
claude plugin validate . 2>&1 | tail -20 || echo "CLI_UNAVAILABLE"
```
Expected: validation success message. If output is `CLI_UNAVAILABLE` or command-not-found, use Step 2.

- [ ] **Step 2: Fallback structural validation**

```bash
python3 - <<'PY'
import json, os, glob, re
errs = []
# marketplace
m = json.load(open(".claude-plugin/marketplace.json"))
names = [p["name"] for p in m["plugins"]]
if len(names) != len(set(names)): errs.append("duplicate plugin names")
# each plugin: plugin.json + >=1 SKILL.md with description
for p in m["plugins"]:
    base = os.path.join("plugins", p["source"])
    skills = glob.glob(f"{base}/skills/*/SKILL.md")
    if not skills: errs.append(f"{p['name']}: no skills")
    for s in skills:
        t = open(s, encoding="utf-8", errors="replace").read()
        if not re.search(r'^description:\s*\S', t, re.M): errs.append(f"{s}: no description")
# global skill-name uniqueness within each plugin
for p in m["plugins"]:
    dirs = [os.path.basename(os.path.dirname(s)) for s in glob.glob(f"plugins/{p['source']}/skills/*/SKILL.md")]
    if len(dirs) != len(set(dirs)): errs.append(f"{p['name']}: dup skill dirs")
total = len(glob.glob("plugins/**/skills/*/SKILL.md", recursive=True))
print("total skills:", total)
print("ERRORS:", errs if errs else "NONE")
assert not errs
assert total == 108, f"expected 108 skills, got {total}"
print("STRUCTURAL VALIDATION OK")
PY
```
Expected: `total skills: 108`, `ERRORS: NONE`, `STRUCTURAL VALIDATION OK`.

---

## Task 9: Consistency sweep — fix counts, install instructions, and honesty overclaims

Update headline metadata and remove misleading runtime claims. Detailed per-phase tables are re-tallied in Phase 2; here we fix headline numbers, version, install commands, and false "automatic" claims.

**Files:**
- Modify: `README.md`
- Modify: `PIPELINE.md`
- Modify: `PHASE-ROADMAP.md` (only if it states totals)

- [ ] **Step 1: README — version + headline counts**

In `README.md`, replace the version in the H1 (`v3.1.0` → `v3.2.0`). Replace the headline blurb so it reads (exact target):
```
> **108 skills across 21 installable Claude Code plugins** (1 core senior-dev-squad plugin + 20 domain plugins). Complete SDLC pipeline: spec → architecture → frontend/backend → security → testing → DevOps → review → ship. Plus guardrails, orchestration, design systems, security frameworks, repo automation, MCP integration, agent platforms, marketing, product management, cross-provider teams, AI/ML pipelines, developer experience, compliance, advanced testing, and distributed-systems architecture.
```
Remove the contradictory line `**82 skills** + **20 domain plugins** = **102 packages, 767 KB** ...` and any other "102/103/82/83 packages" phrasing. Replace with: `**88 core skills + 20 domain plugins = 108 skills / 21 plugins.**`

- [ ] **Step 2: README — fix install section**

Replace the Installation block with the correct Claude Code flow:
````
## Installation

```bash
# 1. Add the marketplace (from GitHub or a local clone)
/plugin marketplace add senior-dev-squad/senior-dev-squad-skills

# 2. Install the core squad and any domain plugins you want
/plugin install senior-dev-squad@senior-dev-squad
/plugin install nextjs-pro@senior-dev-squad

# 3. Invoke skills (namespaced by plugin)
/senior-dev-squad:spec-first-development
/nextjs-pro:nextjs-pro
```
````
Delete the old `claude plugin install senior-dev-squad`, the `cp -r plugins/* ~/.hermes/skills/`, and `cp -r plugins/senior-dev-squad ~/.claude/plugins/` lines (the cp approaches no longer match the structure).

- [ ] **Step 3: README + PIPELINE — fix honesty overclaims**

In `README.md` Philosophy and in `PIPELINE.md`:
- Reword "Always-on guardrails ... never need to be invoked" / "Guardrails run always" → `Guardrails (instincts-guardrails, agent-shield, research-first, session-memory) are *model-invoked based on their descriptions*, and can be made always-on by wiring them as hooks (see each skill's README).`
- Reword the auto-trigger language: change "automatically triggered" / "[auto]" framing to **recommended sequencing**. Add a one-line banner at the top of `PIPELINE.md`:
```
> These chains are RECOMMENDED sequencing, not automatic. Claude Code does not auto-run the next skill; invoke the next skill yourself or wire chaining via hooks.
```

- [ ] **Step 4: README — fix File Statistics + Phase Map totals**

Update the File Statistics table: `Total Packages` → `21 plugins (1 core + 20 domain)`; `Total Skill Files` → `108 (+1 template)`. In the Phase Map table, change the cumulative `Total` to `108 skills / 21 plugins`, and add a note under it: `_Per-phase buckets are re-tallied for accuracy in the Phase 2 content pass._`

- [ ] **Step 5: Verify no stale numbers remain in headline locations**

```bash
grep -nE "v3\.1\.0|= *10[23] *packages|8[23] *skills|claude plugin install senior-dev-squad\b|hermes/skills" README.md || echo "NO STALE HEADLINE NUMBERS"
grep -nE "automatically triggered|never need to be invoked|run at EVERY step" PIPELINE.md README.md || echo "NO OVERCLAIMS"
```
Expected: both print the `NO ...` lines (no matches). Investigate and fix any remaining hits.

---

## Task 10: Final verification & cleanup

**Files:**
- Delete: `docs/superpowers/plans/_inventory.py`, `docs/superpowers/plans/_phase1-inventory.json` (scratch artifacts)

- [ ] **Step 1: Full re-verification**

```bash
python3 - <<'PY'
import glob, os, json
core = [d for d in os.listdir("plugins/senior-dev-squad/skills") if os.path.isdir(f"plugins/senior-dev-squad/skills/{d}")]
total = len(glob.glob("plugins/**/skills/*/SKILL.md", recursive=True))
pj = len(glob.glob("plugins/**/.claude-plugin/plugin.json", recursive=True))
mkt = json.load(open(".claude-plugin/marketplace.json"))
checks = {
  "core_real_skills": len(core),               # expect 88
  "total_skills": total,                        # expect 108
  "plugin_json_count": pj,                       # expect 21
  "marketplace_entries": len(mkt["plugins"]),   # expect 21
  "template_gone": not os.path.exists("plugins/senior-dev-squad/skills/_template"),
  "dup_gone": not os.path.exists("plugins/cross-model-reviewer"),
  "old_marketplace_gone": not os.path.exists("marketplace.json"),
  "template_relocated": os.path.exists("templates/SKILL-template.md"),
}
print(json.dumps(checks, indent=2))
assert checks["core_real_skills"]==88 and checks["total_skills"]==108
assert checks["plugin_json_count"]==21 and checks["marketplace_entries"]==21
assert all([checks["template_gone"],checks["dup_gone"],checks["old_marketplace_gone"],checks["template_relocated"]])
print("PHASE 1 COMPLETE — ALL CHECKS PASS")
PY
```
Expected: all values as commented, then `PHASE 1 COMPLETE — ALL CHECKS PASS`.

- [ ] **Step 2: Remove scratch inventory artifacts**

```bash
rm -f docs/superpowers/plans/_inventory.py docs/superpowers/plans/_phase1-inventory.json
echo "cleaned"
```

- [ ] **Step 3: Manual smoke test (human/agent, interactive — optional)**

In a Claude Code session: `/plugin marketplace add /Users/halitozger/Desktop/megaskills/senior-dev-squad-skills` then `/plugin install senior-dev-squad@senior-dev-squad`. Confirm install succeeds and `/senior-dev-squad:` skills appear.

---

## Task 11 (optional): Initialize git

**Files:** Create `.gitignore`

- [ ] **Step 1: Init + ignore backup/scratch**

```bash
git init
printf "*.bak-*/\n.DS_Store\ndocs/superpowers/plans/_*.json\n" > .gitignore
git add -A
git commit -m "chore: restructure into installable Claude Code marketplace (Phase 1)"
```
Expected: a clean initial commit. (Run only if version control is wanted.)

---

## Self-Review (against spec)

- **Spec coverage:** Phase 1 spec steps 1–7 all mapped → moves (T3), dedupe (T2), domain restructure (T4), `_template` relocate (T5), metadata gen (T6/T7), validation (T8), consistency+honesty (T9). ✓
- **Counts:** 88 core / 108 total / 21 plugins used consistently across all tasks and asserts. ✓
- **No placeholders:** every step has runnable commands/scripts and expected output. ✓
- **Reversibility:** Task 0 backup compensates for no VCS. ✓
- **Idempotency:** move/restructure scripts skip already-done items. ✓

---

## Post-execution corrections (2026-05-21)

Discovered during execution; recorded for accuracy:

1. **Empty stub dirs:** core had 6 empty placeholder dirs (`multi-agent-debate`, `opportunity-solver`, `provider-router`, `roadmap-prioritizer`, `user-story-refiner`, `validation-designer`) with no `SKILL.md`. They masked the real top-level copies and inflated the initial disk estimate. Removed them; moved the real copies in.
2. **Real counts:** **82 core + 20 domain = 102 skills / 21 plugins** (not the estimated 88/108). Any task asserts above that say 88/108 are superseded by 82/102.
3. **marketplace `source` format:** `claude plugin validate` **rejects** bare names + `metadata.pluginRoot`. Correct form is `"source": "./plugins/<name>"` (with `./` prefix). marketplace.json was regenerated accordingly; official validation passes for the marketplace and all 21 plugins.
