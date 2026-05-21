---
name: supply-chain-verifier
description: "Dependency security scanning, provenance verification, license compliance, package.json, requirements.txt, go.mod, Cargo.toml. Use when auditing supply-chain risk."
---

# Supply Chain Verifier

## Overview

This skill audits software supply chain security via dependency vulnerability scans, provenance verification, and licensing checks. It parses package manifests (e.g., `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, `Gemfile`, `pom.xml`) to discover known vulnerabilities (CVEs), verifies that package registries (npm, PyPI, crates.io) map to trusted repository source origins (GitHub, GitLab), audits nested transitive dependencies, and checks licenses (MIT, GPL, AGPL, Apache 2.0, BSD) for compliance. The goal is to answer: "Is this dependency secure and compliant across CVEs, provenance, and license types?"

**Core principle:** If there is no verified source origin, there is no trusted dependency. Every dependency is treated as untrusted until validated.

## The Iron Law

```
NO DEPENDENCY CAN BE MERGED OR DEPLOYED TO PRODUCTION WITHOUT UNDERGOING CVE SCANNING, PROVENANCE VALIDATION, AND LICENSE COMPLIANCE CHECKS.
```

Omitting any of these three checks leaves the system vulnerable to supply chain exploits.

## When to Use

**Use this when:**
- A new dependency is proposed in a pull request.
- Performing periodic, automated audits of a project's dependency tree.
- A new CVE is disclosed, and you must verify whether your projects are affected.
- Auditing dependency licenses prior to releases or compliance audits.
- Confirming that registry artifacts (npm/PyPI packages) match their declared source code repositories.
- Scanning transitive, nested dependencies for inherited vulnerabilities.

**Use this ESPECIALLY when:**
- A supply chain security incident is disclosed in the wild (e.g., SolarWinds, event-stream, ua-parser-js) — audit all projects immediately.
- A developer asserts "this is a popular package used by thousands, it is safe" — popularity does not guarantee security.
- Restrictive copyleft licenses (e.g., AGPL) risk leaking into commercial proprietary codebases.

**Don't skip when:**
- A project claims to have zero third-party dependencies — double check the lockfiles.
- The project has automated SBOM generators; execute anomaly scans on these outputs.

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

## Phase 5: Final Verification

Before marking complete:

- [ ] Have all package manifests been audited and dependency lists compiled?
- [ ] Has context analysis been executed for all Critical and High CVEs?
- [ ] Is provenance validated for all direct dependencies?
- [ ] Are packages audited for typosquatting, account takeovers, and impersonation?
- [ ] Are all direct and transitive licenses cataloged?
- [ ] Are restrictive copyleft licenses checked against project compliance guidelines?
- [ ] Are action steps defined for packages with undefined (UNKNOWN) licenses?
- [ ] Are dependency resolution overrides written for transitive CVEs?
- [ ] Are breaking change risks reviewed for all package updates?
- [ ] Is the final report structured for both developers and management?
- [ ] Is an SBOM generated in SPDX or CycloneDX format?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This is a popular package; it would have been flagged if it had a CVE." — **Popularity does not protect you. event-stream and ua-parser-js had millions of downloads when compromised.**
- "I only need to scan direct dependencies; transitive dependencies are out of scope." — **Most supply chain attacks target nested, transitive paths.**
- "Licenses are standard; there's no need to audit them." — **An unvetted AGPL dependency can require you to open source your proprietary project.**
- "This npm artifact matches the GitHub repository link; it is safe." — **Provenance validation requires verifying integrity hashes, not just metadata strings.**
- "We can't update this package because the breaking changes are too large." — **Running code with unmitigated high CVEs is a higher operational risk than refactoring code.**
- "The npm audit returned green, so the dependencies are secure." — **Audit tools only flag cataloged CVEs; they do not check for typosquatting, zero-days, or provenance anomalies.**

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Did you verify the provenance of this package?" — You skipped registry hash checks.
- "Are the transitive dependencies included in the scan?" — You audited only direct dependencies.
- "Will this AGPL license impact our commercial license model?" — You misclassified copyleft license risks.
- "What is the impact of this CVE? Are we importing the vulnerable class?" — You skipped context impact reviews.
- "The package name in your update plan has a typo." — Pay closer attention to package naming details.
- "Why is this dependency missing from your report?" — Your path configuration was incorrect during tool execution.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Popular libraries are secure by default." | Popular libraries are primary targets for account takeover and typosquatting attacks. |
| "Transitive dependencies are too deep to audit." | 70% of supply chain vulnerabilities enter via nested transitive libraries. Audits are mandatory. |
| "All open-source licenses are permissive." | A single copyleft or restrictive license introduces legal and IP liability risks. |
| "Registry packages are identical to their Git repositories." | Registry uploads can be modified to contain backdoor payloads. Always audit provenance. |
| "Updating dependencies takes too much sprint time." | Exploits for public CVEs are often weaponized within days. Patching must be prioritized. |
| "We don't need SBOMs; our dependency count is low." | SBOMs are standard compliance artifacts required during audits. |

## Related Skills

- **security-reviewer** — Audit how vulnerable code paths in flagged dependencies are executed in application code.
- **mitre-attack-mapper** — Map supply chain vulnerabilities to MITRE ATT&CK techniques (T1195 - Supply Chain Compromise).

## Self-Review

After completing this process:

1. **Tool Verification:** Have manifest files for all project languages been processed with appropriate security linters?
2. **Context Analysis:** Are context checks complete for all High and Critical findings?
3. **Integrity Validation:** Are hashes and source repositories validated for direct dependencies?
4. **License Compliance:** Is every dependency licensed under an approved category?
5. **SBOM Accuracy:** Is the SBOM output complete and valid?
6. **Iron Law Verification:** Has every dependency passed vulnerability scanning, provenance checks, and license verification?
