---
name: auto-changelog
description: "Commit analysis, change categorization, breaking change detection, semver recommendation, CHANGELOG.md. Use when generating or updating a project changelog."
---

# Auto Changelog

## Overview

Generates CHANGELOG.md automatically from commit history. It categorizes changes using the Conventional Commits standard (`feat:`, `fix:`, `chore:`, `docs:`, etc.), detects breaking changes, recommends semantic versioning (SemVer) increments, and produces human-readable changelogs in the keepachangelog.com format.

**Core principle:** THE CHANGELOG IS AS IMPORTANT AS THE CODE. What each release changes must be clear, traceable, and meaningful to the user.

## The Iron Law

```
THE CHANGELOG MUST BE UPDATED BEFORE EVERY RELEASE. AUTOMATED CHANGELOGS ARE ALWAYS MORE RELIABLE THAN MANUAL ONES.
```

## When to Use

**Use this when:**
- You need to generate a changelog before a release.
- Commit history is written in the Conventional Commits format.
- You want to automatically determine the next version number (major/minor/patch).
- You need to prepare release notes for users.

**Use this ESPECIALLY when:**
- You are working in a fast-paced release cycle (daily/weekly releases).
- You want to generate changelogs automatically within a CI pipeline.
- There is a high risk of missing breaking changes.

**Don't skip when:**
- "There is only one commit" — changelogs apply to projects of all sizes.
- "Commit messages are messy" — analyze messy commits and extract a structured changelog regardless.

## Phase 1: Commit History Analysis

**BEFORE proceeding:**

1. **Determine the analysis range:**
   - **First changelog:** The entire commit history (from initial commit to HEAD).
   - **Subsequent changelogs:** Commits since the last tag (release).
   - **Specific range:** Commits between two tags/SHAs.
2. **Parse commits based on Conventional Commits:**
   - `feat:` — New feature (minor version bump)
   - `fix:` — Bug fix (patch version bump)
   - `chore:` — Maintenance, configuration (no version bump)
   - `docs:` — Documentation changes (no version bump)
   - `refactor:` — Code refactoring (no version bump)
   - `test:` — Test changes (no version bump)
   - `style:` — Code style changes (no version bump)
   - `perf:` — Performance improvement (patch version bump)
   - `ci:` — CI/CD changes (no version bump)
   - `build:` — Build system changes (no version bump)
3. **Extract scope and breaking change metadata:**
   - `feat(api):` → scope = "api"
   - `feat!:` → breaking change (major version bump)
   - `feat(api)!:` → scope + breaking change

```bash
# List commits since the last tag
git log $(git describe --tags --abbrev=0)..HEAD --oneline --no-decorate

# Complete commit history (for initial changelog)
git log --reverse --oneline --no-decorate

# Parse conventional commits
git log --format="%s" $(git describe --tags --abbrev=0)..HEAD | grep -E "^(feat|fix|chore|docs|refactor|test|style|perf|ci|build)(\([a-z]+\))?!?:"
```

## Phase 2: Breaking Change Detection

**BEFORE proceeding:**

1. **Explicit breaking change detection:** Search for commits containing the `!` modifier:
   - `feat!: remove deprecated endpoint`
   - `fix(api)!: change response format`
2. **Implicit breaking change detection** — Changes not immediately obvious from the commit message alone:
   - API endpoint changes (URLs, methods, parameters)
   - Database schema changes (migrations, column deletions/type alterations)
   - Dependency major version upgrades
   - Configuration format changes
   - Public API signature changes
3. **Prepare migration/resolution notes for each change:**
   - What changed?
   - How should it be migrated?
   - From which version is it applicable?

```bash
# Find explicit breaking changes
git log --format="%s" $(git describe --tags --abbrev=0)..HEAD | grep "!:" 

# Inspect diffs of relevant commits (implicit breaking changes)
git diff <COMMIT_SHA>~1 <COMMIT_SHA> --stat
```

## Phase 3: Change Categorization

**BEFORE proceeding:**

1. **Sort commits into categories:**
   - **Added:** New features (`feat:`)
   - **Fixed:** Bug fixes (`fix:`, `perf:`)
   - **Changed:** Changes to existing features (`refactor:`, `style:`)
   - **Deprecated:** Features to be removed in future releases
   - **Removed:** Deprecated features removed in this release
   - **Security:** Security patches and fixes
   - **Infrastructure:** CI/CD, build, and dependency changes
