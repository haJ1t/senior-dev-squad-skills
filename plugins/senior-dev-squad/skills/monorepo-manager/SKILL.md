---
name: monorepo-manager
description: "Structures and operates monorepos with explicit package boundaries, affected-only CI builds, and shared tooling. Use when setting up a monorepo, enforcing workspace boundaries, wiring Turborepo/Nx pipelines, or deciding polyrepo vs. monorepo."
---

# Monorepo Manager

## Overview

A monorepo is not just "all code in one repo." It is a disciplined system of explicit package boundaries, a build graph that runs only what changed, shared tooling that never drifts, and a release process that stays coherent as the codebase grows. Without that discipline, a monorepo degenerates into a big-ball-of-mud repo that rebuilds the world on every commit, blurs ownership, and makes phantom-dependency bugs inevitable.

This skill covers the full lifecycle: deciding whether a monorepo is right, laying out the workspace, wiring Turborepo/Nx with remote caching, enforcing package boundaries in CI, and shipping releases with Changesets. Deep configuration snippets live in [REFERENCE.md](./REFERENCE.md).

**Core principle:** Run only what changed. Enforce explicit package boundaries. Never let CI rebuild the world.

## The Iron Law

```
NEVER IMPORT ACROSS PACKAGE BOUNDARIES WITHOUT AN EXPLICIT DECLARED DEPENDENCY.
NEVER RUN A TASK FOR A PACKAGE THAT HAS NOT CHANGED OR DOES NOT DEPEND ON WHAT CHANGED.
CI THAT REBUILDS THE WORLD ON EVERY COMMIT IS BROKEN CI — FIX THE PIPELINE, NOT THE PATIENCE.
```

## When to Use

**Use this when:**
- Setting up a new monorepo from scratch (workspace layout, tooling, pipeline)
- An existing monorepo has slow CI because it rebuilds every package on every PR
- Cross-package imports use relative `../../` deep paths instead of package names
- A new package, app, or shared library needs to be added to an existing workspace
- Phantom dependencies are causing intermittent failures
- The team is deciding between monorepo and polyrepo for a new product family
- Changesets or versioning is broken or not wired up

**Use this ESPECIALLY when:**
- Someone says "it's fine, just run the full build — it's only 8 minutes" (it will be 20 in six months)
- A PR touching `packages/ui` triggers full rebuilds of 12 apps that did not change
- A developer writes `import { db } from '../../../packages/database/src/client'` instead of `import { db } from '@acme/database'`

**Never skip when:**
- Adding a new shared package — boundaries and dependency declarations must be set up from day one
- CI is "too slow to fix right now" — affected-graph wiring pays back in the first week

## Polyrepo vs. Monorepo Tradeoff

Decide before you build. The monorepo pays when packages are genuinely coupled; it costs when they are not.

| Factor | Favour Monorepo | Favour Polyrepo |
|---|---|---|
| Code sharing | Multiple packages share types, utils, or UI | Packages are fully independent |
| Atomic changes | A single PR must touch app + library + types | Changes rarely cross package lines |
| Team topology | One team or tightly collaborating teams | Separate teams, independent release cadences |
| Tooling overhead | Team can invest in Turborepo/Nx config | Team wants zero orchestration overhead |
| Dependency drift | Shared deps must stay in sync (React, TS) | Each package pins its own versions safely |
| Versioning | Coordinated releases (Changesets) are a feature | Independent semver is a hard requirement |

**Rule of thumb:** if two packages are changed together more than 30% of the time, they belong in the same repo.

## Phase 1: Workspace Layout

```
<root>/
  apps/           # deployable applications (Next.js, Express, workers)
  packages/       # shared libraries consumed by apps or other packages
  tooling/        # shared dev config (tsconfig, eslint, prettier)
  .changeset/     # Changesets configuration
  turbo.json      # Turborepo pipeline (or nx.json for Nx)
  package.json    # root workspace manifest
```

Each package gets an explicit `"name": "@acme/package-name"` in its own `package.json`. Cross-package dependencies reference that name with `"workspace:*"` — never a relative path. See [REFERENCE.md](./REFERENCE.md) for full manifests.

## Phase 2: Task Orchestration Pipeline

Wire Turborepo or Nx so tasks execute in dependency order and are cached by default.

**Critical Turborepo rules:**
- `"dependsOn": ["^build"]` — build all upstream packages first (this is the build graph)
- `"cache": true` with non-empty `"outputs"` — enables local and remote caching
- `dev` must be `"cache": false` and `"persistent": true` — it is a watcher, not a task

**Critical Nx rules:**
- `targetDefaults.build.dependsOn: ["^build"]` — same graph semantics
- `defaultBase: "main"` — sets the comparison branch for `nx affected`

Full `turbo.json` and `nx.json` configs with all pipeline keys are in [REFERENCE.md](./REFERENCE.md).

## Phase 3: Affected-Graph CI

Only build and test packages that changed or that depend on what changed.

```bash
# Turborepo — run build + test + lint only for changed packages and their dependents
turbo run build test lint --filter='...[origin/main]'

# Nx equivalent
npx nx affected --target=build --base=origin/main --head=HEAD
npx nx affected --target=test  --base=origin/main --head=HEAD
```

The `--filter='...[origin/main]'` flag means: every package that changed relative to `origin/main`, plus every package that depends on those (the `...` prefix = dependents).

