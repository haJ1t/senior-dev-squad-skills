---
name: dependency-upgrader
description: "Safely upgrades project dependencies: audit, changelog review, one-at-a-time bumps, tests green between each, lockfile pinning, rollback plan. Use when updating outdated or vulnerable packages."
---

# Dependency Upgrader

## Overview

Upgrading dependencies is not a bulk operation performed with a single command. It is a deliberate, sequenced process: audit current state, read the changelog, bump one dependency (or one safe group), verify tests are green, then move to the next. The lockfile is the source of truth. Every upgrade must leave the project in a provably working state before the next begins.

**Core principle:** ONE dependency (or one safe patch/minor group) at a time, tests green between each — majors always individually with a migration guide in hand.

## The Iron Law

```
NEVER BUMP A MAJOR WITHOUT READING ITS MIGRATION GUIDE.
NEVER UPGRADE MORE THAN ONE LOGICAL UNIT AT A TIME WITHOUT GREEN TESTS IN BETWEEN.
```

## When to Use

**Use this when:**
- `npm outdated`, `pip list --outdated`, `bundle outdated`, or `cargo outdated` reveals stale packages
- A security advisory (CVE, GitHub Dependabot alert, `npm audit`) flags a vulnerable version
- Onboarding to a codebase that has not been updated in months
- Automated PRs from Renovate or Dependabot are ready for review and merge

**Use this ESPECIALLY when:**
- A package has a known CVE and the fix is in a new major — reading the migration guide is non-negotiable
- Multiple majors are outstanding — the temptation to do them all at once is highest and the blast radius is worst
- CI has been red for a while — upgrading into a broken baseline hides new breakage

**Never skip when:**
- A PR description says "just bumped some deps" — surface area is unknown until you audit
- The project has no tests — that is a prerequisite problem; invoke `test-engineer` first, then return here

## Semver Risk Table

| Version bump | Expected risk | Approach |
|---|---|---|
| **Patch** (x.y.**Z**) | Low — bug fix, no API change | Safe to group same-package patch bumps; run tests once |
| **Minor** (x.**Y**.0) | Medium — new API surface, deprecations possible | Group same-package minor bumps cautiously; read changelog |
| **Major** (**X**.0.0) | High — breaking changes, API removals | Always individual; read migration guide before touching lockfile |

## Phase 1: Audit Current State

**Before touching any version number:**

1. **Capture the outdated inventory** — run the appropriate audit command for your ecosystem (see [REFERENCE.md](./REFERENCE.md) for full command list per ecosystem).

   ```bash
   npm outdated && npm audit          # Node / npm
   ```

2. **Categorise every outdated package** — open a scratch list:
   - Package name | current → wanted → latest | patch / minor / major | CVE? | priority

3. **Confirm the test baseline is green.** If CI is red before you start, stop. Fix existing failures first.

   ```bash
   npm test    # or: pytest / bundle exec rspec / cargo test / go test ./...
   ```

4. **Start from a clean branch and clean working tree.**

   ```bash
   git checkout -b deps/upgrade-$(date +%Y-%m-%d)
   ```

## Phase 2: Read Before You Bump

For every dependency on your list, before touching the version:

1. **Find the changelog** — check `CHANGELOG.md` in the repo, the GitHub Releases page, or the npm/PyPI release notes.
2. **For majors — read the migration guide fully.** Note every breaking change that affects your call-sites. No migration guide = treat as "unknown risk" and allocate extra test time.
3. **For minors — scan for deprecation notices.** Deprecated APIs become breaking in the next major.
4. **Assess blast radius** — count how many files import this package before touching it.

**Output:** annotated list with "safe to bump", "needs migration work", or "defer — too large" for each package.

## Phase 3: Upgrade One Unit at a Time

A "unit" is a single package at any bump level, or a group of patch-only bumps for unrelated packages when you are confident tests cover each.

**Never** bundle a major with anything else in one commit.

After each unit — if tests are green, commit immediately:

```bash
git add package.json package-lock.json    # or lockfile equivalent
git commit -m "deps: upgrade <package> <old> → <new>"
```

One commit per unit. Granular commits are your rollback path. See [REFERENCE.md](./REFERENCE.md) for per-ecosystem upgrade commands (npm, pip, Cargo, Go, Bundler).

## Phase 4: Handle Majors — Migration Work