2. **Group by scope** — Subgroup by scope within each category.
3. **If no scope is provided** — Use the commit title directly.
4. **Order commits chronologically** within each category (newest on top).

```bash
# Group commits by category
echo "### Added"
git log --format="  - %s" $(git describe --tags --abbrev=0)..HEAD | grep "^  - feat"

echo "### Fixed"
git log --format="  - %s" $(git describe --tags --abbrev=0)..HEAD | grep "^  - fix\|^  - perf"

echo "### Changed"
git log --format="  - %s" $(git describe --tags --abbrev=0)..HEAD | grep "^  - refactor\|^  - style"
```

## Phase 4: Version Bump Recommendation

**BEFORE proceeding:**

1. **SemVer calculation rules:**
   - **Major (X.0.0):** Contains breaking changes → `feat!:` or `fix!:`
   - **Minor (0.X.0):** Contains new features → `feat:`
   - **Patch (0.0.X):** Contains only fixes/performance improvements → `fix:`, `perf:`
   - **No Bump:** Contains only chore, docs, refactor, test, style, ci, build
2. **Read the current version:**
   - package.json, Cargo.toml, pyproject.toml, or VERSION file
   - The most recent git tag
3. **Calculate and recommend the new version:**
   - Current: v1.2.3 → feat exists → v1.3.0
   - Current: v1.2.3 → fix + breaking change exists → v2.0.0
   - Current: v1.2.3 → docs only → v1.2.3 (no release required)

```bash
# Find the current version tag
git describe --tags --abbrev=0

# Read from package.json (if applicable)
grep '"version"' package.json | head -1

# Calculate SemVer
# Major bump: git log --format="%s" <TAG>..HEAD | grep -q "!:"
# Minor bump: git log --format="%s" <TAG>..HEAD | grep -q "^feat"
# Patch bump: git log --format="%s" <TAG>..HEAD | grep -q "^fix\|^perf"
```

## Phase 5: CHANGELOG.md Generation

**BEFORE proceeding:**

1. **Use the keepachangelog.com format:**
   - Reverse chronological order (newest release on top)
   - Format each release header as `## [version] - YYYY-MM-DD`
   - Use categories: Added, Changed, Deprecated, Removed, Fixed, Security
   - Follow link formats: `[version]: https://github.com/owner/repo/releases/tag/v1.0.0`
2. **Maintain an Unreleased section:**
   - `## [Unreleased]` — changes not yet deployed to a tag
   - Everything slated for the next release goes here
3. **Write/Update the file:**
   - If missing: Create a new CHANGELOG.md
   - If present: Prepend the new release section to the top
   - Update comparison links at the bottom

```bash
# CHANGELOG.md Format Template
cat << 'CHANGELOG'
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- ...

### Fixed
- ...

## [1.2.0] - 2026-05-15

### Added
- feat(api): user deletion endpoint
- feat(cli): batch processing support

### Fixed
- fix(api): resolved null pointer error
- perf(core): optimized caching layer

[Unreleased]: https://github.com/owner/repo/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/owner/repo/releases/tag/v1.2.0
CHANGELOG
```

## Phase 6: Release Notes Generation

**BEFORE proceeding:**

1. **Use user-oriented language:**
   - Avoid deep developer jargon, use customer-facing terms.
   - "Users can now do X" — feature
   - "Resolved issue where X occurred" — fix
   - "X has changed, please use Y instead" — breaking change
2. **Order by importance:**
   - Breaking Changes (critical)
   - New Features
   - Bug Fixes
   - Performance Improvements
   - Other Changes
3. **Append PR/Issue links for traceability** — `(#123)`
4. **Include a migration guide** — if there are breaking changes.

```bash
# Generate release notes
cat << 'RELEASE'
## v1.2.0 Release Notes

🚀 **New Features**
- Added user deletion endpoint — you can now remove users directly from the administration dashboard (#42)
- Added batch processing CLI command (#45)

🐛 **Bug Fixes**
- Fixed null pointer error — resolved application crash during user profile load (#44)

⚡ **Performance**
- Caching layer improvements — API response latency reduced by 30% (#46)

⚠️ **Breaking Changes**
- **None**

---

[Full Changelog](CHANGELOG.md)
RELEASE
```

