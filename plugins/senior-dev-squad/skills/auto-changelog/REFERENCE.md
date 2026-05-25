# Auto Changelog — Reference

Detailed commit-type tables, breaking-change detection commands, categorization mappings, SemVer rules, git log scripts, CHANGELOG.md and release notes templates. Linked from [SKILL.md](SKILL.md).

---

## Phase 1: Commit History Analysis

**Determine the analysis range:**
- **First changelog:** The entire commit history (from initial commit to HEAD).
- **Subsequent changelogs:** Commits since the last tag (release).
- **Specific range:** Commits between two tags/SHAs.

**Conventional Commits type → version impact:**

| Type | Meaning | Version Bump |
|------|---------|-------------|
| `feat:` | New feature | Minor |
| `fix:` | Bug fix | Patch |
| `perf:` | Performance improvement | Patch |
| `chore:` | Maintenance, configuration | None |
| `docs:` | Documentation changes | None |
| `refactor:` | Code refactoring | None |
| `test:` | Test changes | None |
| `style:` | Code style changes | None |
| `ci:` | CI/CD changes | None |
| `build:` | Build system changes | None |

**Scope and breaking change syntax:**
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

---

## Phase 2: Breaking Change Detection

**Explicit breaking change detection** — Search for commits containing the `!` modifier:
- `feat!: remove deprecated endpoint`
- `fix(api)!: change response format`

**Implicit breaking change detection** — Changes not immediately obvious from the commit message alone:
- API endpoint changes (URLs, methods, parameters)
- Database schema changes (migrations, column deletions/type alterations)
- Dependency major version upgrades
- Configuration format changes
- Public API signature changes

**Prepare migration/resolution notes for each change:**
- What changed?
- How should it be migrated?
- From which version is it applicable?

```bash
# Find explicit breaking changes
git log --format="%s" $(git describe --tags --abbrev=0)..HEAD | grep "!:"

# Inspect diffs of relevant commits (implicit breaking changes)
git diff <COMMIT_SHA>~1 <COMMIT_SHA> --stat
```

---

## Phase 3: Change Categorization

**Category → commit type mapping:**

| Category | Commit Types |
|----------|-------------|
| Added | `feat:` |
| Fixed | `fix:`, `perf:` |
| Changed | `refactor:`, `style:` |
| Deprecated | (manually flagged) |
| Removed | (manually flagged) |
| Security | (manually flagged) |
| Infrastructure | `ci:`, `build:`, `chore:` |

- **Group by scope** — Subgroup by scope within each category.
- **If no scope is provided** — Use the commit title directly.
- **Order commits chronologically** within each category (newest on top).

```bash
# Group commits by category
echo "### Added"
git log --format="  - %s" $(git describe --tags --abbrev=0)..HEAD | grep "^  - feat"

echo "### Fixed"
git log --format="  - %s" $(git describe --tags --abbrev=0)..HEAD | grep "^  - fix\|^  - perf"

echo "### Changed"
git log --format="  - %s" $(git describe --tags --abbrev=0)..HEAD | grep "^  - refactor\|^  - style"
```

---

## Phase 4: Version Bump Recommendation

**SemVer calculation rules:**

| Condition | Bump | Example |
|-----------|------|---------|
| Contains `feat!:` or `fix!:` (breaking change) | Major (X.0.0) | v1.2.3 → v2.0.0 |
| Contains `feat:` (no breaking change) | Minor (0.X.0) | v1.2.3 → v1.3.0 |
| Contains only `fix:`, `perf:` | Patch (0.0.X) | v1.2.3 → v1.2.4 |
| Only `chore`, `docs`, `refactor`, `test`, `style`, `ci`, `build` | No Bump | v1.2.3 → v1.2.3 (no release required) |

**Read the current version from:**
- `package.json`, `Cargo.toml`, `pyproject.toml`, or `VERSION` file
- The most recent git tag

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

---

## Phase 5: CHANGELOG.md Generation

**Format rules (keepachangelog.com):**
- Reverse chronological order (newest release on top)
- Format each release header as `## [version] - YYYY-MM-DD`
- Use categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Maintain an `## [Unreleased]` section for changes not yet tagged
- Update comparison links at the bottom

**Write/Update the file:**
- If missing: Create a new CHANGELOG.md
- If present: Prepend the new release section to the top, update comparison links

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

---

## Phase 6: Release Notes Generation

**Language guidelines:**
- Avoid deep developer jargon — use customer-facing terms.
- "Users can now do X" — feature
- "Resolved issue where X occurred" — fix
- "X has changed, please use Y instead" — breaking change

**Order by importance:**
1. Breaking Changes (critical)
2. New Features
3. Bug Fixes
4. Performance Improvements
5. Other Changes

- Append PR/Issue links for traceability — `(#123)`
- Include a migration guide if there are breaking changes

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

---

## Self-Review

After completing this skill's process:

1. **Coverage check:** Have you scanned all commits? Are they accurately categorized?
2. **Edge case check:** How are merge commits, revert commits, and empty or invalid commit messages handled?
3. **Quality check:** Is the CHANGELOG.md clear? Is the recommended version bump accurate? Are breaking changes highlighted sufficiently?
