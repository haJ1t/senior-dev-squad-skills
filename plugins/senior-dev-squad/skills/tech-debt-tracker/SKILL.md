---
name: tech-debt-tracker
description: "Scanning, categorizing, prioritizing, reporting technical debt, Harness Craft methodology. Use when identifying or triaging tech debt in a codebase."
---

# Tech Debt Tracker

## Overview

This skill systematically scans, categorizes, prioritizes, and registers technical debt within the codebase. It makes technical debt visible, ranging from simple TODO/FIXME/HACK comments to complex code smells, duplicate code blocks, high cyclomatic complexity, outdated dependencies, and documentation gaps. The goal is to move technical debt from an "invisible" friction point into a measurable, manageable, and strategically addressable backlog item.

**Core principle:** Technical debt is a measurement, not an accusation. Debt that is not measured cannot be paid off.

## The Iron Law

```
TECHNICAL DEBT MUST NEVER BE MANAGED SOLELY BY INTUITION. EVERY DEBT ITEM MUST BE SCANNED, DOCUMENTED, PRIORITIZED, AND TRACKED IN A REGISTER.
```

## When to Use

**Use this when:**
- Joining a new project or team and evaluating the existing codebase.
- Planning sprint items to determine which refactoring or clean-up tasks to prioritize.
- Working on a new feature and needing to understand pre-existing debt in affected areas.
- Investigating performance bottlenecks or security vulnerabilities.
- Recording recurring code patterns flagged during code reviews.

**Use this ESPECIALLY when:**
- The team defaults to a "we'll clean it up later" culture.
- Production failures are traced back to unaddressed technical debt.
- A new engineer joins and is confused by the state of the codebase.
- Upgrading package dependencies has been deferred for an extended period.

**Don't skip when:**
- The codebase is new and lacks debt (run a scan anyway to establish a baseline).
- The project is archived or read-only.

## Phase 1: Code Smell Scanning (TODO/FIXME/HACK/XXX)

**BEFORE proceeding:**

1. **Perform a regex scan** across the codebase to look for tags: `TODO`, `FIXME`, `HACK`, `XXX`, `BUG`, `WORKAROUND`, `TEMP`, `KLUDGE`.
2. **Gather context for each finding** — record the file path, line number, and enclosing code block.
3. **Trace the age** of the comment using `git blame` to determine how long the tag has existed.
4. **Categorize each tag** (e.g., TODO = planned work, FIXME = bug/issue, HACK = temporary workaround).

```bash
# Scan all technical debt tags (example)
rg -n -i "(TODO|FIXME|HACK|XXX|BUG|WORKAROUND|TEMP|KLUDGE):?" --type-add 'code:*.{py,js,ts,jsx,tsx,go,java,rs,c,cpp,h,hpp,swift,kt}' -t code .

# Get blame details for a specific line range
git blame <filename> -L <start>,<end> --show-email 2>/dev/null | head -5
```

## Phase 2: Duplicate Code Detection

**BEFORE proceeding:**

