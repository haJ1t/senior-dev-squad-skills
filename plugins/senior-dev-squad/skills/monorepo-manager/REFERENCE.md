# Monorepo Manager — Reference

Deep configuration snippets for the [monorepo-manager](./SKILL.md) skill.
No frontmatter — this file is not a skill and is not auto-discovered by the marketplace.

---

## Root Workspace Manifests

### `package.json` (npm / yarn workspaces)

```json
{
  "name": "acme-monorepo",
  "private": true,
  "workspaces": ["apps/*", "packages/*", "tooling/*"],
  "scripts": {
    "build":   "turbo run build",
    "test":    "turbo run test",
    "lint":    "turbo run lint",
    "dev":     "turbo run dev --parallel",
    "release": "turbo run build --filter='...[origin/main]' && changeset publish"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "@changesets/cli": "^2.27.0"
  }
}
```

### `pnpm-workspace.yaml`

```yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tooling/*'
```

### Individual package `package.json`

```json
{
  "name": "@acme/ui",
  "version": "0.1.0",
  "private": false,
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js",
      "types": "./dist/index.d.ts"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format esm,cjs --dts",
    "dev":   "tsup src/index.ts --format esm,cjs --dts --watch",
    "lint":  "eslint src/",
    "test":  "vitest run"
  }
}
```

---

## Turborepo Pipeline (`turbo.json`)

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"],
      "cache": true
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["coverage/**"],
      "cache": true,
      "env": ["CI", "NODE_ENV"]
    },
    "lint": {
      "outputs": [],
      "cache": true
    },
    "type-check": {
      "dependsOn": ["^build"],
      "outputs": [],
      "cache": true
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

**Key rules:**
- `"dependsOn": ["^build"]` — `^` means "all upstream workspace dependencies must run `build` first."
- `"cache": true` requires `"outputs"` to be meaningful — Turborepo hashes outputs to decide cache hits.
- `dev` is a long-running watcher: always `"cache": false` + `"persistent": true`.

---

## Nx Pipeline (`nx.json`)

```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/dist"],
      "cache": true
    },
    "test": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/coverage"],
      "cache": true
    },
    "lint": {
      "cache": true
    },
    "type-check": {
      "dependsOn": ["^build"],
      "cache": true
    }
  },
  "defaultBase": "main"
}
```

---

## GitHub Actions — Affected CI (Turborepo)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0        # full history needed for affected calculation

      - uses: pnpm/action-setup@v3
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install --frozen-lockfile

      - name: Build, test, and lint affected packages
        run: pnpm turbo run build test lint --filter='...[origin/main]'
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM:  ${{ secrets.TURBO_TEAM }}
```

**`fetch-depth: 0`** is required — without full history, git cannot diff against `origin/main` and the filter falls back to building everything.

### Remote cache setup (one-time)

```bash
npx turbo login          # authenticate with Turborepo Cloud
npx turbo link           # link this repo to a Turborepo Cloud team
# → adds TURBO_TOKEN / TURBO_TEAM to .turbo/config.json (gitignored)
# Add TURBO_TOKEN and TURBO_TEAM to your CI environment secrets.
```

Self-hosted alternatives: [ducktape](https://github.com/ducktape-dev/ducktape), Depot remote cache, or any S3-compatible store with a custom `TURBO_API`.

---

## Package Boundary Enforcement

### `eslint-plugin-import` (framework-agnostic)

```js
// .eslintrc.js (root)
module.exports = {
  plugins: ['import'],
  rules: {
    // Ban: import { x } from '../../packages/ui/src/Button'
    // Allow: import { x } from '@acme/ui'
    'import/no-relative-packages': 'error',
  },
};
```

### Nx module boundary constraints

Tag each project in `project.json`:

```json
{
  "name": "web",
  "tags": ["scope:app", "type:feature"]
}
```

```json
{
  "name": "ui",
  "tags": ["scope:shared", "type:ui"]
}
```

Enforce in root `.eslintrc.js`:

```js
module.exports = {
  rules: {
    '@nx/enforce-module-boundaries': ['error', {
      enforceBuildableLibDependency: true,
      depConstraints: [
        {
          sourceTag: 'scope:app',
          onlyDependOnLibsWithTags: ['scope:shared', 'scope:app'],
        },
        {
          sourceTag: 'scope:shared',
          onlyDependOnLibsWithTags: ['scope:shared'],
        },
      ],
    }],
  },
};
```

### Phantom dependency detection

```bash
# List direct deps per package and spot anything not declared
pnpm ls --depth=0 --filter @acme/web

# Audit version mismatches across all packages
pnpm dlx syncpack list-mismatches

# Auto-fix mismatches (review the diff before committing)
pnpm dlx syncpack fix-mismatches
```

---

## Shared Tooling Config

### `tooling/typescript/base.json`

```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "target": "ES2022",
    "lib": ["ES2022"],
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "exclude": ["node_modules", "dist"]
}
```

### `tooling/typescript/package.json`

```json
{
  "name": "@acme/tsconfig",
  "version": "0.0.0",
  "private": true,
  "exports": {
    "./base.json": "./base.json",
    "./nextjs.json": "./nextjs.json",
    "./react-library.json": "./react-library.json"
  }
}
```

### Consuming package `tsconfig.json`

```json
{
  "extends": "@acme/tsconfig/base.json",
  "compilerOptions": {
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

### Shared ESLint base (`tooling/eslint/base.js`)

```js
module.exports = {
  extends: ['eslint:recommended'],
  plugins: ['import'],
  rules: {
    'import/no-relative-packages': 'error',
    'no-console': 'warn',
  },
  env: { node: true, es2022: true },
};
```

---

## Changesets Configuration

### `.changeset/config.json`

```json
{
  "$schema": "https://unpkg.com/@changesets/config@3.0.0/schema.json",
  "changelog": "@changesets/cli/changelog",
  "commit": false,
  "linked": [],
  "access": "restricted",
  "baseBranch": "main",
  "updateInternalDependencies": "patch",
  "ignore": []
}
```

- `"access": "public"` for open-source scoped packages on npm; `"restricted"` for private.
- `"updateInternalDependencies": "patch"` — when `@acme/ui` bumps, any `workspace:*` dep on it in other packages automatically gets a patch bump recorded.
- `"linked": []` — add package groups here if you want them to always version in lockstep.

### Release CI workflow

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [main]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: pnpm/action-setup@v3
        with:
          version: 9

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
          registry-url: 'https://registry.npmjs.org'

      - run: pnpm install --frozen-lockfile

      - name: Create Release PR or Publish
        uses: changesets/action@v1
        with:
          publish: pnpm changeset publish
          version: pnpm changeset version
          commit: "chore: version packages"
          title: "chore: version packages"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

The `changesets/action` opens a "Version Packages" PR automatically. Merging that PR triggers the publish.
