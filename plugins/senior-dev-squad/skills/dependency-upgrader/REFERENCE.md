# Dependency Upgrader — Reference

Extended command reference and configuration examples for the `dependency-upgrader` skill. No frontmatter — this file is not a skill, it is linked reference material.

---

## Audit Commands by Ecosystem

### Node / npm

```bash
npm outdated                        # shows current / wanted / latest
npm audit                           # CVE report against installed tree
npm audit fix                       # auto-fix patch/minor advisories (run cautiously)
npm audit fix --force               # includes majors — review diff before accepting
```

### Node / yarn (classic v1)

```bash
yarn outdated
yarn audit
```

### Node / yarn (berry v2+)

```bash
yarn upgrade-interactive            # interactive TUI for selective bumps
yarn npm audit
```

### Python / pip

```bash
pip list --outdated
pip-audit                           # install with: pip install pip-audit
safety check                        # alternative: pip install safety
```

### Python / poetry

```bash
poetry show --outdated
poetry update <package>             # respects version constraints in pyproject.toml
```

### Ruby / Bundler

```bash
bundle outdated
bundle audit check --update         # install with: gem install bundler-audit
```

### Rust / Cargo

```bash
cargo outdated                      # install with: cargo install cargo-outdated
cargo audit                         # install with: cargo install cargo-audit
```

### Go

```bash
go list -m -u all                   # shows available upgrades
govulncheck ./...                   # install with: go install golang.org/x/vuln/cmd/govulncheck@latest
```

---

## Per-Ecosystem Upgrade Commands

### npm

```bash
# Upgrade to wanted version (within semver range in package.json)
npm update <package>

# Upgrade to a specific version, including majors
npm install <package>@<version>

# Reinstall from lockfile (CI-safe, never upgrades)
npm ci
```

### yarn (classic v1)

```bash
yarn upgrade <package>
yarn upgrade <package>@<version>
```

### yarn (berry v2+)

```bash
yarn up <package>
yarn up <package>@<version>
```

### pip / requirements.txt

```bash
# 1. Edit the version pin in requirements.txt / pyproject.toml
# 2. Reinstall
pip install -r requirements.txt

# Or with pip-tools:
pip-compile --upgrade-package <package> requirements.in
pip-sync requirements.txt
```

### poetry

```bash
poetry add <package>@<version>      # updates pyproject.toml + poetry.lock
poetry install                      # reinstall from lock
```

### Bundler

```bash
bundle update <gem>                 # updates Gemfile.lock for this gem only
bundle update --patch               # conservative: patch bumps only across all gems
```

### Cargo

```bash
cargo update -p <crate>             # updates Cargo.lock for this crate within semver range
# For a major: edit Cargo.toml manually, then:
cargo build                         # regenerates Cargo.lock
cargo test
```

### Go

```bash
go get <module>@<version>           # updates go.mod + go.sum
go mod tidy                         # removes unused entries from go.sum
go test ./...
```

---

## Automation Starter Configs

### Renovate — `renovate.json`

```json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "minor"],
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "matchUpdateTypes": ["major"],
      "automerge": false,
      "labels": ["dependencies", "major"]
    }
  ],
  "prConcurrentLimit": 3,
  "schedule": ["before 9am on Monday"]
}
```

Key options:
- `automerge: true` on patch/minor means green CI auto-merges without a human click
- `prConcurrentLimit` prevents a flood of open PRs
- `schedule` batches PRs to a predictable window

### Dependabot — `.github/dependabot.yml`

```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 5
    labels:
      - "dependencies"

  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 3
```

Add one `updates` entry per ecosystem. Dependabot does not support automerge natively — pair with a GitHub Actions workflow that merges on green CI for patch/minor:

```yaml
# .github/workflows/auto-merge-deps.yml
name: Auto-merge Dependabot patch/minor
on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - uses: actions/checkout@v4
      - name: Fetch Dependabot metadata
        id: meta
        uses: dependabot/fetch-metadata@v2
      - name: Merge if patch or minor
        if: steps.meta.outputs.update-type == 'version-update:semver-patch' || steps.meta.outputs.update-type == 'version-update:semver-minor'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Pinning Transitive Dependencies

Use only as a last resort — for example, a transitive dependency has a CVE and the declaring package has not yet released a fix.

### npm overrides (npm 8+)

```json
// package.json
"overrides": {
  "vulnerable-transitive-dep": ">=2.3.1"
}
```

### yarn resolutions (classic v1)

```json
// package.json
"resolutions": {
  "vulnerable-transitive-dep": "2.3.1"
}
```

### poetry dependency overrides

```toml
# pyproject.toml
[tool.poetry.dependencies]
vulnerable-transitive-dep = ">=2.3.1"
```

Always add a comment documenting:
- Why the pin exists
- The CVE or issue link
- When to remove it (i.e., when the declaring package ships a fix)