## Phase 7: Final Verification

Before marking complete:

- [ ] All commits have been successfully parsed according to the Conventional Commits specification.
- [ ] Commits are categorized accurately (Added/Fixed/Changed/Removed etc.).
- [ ] Breaking changes have been detected and migration paths documented.
- [ ] Changes are grouped by scope.
- [ ] Version bump recommendation is correctly calculated (major/minor/patch).
- [ ] CHANGELOG.md is correctly structured using keepachangelog.com guidelines.
- [ ] Release notes are user-friendly and clear.
- [ ] Comparison links at the bottom are accurate and active.
- [ ] Dates match the YYYY-MM-DD format.
- [ ] CHANGELOG.md changes have been written to the target file.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Commit messages are obvious enough, no need to parse them" — Always parse systematically, manual parsing misses edge cases.
- "It only contains fixes, so a patch bump is fine" — Breaking changes can be implicit, check the file diff.
- "I will write the changelog manually" — Automated changelogs are more accurate and comprehensive.
- "Scope information isn't important" — Scope is the key element that makes changelogs readable.
- "Release notes aren't necessary, the changelog is enough" — Release notes are for users, changelogs are for developers.

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "You missed a breaking change" — Phase 2 was skipped, perform an implicit breaking change check.
- "This commit is a fix, not a feature" — Parsing error occurred, check conventional commit typing regex.
- "The changelog format is wrong, not proper markdown" — keepachangelog.com format was violated, return to Phase 5.
- "Version recommendation is wrong, should be major instead of minor" — A breaking change was missed, return to Phase 2 and Phase 4.
- "Incorrect date format" — Use ISO 8601 format (YYYY-MM-DD), return to Phase 5.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Commit messages are messy and not in conventional commits format" | They can still be categorized using regex and pattern matching; some structure is better than none. |
| "There are no breaking changes, only fixes" | Unintentional changes can still cause breaking outcomes — audit the diffs. |
| "Creating a CHANGELOG.md is a waste of time" | A clean changelog is crucial for user adoption and confidence — it is a high-value time investment. |
| "I'll bump the version manually" | Manual versioning leads to inconsistency and is highly prone to human error. |
| "Release notes are only for major releases" | Every release (even patch releases) deserves notes — users want to know what changed. |

## Output Schema (MANDATORY)

Structure your response with:
1. **Analysis** — What you found/designed
2. **Concrete output** — Code, YAML, tables (not just descriptions)
3. **Tradeoffs/risks** — What you chose and why, what could go wrong
4. **Verification** — How to confirm correctness

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague recommendations | Not actionable | Concrete examples, specific steps |
| Missing tradeoffs | One-sided analysis | Every choice: "X over Y because..." |
| "Consider doing X" | No commitment | "Do X. Why: [reason]" |
| No verification criteria | Can't confirm quality | "Verify by: [test/check]" |
| Generic response | Not tailored | Domain-specific vocabulary, exact tool names |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Specificity | Generic advice | Some specifics | Concrete, actionable output |
| Tradeoff awareness | None | Mentioned | Documented with alternatives |
| Output format | Free text | Partial structure | Structured, scannable |
| Verification | None | Vague | Specific test/criteria |
| Domain accuracy | Wrong terms | Mostly correct | Precise domain vocabulary |

**Pass: 7/10**

## Related Skills

- **devops-release-engineer** — Automates changelogs and release steps in the CI pipeline.
- **pr-babysitter** — Triggers changelog updates post-PR merges.
- **ship-readiness-checklist** — Evaluates release-readiness metrics.
- **code-reviewer** — Reviews commit messages for conventional standard compliance.

## Self-Review

After completing this skill's process:

1. **Coverage check:** Have you scanned all commits? Are they accurately categorized?
2. **Edge case check:** How are merge commits, revert commits, and empty or invalid commit messages handled?
3. **Quality check:** Is the CHANGELOG.md clear? Is the recommended version bump accurate? Are breaking changes highlighted sufficiently?
