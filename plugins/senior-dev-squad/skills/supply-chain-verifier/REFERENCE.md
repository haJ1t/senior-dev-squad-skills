# Supply Chain Verifier — Reference

Detailed phase procedures, commands, output schemas, and worked examples. Linked from [SKILL.md](SKILL.md).

---

## Phase 1: Dependency Inventory and CVE Scanning

**BEFORE proceeding:**

Confirm that package files (`package.json`, `requirements.txt`, `go.mod`, etc.) are up to date and situated in the project workspace directory.

1. **Locate package files:** `package.json`, `package-lock.json`, `yarn.lock`, `requirements.txt`, `Pipfile.lock`, `go.mod`, `go.sum`, `Cargo.toml`, `Cargo.lock`, `Gemfile`, `Gemfile.lock`, `pom.xml`, `build.gradle`.
2. **Execute vulnerability scans** using language-specific tools:
   - Node.js: `npm audit`, `yarn audit`, `snyk test`.
   - Python: `pip-audit`, `safety check`, `pipenv check`.
   - Go: `govulncheck`, `nancy`.
   - Rust: `cargo audit`.
   - Java: `mvn dependency-check:check`, `gradle audit`.
3. **Prioritize findings** based on CVSS severity scores (Critical > High > Medium > Low).
4. **Run context audits** on critical/high CVEs to see if the vulnerable functions are imported and executable.

```bash
# Node.js
npm audit --audit-level=high
# or
snyk test --all-projects --severity-threshold=high

# Python
pip-audit -r requirements.txt --desc

# Go
govulncheck ./...

# Rust
cargo audit --json > cargo-audit-report.json
```

```json
{
  "vulnerabilities": [
    {
      "package": "axios",
      "version": "0.21.1",
      "severity": "HIGH",
      "cve": "CVE-2021-3749",
      "cvss": 7.5,
      "fix_version": "0.21.2",
      "direct": true,
      "path": ["package.json"],
      "used_by": ["api/client.js:35"],
      "exploitable_in_current_context": true
    },
    {
      "package": "debug",
      "version": "2.6.9",
      "severity": "MEDIUM",
      "cve": "CVE-2017-16137",
      "cvss": 5.3,
      "fix_version": "3.1.0",
      "direct": false,
      "path": ["express", "body-parser", "debug"],
      "exploitable_in_current_context": false
    }
  ]
}
```

---

## Phase 2: Provenance Validation

**BEFORE proceeding:**

Ensure the inventory phase is complete, prioritizing direct dependencies.

1. **Locate source repositories** for each dependency:
   - npm: `npm view <package> repository.url`.
   - PyPI: Homepage/Source links on the PyPI package page.
   - crates.io: Repository parameter in the package metadata.
   - Go mod: Root module URL in `go.sum`.
2. **Compare registry packages** against declared repository states:
   - Check if release tags exist in the repository matching the registry version.
   - Compare package hash values.
   - Download the registry tarball (e.g., using `npm pack <package>@<version>`) and verify the integrity checksum.
3. **Scan for registry anomalies:**
   - Popular package name mapping to an empty or low-activity repository → **Typosquatting**.
   - Recent addition of a new maintainer followed by rapid version releases → **Account Takeover**.
   - Repository URL pointing to an unrelated or suspicious domain → **Impersonation**.
   - Very new package (< 30 days) with anomalous download spikes → **Astroturfing**.

```bash
# Verify npm repository source
npm view express repository.url
# -> https://github.com/expressjs/express

# Download and check package checksum
npm pack express@4.18.2
shasum -a 512 express-4.18.2.tgz
npm view express@4.18.2 dist.integrity  # Compare hashes

# Verify Python package homepage
pip show requests | grep Home-page
# -> https://github.com/psf/requests
```

```yaml
provenance_report:
  validated_packages:
    - express: "GitHub: expressjs/express — version v4.18.2 matches repository tag ✓"
    - requests: "GitHub: psf/requests — version v2.31.0 matches repository tag ✓"
  
  suspicious_packages:
    - package: "calender"  # Typo squatting check (calendar typo)
      npm_registry: "calender"
      repository: "github.com/typo-squatter/calender"
      commit_count: 3
      age_days: 12
      downloads: 150000
      risk: "HIGH — TypoSquatting: calender mimicking calendar"
      action: "Remove immediately and replace with correct calendar dependency"
    
    - package: "fast-csv-old"
      npm_registry: "fast-csv-old"
      repository: "github.com/unknown/fast-csv-old"
      issues:
        - "Repository has been deleted"
        - "Last update: 2 years ago"
        - "Maintainer changed 2 months ago"
      risk: "MEDIUM — Suspected account takeover"
      action: "Audit alternative libraries; transition to active fork"
```

---

## Phase 3: License Compliance Audit

**BEFORE proceeding:**

Ensure a comprehensive listing of all direct and transitive dependencies is available.

1. **Extract license identifiers:**
   - CLI commands: `npm licenses`, `pip-licenses`, `go-licenses`, `cargo license`.
   - Enforce audits on nested dependencies.
