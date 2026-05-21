# senior-dev-squad-skills — maintenance rules

Repo = a Claude Code plugin **marketplace**. Read before changing structure.

## Layout
```
.claude-plugin/marketplace.json   # lists the 21 plugins (source: ./plugins/<name>)
plugins/
  senior-dev-squad/               # CORE plugin — cross-domain skills
    .claude-plugin/plugin.json
    skills/<name>/SKILL.md         # auto-discovered
  <x>-pro/                         # 20 domain plugins (1 skill each)
    .claude-plugin/plugin.json
    skills/<x>-pro/SKILL.md
templates/                        # SKILL-template.md, CONTEXT-FORMAT.md, ADR-FORMAT.md (not shipped)
incubator/  attic/                # in-progress / deprecated skills (NOT shipped)
docs/superpowers/{specs,plans}/   # design + plan records
scripts/check-consistency.py      # run before publishing
```

## Rules
- **Skills are auto-discovered** from each plugin's `skills/` dir. Do NOT add a `skills` map to `plugin.json`. Frontmatter = `name` + `description` only (no `model`/`user-invocable`/`always`).
- **marketplace.json lists plugins, not skills.** Adding a skill to the core plugin needs NO marketplace edit — only count/version updates. `source` MUST be `./plugins/<name>` (with `./`); bare names / `pluginRoot` are rejected by the validator.
- **Counts source of truth = disk.** README headline, marketplace `description`, and any count must equal `scripts/check-consistency.py` output (`N total = C core + D domain`).
- **Bar:** core skills follow the 7-section template (`templates/SKILL-template.md`): Overview/Core principle, Iron Law, When to Use, Red Flags, Common Rationalizations, Human-Partner Signals, Verification, Related Skills. Domain plugins use a lighter bar (description + When to Use + Related Skills).
- **Descriptions** are trigger-rich, third person, `<what>. Use when <triggers>.`, <~200 chars.
- **Lifecycle:** unfinished → `incubator/`, retired → `attic/`. Never under `plugins/`, never in `marketplace.json`.
- **Honesty:** skills are model-invoked from descriptions or wired via hooks; do NOT claim auto-trigger/always-on chaining.
- **Version bump** core `plugin.json` + marketplace core entry + README on any skill add/remove.

## Before publishing
```bash
python3 scripts/check-consistency.py   # must print CONSISTENCY: OK
claude plugin validate .               # marketplace + all 21 plugins
```