**Remote caching** makes every CI run after the first one near-instant for unchanged packages. Set `TURBO_TOKEN` and `TURBO_TEAM` as CI secrets and run `turbo login && turbo link` once. Full GitHub Actions workflow in [REFERENCE.md](./REFERENCE.md).

## Phase 4: Package Boundary Enforcement

Declare every cross-package dependency explicitly. Deep relative imports across packages are banned.

```json
// apps/web/package.json
{
  "dependencies": {
    "@acme/ui":     "workspace:*",
    "@acme/config": "workspace:*"
  }
}
```

Enforce the boundary with a lint rule in CI:

```js
// .eslintrc.js
{ rules: { 'import/no-relative-packages': 'error' } }
```

For Nx, use `@nx/enforce-module-boundaries` with tag-based constraints. Run `pnpm dlx syncpack list-mismatches` to catch phantom dependency version drift. Full ESLint and Nx configs in [REFERENCE.md](./REFERENCE.md).

## Phase 5: Shared Tooling Config

Keep TypeScript, ESLint, and Prettier config in `tooling/`. Each package extends; it never duplicates.

```json
// packages/web/tsconfig.json
{ "extends": "@acme/tsconfig/base.json", "compilerOptions": { "outDir": "dist" } }
```

Publish `tooling/typescript` as `@acme/tsconfig` so the `extends` path resolves cleanly inside the workspace. Full base config in [REFERENCE.md](./REFERENCE.md).

## Phase 6: Versioning and Release

```bash
# Developer: add a changeset with every PR that touches a published package
pnpm changeset

# CI on main: bump versions + update CHANGELOG.md
pnpm changeset version

# CI on main: publish changed packages
pnpm changeset publish
```

Set `"updateInternalDependencies": "patch"` in `.changeset/config.json` so internal `workspace:*` deps stay consistent when a shared package bumps. Full config in [REFERENCE.md](./REFERENCE.md).

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "Let me just use a relative `../../../` import for now and fix it later"
- "The full build only takes 8 minutes — affected filtering is not worth wiring up"
- "I'll put this util in `apps/web/src/lib/` instead of a proper package — it's only used there for now"
- "No need to declare the dep in `package.json` — it hoists from root anyway"
- "We can do Changesets later — we'll just bump versions manually for now"
- CI always rebuilds every package regardless of what changed

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|---|---|
| "Hoisting means I don't need to declare the dep" | Hoisting is non-deterministic. Phantom deps cause silent runtime failures in CI or after lockfile updates. |
| "Relative imports across packages are fine" | They bypass the build graph, break caching, and make refactors untraceable. One ESLint rule prevents this permanently. |
| "Affected CI is complex to set up" | It is one flag in a `turbo run` call. Not setting it up means paying full rebuild costs forever. |
| "We'll add Changesets when we need to publish" | By then there is no changelog, no semver history, and a tangle of manual bumps to untangle. |
| "Remote caching costs money" | Turborepo Cloud has a free tier. The cost of rebuilding everything on every PR is engineers waiting. |
| "This utility is too small for its own package" | Small packages are cheap. Shared logic buried in an app becomes a boundary-violation magnet. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why is CI rebuilding everything again?" — Affected filtering is not wired or the filter pattern is wrong
- "I imported from `packages/ui/src/` directly, is that OK?" — Boundary lint rule is not running in CI
- "The versions in these packages are out of sync" — Changesets is not being used; someone is bumping by hand
- "Package X uses React 17 but Y uses React 18 and they clash" — Shared deps are not pinned at root; run `syncpack list-mismatches`
- "It takes forever to install deps in CI" — Hoisting config (`shamefully-hoist`) is leaking; check `pnpm-workspace.yaml`

**When you see these:** STOP. Return to the relevant phase.

## Related Skills

- **devops-release-engineer** — use alongside for full CI/CD pipeline wiring, environment promotion, and deployment beyond build/test
- **auto-changelog** — use to automate CHANGELOG generation from Changesets entries on every release
- **architecture-planner** — use before committing to a monorepo topology; maps ownership and package responsibility
- **tech-debt-tracker** — use to surface and prioritise boundary violations and phantom deps accumulating in the repo
- **dependency-upgrader** — use to keep shared deps in sync across packages without manual version bumping

## Verification

- [ ] Workspace manifest lists all glob patterns (`apps/*`, `packages/*`, `tooling/*`)
- [ ] Every shared package has a declared `name` in the `@scope/name` convention
- [ ] Cross-package dependencies use `workspace:*` — no relative paths in `dependencies`
- [ ] `turbo.json` or `nx.json` pipeline defines `dependsOn: ["^build"]` for `build` and `test`
- [ ] At least one task is `"cache": true` with non-empty `outputs`
- [ ] CI uses `--filter='...[origin/main]'` (Turborepo) or `nx affected` — not a full `turbo run build`
- [ ] Remote cache credentials are set as CI secrets and `turbo link` has been run
- [ ] `import/no-relative-packages` or `@nx/enforce-module-boundaries` is active and runs in CI lint step
- [ ] `syncpack list-mismatches` returns no unintentional mismatches
- [ ] `.changeset/config.json` exists and at least one developer has used `pnpm changeset`
- [ ] Phantom-dep check (`pnpm ls --depth=0` per package) is clean
- [ ] Polyrepo-vs-monorepo tradeoff was evaluated explicitly before setup