2. **Categorize dependency licenses:**
   - **Permissive** (Low Risk): MIT, Apache 2.0, BSD-2/3-Clause, Unlicense, ISC, CC0-1.0.
   - **Copyleft** (Medium Risk): GPL-2.0, GPL-3.0, LGPL-2.1/3.0, MPL-2.0.
   - **Restrictive** (High Risk): AGPL-3.0, SSPL, BUSL, Commons Clause.
   - **Unknown**: Undefined or proprietary licenses.
3. **Assess licensing compatibility:**
   - Proprietary commercial projects: Identify copyleft licenses (GPL/AGPL) and flags for replacement.
   - Open source projects: Ensure all source compliance terms are satisfied.
   - SaaS deployments: Verify AGPL license types due to "remote network interaction" clauses.
4. **Identify alternatives** for incompatible dependencies.

```bash
# npm license checker
npx license-checker --production --json | jq 'to_entries[] | {(.key): .value.licenses}'

# Python license listing
pip-licenses --format=json --with-system
```

```yaml
license_compliance_report:
  summary:
    total_dependencies: 247
    permissive: 201
    copyleft: 38
    restrictive: 5
    unknown: 3

  critical_findings:
    - package: "agpl-toolkit"
      version: "1.2.3"
      license: "AGPL-3.0"
      dependency_type: "transitive"
      path: ["main-pkg", "utils-lib", "agpl-toolkit"]
      risk: "CRITICAL — AGPL-3.0 is incompatible with proprietary commercial licensing"
      suggested_fix: "Replace agpl-toolkit with an MIT-licensed alternative or isolate usage behind service boundaries"
    
    - package: "old-gpl-lib"
      version: "0.9.0"
      license: "GPL-2.0-only"
      dependency_type: "direct"
      risk: "HIGH — GPL-2.0 code linking restrictions may impact proprietary packaging"
      suggested_fix: "Isolate GPL code execution to a separate runtime process or identify an Apache/MIT alternative"
      alternatives:
        - "new-mit-lib (MIT, v2.0)"
        - "permissive-lib (Apache-2.0, v1.5)"

  warnings:
    - package: "unknown-license-pkg"
      version: "0.0.5"
      license: "UNKNOWN"
      risk: "MEDIUM — Undefined license represents legal liability risk"
      action: "Review licensing information in the package directory manually; open an issue on the upstream repository"
```

---

## Phase 4: Transitive Dependency Auditing and Updates

**BEFORE proceeding:**

Ensure CVE scanning, provenance, and license compliance audits have been completed.

1. **Map the dependency tree:**
   - CLI commands: `npm ls --all`, `pipdeptree`, `go mod graph`, `cargo tree`.
   - Identify which direct dependencies pull in specific transitive dependencies.
2. **Audit nested transitive paths** for CVEs:
   - Nested packages are often outdated even if the parent package is current.
   - Flag deep CVE paths (3+ levels down).
3. **Formulate resolution steps:**
   - Non-breaking changes: Bump patch releases (`^1.2.3` -> `^1.2.4`).
   - Minor updates: Bump minor releases (`^1.2.3` -> `^1.3.0`) and run verification tests.
   - Major updates: Bump major releases (`^1.2.3` -> `^2.0.0`) and audit for breaking changes.
   - Dependency overrides: Enforce target version resolutions in the package manifest if the parent package is unmaintained.
4. **Assess update impact:**
   - Prune unused packages.
   - Verify test suite coverage post-update.
   - Review release logs for breaking changes.

```bash
# Inspect package tree paths
npm ls --all --depth=5
# or
yarn why <package-name>

# Python dependency tree
pipdeptree --warn silence | grep -E ".*==.*"

# Enforce override in npm package.json
{
  "overrides": {
    "express": "4.19.2",
    "minimatch": "3.1.2"
  }
}

# Enforce replace in go.mod
replace golang.org/x/net v0.0.0-202001... => golang.org/x/net v0.7.0
```

```yaml
dependency_updates:
  immediate_critical:
    - package: "axios"
      current: "0.21.1"
      target: "0.28.0"
      cve: "CVE-2021-3749"
      severity: "HIGH"
      breaking: false  # No breaking changes in minor update
      test_coverage: true
      changelog: "https://github.com/axios/axios/blob/main/CHANGELOG.md"
    
    - package: "minimatch"
      current: "3.0.4"
      target: "3.1.2"
      cve: "CVE-2022-3517"
      severity: "CRITICAL"
      breaking: false
      note: "Patch version update containing no API modifications"

  recommended:
    - package: "express"
      current: "4.17.1"
      target: "4.19.2"
      reason: "4 minor versions behind; resolves outstanding security vulnerabilities"
      breaking_review_required: true
  
  monitored:
    - package: "lodash"
      current: "4.17.21"
      target: "5.0.0"
      reason: "Major release update; ESM transition introduces breaking changes"
      breaking: true
      postpone: true
      alternative: "Transition to lodash-es or replace with native JS functions"
```
