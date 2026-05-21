#!/usr/bin/env python3
"""Repo consistency guard for senior-dev-squad-skills.

Asserts:
  - every shipped skill (plugins/**/skills/*/SKILL.md) has valid frontmatter
    (name + description) and name == its directory;
  - skill directory names are globally unique (no accidental duplicates);
  - README headline count matches the real skill count on disk;
  - marketplace.json plugins all resolve (dir + .claude-plugin/plugin.json + skills/);
  - incubator/ and attic/ contents are NOT shipped (never under plugins/).

Exit 0 if consistent, 1 otherwise. Run before publishing.
Usage: python3 scripts/check-consistency.py
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
errors = []

def fm(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.match(r"^---\n(.*?)\n---", t, re.S)
    if not m:
        return None, None
    name = desc = None
    for line in m.group(1).splitlines():
        mm = re.match(r"(\w[\w-]*):\s*(.*)", line)
        if not mm:
            continue
        k, v = mm.group(1), mm.group(2).strip().strip('"').strip("'")
        if k == "name": name = v
        if k == "description": desc = v
    return name, desc

skills = glob.glob("plugins/**/skills/*/SKILL.md", recursive=True)
names = {}
for p in skills:
    d = os.path.basename(os.path.dirname(p))
    name, desc = fm(p)
    if not name or not desc:
        errors.append(f"{p}: missing frontmatter name/description")
    elif name != d:
        errors.append(f"{p}: frontmatter name '{name}' != dir '{d}'")
    names.setdefault(d, []).append(p)

dups = {k: v for k, v in names.items() if len(v) > 1}
for k, v in dups.items():
    errors.append(f"duplicate skill name '{k}': {v}")

core = len(glob.glob("plugins/senior-dev-squad/skills/*/SKILL.md"))
total = len(skills)
domain = total - core

# README headline count must mention the real total.
readme = open("README.md", encoding="utf-8", errors="replace").read()
if f"{total} skills" not in readme:
    errors.append(f"README.md does not state the real total '{total} skills' "
                  f"(disk: {total} total = {core} core + {domain} domain)")

# marketplace plugins resolve
mkt = json.load(open(".claude-plugin/marketplace.json"))
for pl in mkt["plugins"]:
    base = os.path.join("plugins", pl["source"].replace("./plugins/", "").lstrip("./"))
    if not os.path.exists(os.path.join(base, ".claude-plugin", "plugin.json")):
        errors.append(f"marketplace: unresolved plugin.json for {pl['name']}")
    if not os.path.isdir(os.path.join(base, "skills")):
        errors.append(f"marketplace: no skills/ dir for {pl['name']}")

# lifecycle dirs must not be shipped
for life in ("incubator", "attic"):
    for s in glob.glob(f"{life}/**/SKILL.md", recursive=True):
        if s.startswith("plugins/"):
            errors.append(f"{s}: lifecycle skill must not be under plugins/")

print(f"skills: {total} total = {core} core + {domain} domain | plugins: {len(mkt['plugins'])}")
if errors:
    print("CONSISTENCY: FAIL")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("CONSISTENCY: OK")
