---
name: release-manager
description: "Release management, tagging, changelog generation, and package publishing. Use when cutting a release or automating the publish workflow."
---

# Release Manager

## Overview

This skill automates the release management process in software projects. It parses conventional commit messages to calculate semantic versions, generates changelogs, manages git tags, creates release branches, validates builds, and publishes packages to target repositories. The goal is to eliminate human error, ensuring every release is consistent, traceable, and reproducible.

**Core principle:** Every release must be documented, tagged, and validated. No manual release operation is trusted.

## The Iron Law

```
A RELEASE CAN NEVER BE EXECUTED MANUALLY. ALL TAGGING, CHANGELOG GENERATION, AND PUBLISHING OPERATIONS MUST BE AUTOMATED.
```

## When to Use

**Use this when:**
- A project is ready to tag and deploy a new release.
- The project follows conventional commit standards.
- Publishing to package managers like npm, PyPI, or GitHub Releases.
- Automated changelog updates are required.
- The version number needs updating (avoid manual updates; use this skill instead).

**Use this ESPECIALLY when:**
- Under time pressure, such as when hotfixing a production issue.
- Releasing multi-package repositories or microservices.
- Releasing during off-hours or weekends (when the risk of human error is highest).

**Don't skip when:**
- No new commits exist, or no changes have occurred since the last tag.
- The project has not yet reached a stable version (e.g., 0.x.x) — tagging is still required.

## Phase 1: Analyze Current Project State

**BEFORE proceeding:**

1. **Locate the last tag** — Identify the most recent git tag.
2. **Collect the commit log** — Retrieve conventional commit messages (e.g., `feat`, `fix`, `refactor`, breaking changes) since the last tag.
3. **Calculate the next semantic version** based on commit types:
   - `BREAKING CHANGE` or `!` → Major version bump.
   - `feat` → Minor version bump.
   - `fix`, `docs`, `refactor` → Patch version bump.
   - `chore`, `ci`, `test` → No version bump.
4. **Verify branch status** — Ensure the repository is checked out to the main release branch (e.g., `main`/`master`) and the working directory is clean.

```bash
# Locate the last tag
git describe --tags --abbrev=0 2>/dev/null || echo "0.0.0"

# Collect conventional commit messages
git log $(git describe --tags --abbrev=0 2>/dev/null || echo "HEAD")..HEAD --oneline --pretty=format:"%s"

# Check active branch and status
git rev-parse --abbrev-ref HEAD
git status --porcelain
```

## Phase 2: Calculate Version and Generate Changelog

**BEFORE proceeding:**

1. **Calculate the new version string** based on the Phase 1 analysis.
2. **Construct the changelog entry** — Group commits by type (e.g., Features, Bug Fixes, Breaking Changes, Documentation).
3. **Write the changelog** — Append the new entry to the top of `CHANGELOG.md`.
4. **Update package manifests** — Modify files containing the version string (e.g., `package.json`, `pyproject.toml`, `Cargo.toml`, `version.rb`).

```bash
# Example: Updating package.json version
npm version --no-git-tag-version <major|minor|patch>

# Example: Formatting a changelog entry
echo "## [v1.2.3] - $(date +%Y-%m-%d)" > CHANGELOG.tmp
echo "" >> CHANGELOG.tmp
cat changelog-section.md >> CHANGELOG.tmp
echo "" >> CHANGELOG.tmp
cat CHANGELOG.md >> CHANGELOG.tmp 2>/dev/null || true
mv CHANGELOG.tmp CHANGELOG.md
```

## Phase 3: Validate the Build

**BEFORE proceeding:**

1. **Run tests** (e.g., `npm test`, `pytest`, `cargo test`).
2. **Build the packages** (e.g., `npm run build`, `python -m build`, `cargo build`).
3. **Run linters and style checks** (e.g., `npm run lint`, `ruff check`, `cargo fmt --check`).
4. **Halt on any error** — Report the failure and cancel the release process.

```bash
npm run build && npm test
# or
python -m build && pytest
```

## Phase 4: Git Operations

**BEFORE proceeding:**

1. **Create the release branch** — `release/v{major}.{minor}.{patch}`.
2. **Commit version updates** — Group changelog and manifest updates into a single release commit.
3. **Create an annotated tag** — Add release notes to the tag message metadata.
4. **Push the branch and tags** to origin.
5. **Merge changes** — Merge the release branch back into the main branch (and develop branch if applicable).

```bash
git checkout -b release/v$NEW_VERSION
git add CHANGELOG.md package.json
git commit -m "chore(release): v$NEW_VERSION"
git tag -a v$NEW_VERSION -m "$RELEASE_NOTES"
git push origin release/v$NEW_VERSION
git push origin v$NEW_VERSION
```

## Phase 5: Publishing

**BEFORE proceeding:**

1. **Publish to package managers** (e.g., `npm publish`, `twine upload dist/*`).
2. **Create the GitHub Release** — Use the `gh` CLI to generate the release and attach notes.
3. **Verify the published package** — Check that the package is live and downloadable with the correct version.

```bash
# npm publish
npm publish

# GitHub Release creation
gh release create v$NEW_VERSION --title "v$NEW_VERSION" --notes "$RELEASE_NOTES"

# PyPI publish
twine upload dist/*
```

## Phase 6: Final Verification

Before marking complete:

- [ ] Is the next version number calculated accurately (major/minor/patch)?
- [ ] Is the changelog updated and correctly formatted?
- [ ] Have all unit and integration tests passed?
- [ ] Has the build completed successfully?
- [ ] Is the annotated tag pushed to the remote repository?
- [ ] Has the release branch been merged into the correct branches?
- [ ] Is the package published and verified on target package managers (e.g., via `npm view` or `pip show`)?
- [ ] Is the GitHub Release created and populated with release notes?
- [ ] Have all CI/CD workflows triggered by the push completed successfully?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I don't need to run the full release process for this hotfix; I'll tag it manually."
- "The commit history is messy, so I'll guess which version number to bump."
- "I'll update the changelog later; let's publish the package first."
- "Tests failed, but it's just a flaky local environment; publish anyway."
- "Publishing manually from my workstation is faster than setting up automation."

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Don't tag manually — use the automated release process."
- "Why wasn't the changelog updated?"
- "Did you run tests before publishing?"
- "This breaking change should have bumped the major version, not the patch."
- "Why wasn't the package version updated in the manifest?"

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "It's a tiny change, we don't need a tag." | Every production deployment must be traceable to a specific git reference. |
| "Setting up release automation takes too long." | Automation prevents human errors, ensuring releases are repeatable and safe. |
| "We are under time pressure; skip the checks." | Pressure is when human errors occur; following the process prevents regressions. |
| "We don't use conventional commits, so this skill won't work." | Manually categorize the commits to calculate the version bump, then update the changelog. |
| "The CI checks passed, so local tests are redundant." | Confirm that the final release branch state has been verified before pushing tags. |

## Related Skills

- **tech-debt-tracker** — Audit technical debt status before executing releases.
- **code-reviewer** — Verify that all commits in the release scope have been approved.

## Self-Review

After completing this process:

1. **Step Validation:** Have you executed every phase (analysis, version calculation, build verification, tagging, publishing)?
2. **SemVer Compliance:** Does the version bump match the semantic versioning standard relative to the change scope?
3. **Artifact Quality:** Is the changelog clean and easy for users to digest?

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