1. **Scan for code duplication** using tools like `jscpd`, `pmd-cpd`, or `dupl`.
2. **Define threshold values** — target duplicate blocks of at least 10 lines with 80%+ similarity.
3. **Document source and target paths** for each duplicate block.
4. **Flag the duplicate** as a DRY (Don't Repeat Yourself) violation.

```bash
# Duplicate code scan using jscpd
npx jscpd . --min-lines 10 --min-tokens 50 --threshold 0.8 --output report.json

# Alternative lint check
pip install flake8 && flake8 --select=Q000 .  # basic check
```

## Phase 3: Complexity Analysis

**BEFORE proceeding:**

1. **Measure cyclomatic complexity** (McCabe complexity) for all functions/methods.
2. **Define threshold ranges** — 10+ = warning, 20+ = critical, 50+ = refactor mandatory.
3. **Rank complexity** — list the top 20 most complex functions.
4. **Identify long functions** — flag functions exceeding 50 lines of code.
5. **Locate deep nesting** — flag conditional or loop nestings exceeding 3 levels.

```bash
# For Python
python -m radon cc . -s --min C
python -m radon raw . --min C

# For JavaScript/TypeScript
npx complexity-report --threshold 10 src/

# For Java
find . -name "*.java" -exec wc -l {} \; | sort -rn | head -20
```

## Phase 4: Dependency Health Audits

**BEFORE proceeding:**

1. **Inventory all dependencies** (e.g., `package.json`, `requirements.txt`, `Cargo.toml`, `pom.xml`).
2. **Check for outdated versions** using commands like `npm outdated`, `pip list --outdated`, or `cargo update`.
3. **Scan for abandoned packages** (e.g., no updates in the past 2+ years).
4. **Audit for security vulnerabilities** using `npm audit`, `pip-audit`, `cargo audit`, or `snyk test`.
5. **Verify license compliance** — identify copyleft or restrictive licenses (e.g., GPL/AGPL).

```bash
# npm
npm outdated
npm audit --json

# Python
pip list --outdated --format=columns
pip-audit

# General check
npx npm-check --ignore@types/*
```

## Phase 5: Documentation Gaps

**BEFORE proceeding:**

1. **Find undocumented public APIs** — locate public functions, methods, or classes missing docstrings or doc comments.
2. **Identify undocumented modules** — list files or directories without high-level architectural explanations.
3. **Check core documents** — verify the presence of a root `README.md` and ensure API guides are up to date.
4. **Audit type coverage** — flag parameters or return values lacking type hints (e.g., in Python or TypeScript).

```python
# Python — Find undocumented public functions
python -c "
import ast, sys
with open('yourfile.py') as f:
    tree = ast.parse(f.read())
for node in ast.walk(tree):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        if not ast.get_docstring(node):
            print(f'{node.name} — missing documentation')
"

# TypeScript — Audit exported functions for JSDoc headers
rg "export (async )?(function|class|interface|type)" --type ts -A 2 | rg -B 2 "^export" | rg -B 2 -v "^/\*\*"
```

## Phase 6: Prioritization and Logging

**BEFORE proceeding:**

1. **Categorize by impact area:**
   - **Performance** — bottlenecks, slow queries, inefficient loops.
   - **Security** — vulnerabilities, outdated dependencies, missing validations.
   - **Maintainability** — code smells, high complexity, missing documentation.
   - **Testability** — coverage gaps, fragile or broken tests.
2. **Assign priority levels** — P0 (critical/immediate), P1 (high), P2 (medium), P3 (low).
3. **Update the tech debt register** — for each item, include: ID, description, file/location, category, priority, discovery date, owner, and current status.
4. **Compile the summary report** — outline key statistics, trends, and the top 5 critical debt items.

```bash
# Tech debt register format (CSV or Markdown table)
echo "| ID | Description | File | Category | Priority | Discovery Date | Owner | Status |" > debt-register.md
echo "|----|-------------|------|----------|----------|----------------|-------|--------|" >> debt-register.md
echo "| TD-001 | HACK: hardcoded DB credentials | config.py | Security | P0 | $(date +%Y-%m-%d) | - | Open |" >> debt-register.md
```

## Phase 7: Final Verification

Before marking complete:

- [ ] Have all TODO/FIXME/HACK/XXX tags been indexed?
- [ ] Are duplicate code blocks identified and logged?
- [ ] Is a list of functions with high cyclomatic complexity (cc > 10) documented?
- [ ] Have dependency updates, vulnerabilities, and licensing issues been analyzed?
- [ ] Are API documentation gaps cataloged?
- [ ] Has each item been assigned a category (performance, security, maintenance, test)?
- [ ] Has each item been assigned a priority (P0 to P3)?
- [ ] Is the tech debt register file updated and saved?
- [ ] Is a summary report prepared for stakeholders?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I already know where the issues are; running automated tools is unnecessary."
- "This HACK has been in the code for 2 years without issues, so we can ignore it."
- "Maintaining a tech debt log is a waste of time; I'll keep it in my head."
- "Let's only check new dependencies; older ones are fine."
- "Complexity metrics are academic and don't apply to real-world code."

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "You missed a TODO comment in this module." — Expand your search scope.
- "This should be P0 priority, not P2." — Re-evaluate prioritization metrics.
- "The register is missing columns like discovery date or ownership." — Complete the register structure.
- "Why isn't this outdated package listed in the report?" — Check your dependency auditing logs.
- "This report is too long; provide an executive summary." — Structure your output with a clear summary section.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "All codebases have technical debt, so there's no point in tracking it." | Unmonitored debt accrues interest in the form of bugs and friction. Tracking lets you pay it off systematically. |
| "Running analysis tools takes too long; I can scan files manually." | Automated linters and complexity analyzers complete in seconds, catching details human reviews miss. |
| "Prioritization is too subjective." | Clear category definitions and a P0-P3 scale establish objective guidelines. |
| "I'll fix this issue later today, so I won't write it down." | Tasks that are not logged are easily forgotten under next-day pressures. |
| "Writing down technical debt is just bureaucracy." | The tech debt register is the only way to justify refactoring tasks to business stakeholders. |

## Related Skills

- **release-manager** — Evaluate technical debt before releasing features to production.
- **code-reviewer** — Log code smells identified during reviews into the register.

## Self-Review

After completing this process:

1. **Coverage Check:** Have you analyzed all five areas (code smells, duplicates, complexity, dependencies, documentation)?
2. **Registry Completeness:** Are all mandatory columns populated in the register?
3. **Iron Law Audit:** Is every listed item mapped to a priority and category rather than relying on gut feeling?