1. Open the migration guide in a browser tab. Do not close it until the upgrade is committed.
2. Build a checklist from every breaking change that touches your call-sites.
3. Bump the version first, run tests, read the failure output — errors are your guide to what the guide missed.
4. Work through the checklist one pattern at a time; no unrelated refactors in this commit.
5. Run full suite plus type-check: `npm test && npx tsc --noEmit`
6. Commit migration code separately from the version bump when the diff is large.

## Phase 5: Lockfile and Pinning

- **Always commit the lockfile** (`package-lock.json`, `yarn.lock`, `Cargo.lock`, `poetry.lock`, `Gemfile.lock`).
- **Use `npm ci` / `yarn install --frozen-lockfile` in CI**, never `npm install` — the latter silently upgrades transitives and breaks reproducibility.
- **Do not manually edit the lockfile.** Let the package manager regenerate it.
- **Pin transitive dependencies via overrides only as a last resort**, and document the reason in a comment.

## Phase 6: Automate Going Forward

Configure Renovate or Dependabot to surface upgrades weekly on a schedule. Set majors to require human review; allow patch/minor to automerge on green CI. See [REFERENCE.md](./REFERENCE.md) for starter configs.

**Automation handles scheduling. You still own reviewing changelogs and merging majors.**

## Phase 7: Rollback Plan

1. **Git is the rollback.** One commit per dependency unit means `git revert <sha>` restores the exact lockfile.
2. **Test the rollback path on a major upgrade** before merging to main — check out the pre-upgrade commit, run `npm ci && npm test`, confirm green.
3. **For production incidents**, revert the relevant commit — do not create a new manual pin. Reverts are auditable and reversible.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll just run `npm update` and see what happens"
- "These are all patch bumps, no need to read anything"
- "I'll fix the failing tests after I finish all the upgrades"
- "The lockfile conflicts are annoying, I'll just delete it and reinstall"
- "This major shouldn't be a big deal — the library is small"
- "I'll do the changelog reading later"
- Upgrading 10+ packages in a single commit

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why are 40 packages changed in this PR?" — You bulk-upgraded instead of one unit at a time
- "Did you read the v5 migration guide?" — You bumped a major without reading it
- "Tests were already failing before this PR" — You did not confirm a green baseline in Phase 1
- "The lockfile shouldn't be deleted" — You nuked the lockfile instead of resolving conflicts properly
- "Roll this back, production is broken" — You had no granular rollback commits

**When you see these:** STOP. Return to Phase 1 and rebuild the upgrade plan.

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "It's just a patch, nothing can break" | Patches fix bugs that your code may depend on. Tests exist precisely for this. |
| "I'll update everything at once and deal with failures" | You lose the ability to attribute any failure to a specific package. Debugging becomes archaeology. |
| "The lockfile is autogenerated, no need to commit it" | Without a committed lockfile, `npm install` resolves differently on every machine and in every CI run. |
| "I don't need to read the changelog for a minor bump" | Minor bumps carry deprecations. Today's deprecation is next major's breakage. |
| "Renovate/Dependabot handles this automatically" | Automation handles scheduling. You still own reviewing changelogs and merging majors. |
| "There are no tests, so I can't verify anything" | That is a blocker, not an excuse. Add tests first or explicitly accept and document the unverified risk. |

## Related Skills

- **supply-chain-verifier** — use before and after upgrading to audit provenance, license compliance, and CVE exposure across the full dependency tree
- **test-engineer** — invoke first when the project lacks adequate test coverage; green tests are a prerequisite for safe upgrading
- **research-first** — use for unfamiliar majors where you need ecosystem context, alternatives, and community migration experience before committing
- **ship-readiness-checklist** — run after all upgrades are complete before merging to main or deploying
- **tech-debt-tracker** — use to record packages that are too risky to upgrade now so they don't silently accumulate further

## Verification

- [ ] `npm outdated` (or equivalent) re-run — remaining deferrals are intentional and documented
- [ ] `npm audit` (or equivalent) shows no new advisories introduced by this session
- [ ] Full test suite is green on the upgrade branch
- [ ] Type-check passes if applicable: `npx tsc --noEmit`
- [ ] Lockfile is committed and up to date
- [ ] Each dependency upgrade is in its own git commit with a clear message
- [ ] Every major bump has a corresponding migration checklist completed
- [ ] CI pipeline is green end-to-end
- [ ] Rollback path confirmed: `git log --oneline` shows granular, revertible commits
- [ ] Renovate or Dependabot configured (or explicitly deferred with a note)
- [ ] No unrelated refactors mixed into dependency upgrade commits
