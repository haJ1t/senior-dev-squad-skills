# Research First — Reference

Detailed phase-by-phase steps, commands, templates, and examples. Linked from [SKILL.md](SKILL.md).

---

## Phase 1: Context Compilation

**Understand the existing codebase and project structure before writing code.**

1. **Scan the Codebase** — Examine the project's directory structure, existing files, and patterns used.
   - Map out the project using tools like `search_files(target='files', pattern='*.py', path='.')`.
   - List the existing modules, services, and components.

2. **Recognize Existing Patterns** — What architectural patterns are used in the project?
   - MVC, Clean Architecture, Feature-based, Monolith, Microservices?
   - What style and rules exist in the current codebase?

3. **Find Related Files** — Identify all files relevant to the change you will make.
   - Detect dependencies, import chains, and shared types.
   - Identify all modules that will be affected by the change.

4. **Read Configuration Files** — `package.json`, `Cargo.toml`, `pyproject.toml`, `Gemfile`, etc.
   - Note the existing dependencies and their versions.

```
# Example scan queries:
search_files(target='files', pattern='*.py', path='/project_path')
search_files(target='files', pattern='*config*', path='/project_path')
search_files(target='content', pattern='from\\s+', file_glob='*.py', path='/project_path')
```

**Output:** Project context map — technologies used, architectural patterns, and a list of related files.

---

## Phase 2: Web Research

**Learn the current status of the libraries, frameworks, and tools you plan to use.**

1. **Check the Latest Versions** — Check the official release page for every dependency.
   - npm: `npm view <package> version`
   - PyPI: `pip index versions <package>` or the PyPI website
   - Crates.io, RubyGems, Maven Central, etc.
   - GitHub releases page

2. **Search for Best Practices** — Find the current best practices for the technology you will use.
   - Search queries like "best practices 2025/2026"
   - The "best practices" section of the official documentation
   - Patterns widely accepted by the community

3. **Explore Alternative Libraries** — Find other options that solve the same problem.
   - Comparison articles, "vs" pages
   - GitHub star count, maintenance status, community size

```
# Example version check commands:
npm view react version
pip index versions fastapi
cargo search serde
```

**Output:** Verified information for each dependency — current version, latest stable version, and a list of current best practices.

---

## Phase 3: Documentation Review

**Read the official documentation of the frameworks/libraries you will use.**

1. **Scan Official Documentation** — Read "getting started", "installation", and "migration guide" sections.
   - Verify installation steps.
   - Check for critical breaking changes.
   - Review migration guides.

2. **Check the API Reference** — Verify the signatures of the functions/classes you will use.
   - Parameter types, return types
   - Deprecated warnings
   - Newly added features

3. **Analyze Example Code** — Ensure the examples in the documentation are up to date.
   - Check version notes used in the examples.
   - Distinguish legacy version examples.

```
# Documentation lookup examples:
# Official site: docs.example.com
# GitHub README: github.com/example/project#readme
# Migration guide: docs.example.com/migration/v2-to-v3
```

**Output:** Verified signatures of the APIs to be used, migration notes, deprecated warnings, and sample code snippets.

---

## Phase 4: Solution Discovery

**Search for existing open-source solutions before writing code from scratch.**

1. **Scan Open Source Alternatives** — Search GitHub, GitLab, and awesome-lists.
   - Query: `site:github.com <problem description>`
   - Check awesome-lists: `awesome-<technology>`
   - Inspect code of similar projects

2. **Evaluate Existing Solutions** — Evaluate the quality of the solutions you find.
   - GitHub stars, forks, and contributor count
   - Last commit date (active maintenance?)
   - Issue and PR response times
   - License compatibility
   - Test coverage and documentation quality

3. **Decide to Borrow or Integrate** — Decide what to do in each case.
   - **Use directly:** If the solution meets the requirements perfectly
   - **Fork and customize:** If the solution is 80% compatible
   - **Take inspiration and write from scratch:** If none are suitable or if there is a licensing issue

```
# GitHub search examples:
# github.com/search?q=<problem>&type=repositories
# npm search: npm search <keyword>
# PyPI search: pip search <keyword>
```

**Output:** Evaluation of existing open-source solutions — decision to use, fork, or write from scratch.

---

## Phase 5: Alternative Analysis

**Compare 2-3 different approaches and choose the best one.**

1. **Identify Candidates** — List at least 2, preferably 3, different approaches.
   - Different libraries, different architectures, different algorithms

2. **Create a Comparison Table** — Evaluate each candidate using the same criteria.

| Criterion | Approach A | Approach B | Approach C |
|--------|-----------|-----------|-----------|
| Performance | High | Medium | Low |
| Maintainability | Medium | High | Low |
| Community Support | Large | Medium | Small |
| Learning Curve | Steep | Medium | Shallow |
| Documentation | Excellent | Good | Weak |
| License | MIT | Apache 2.0 | GPL |
| Dependency Count | 3 | 7 | 0 |

3. **Perform Trade-Off Analysis** — State the advantages and disadvantages of each decision.
   - Explain why one option is better in a given context.
   - Write decision rationales in the format "Approach X is better in this case because..."

```
| Criterion | Approach A | Approach B |
|--------|-----------|-----------|
| Performance | High | Medium |
| ... | ... | ... |

Recommendation: Since the project is small-scale, Approach B is more appropriate.
```

**Output:** Comparison table, trade-off analysis, a clear recommendation, and its rationale.

---

## Phase 6: Version & Compatibility Verification

**Be absolutely sure about the latest version and compatibility of everything you plan to use.**

1. **Version Verification** — Confirm the latest stable versions of all dependencies.
   - Check the official version for each package.
   - Avoid pre-release versions (alpha, beta, rc).

2. **Deprecation Check** — Ensure none of the dependencies are deprecated.
   - Run a "deprecated" query for each library used.
   - Detect deprecated APIs in older versions.

3. **Dependency Compatibility** — Verify compatible versions of packages with each other.
   - Pay attention to peer dependencies.
   - Check Node.js/Python/Ruby version requirements.

4. **Vulnerability Scanning** — Check for known security vulnerabilities.
   - `npm audit`, `pip audit`, `cargo audit`
   - GitHub Dependabot alerts

```
# Version and security checks:
npm outdated
npm audit
pip list --outdated
pip-audit
cargo audit
```

**Output:** Verified versions of all dependencies, security status, and compatibility matrix.

---

## Phase 7: Community Wisdom

**Learn known pitfalls from Stack Overflow, GitHub Issues, and forums.**

1. **Search Stack Overflow** — Find solutions in advance for problems you might encounter.
   - Query: `site:stackoverflow.com <technology> <problem>`
   - Top-voted questions and answers
   - Search with keywords like "gotchas" or "pitfalls"

2. **Scan GitHub Issues** — Learn from open and closed issues.
   - Known issues, bug reports
   - Feature requests (future plans)
   - Solved issues and workarounds

3. **Read Blogs and Articles** — Leverage developers' experiences.
   - Medium, Dev.to, personal blogs
   - Articles like "Why I stopped using X"
   - Migration stories (transitioning from v1 to v2)

```
# Community search examples:
# site:stackoverflow.com fastapi database session
# github.com/<org>/<repo>/issues?q=is%3Aissue+label%3Abug
# "fastapi common mistakes" blog search
```

**Output:** List of known pitfalls, common errors and their solutions, and recommended workarounds.

---

## Phase 8: Synthesis

**Convert all research findings into a single report.**

Compile research findings using the following template:

```markdown
# Research Synthesis Report

## Project Context
- Technologies used, architecture, patterns
- Related files and modules

## Dependencies
| Package | Current Version | Latest Version | Notes |
|-------|-------------|-------------|--------|
| react | 18.2.0 | 19.1.0 | Contains breaking changes |
| axios | 1.6.0 | 1.8.0 | Security patch available |

## Alternatives Comparison
- Recommended approach: [Approach A]
- Rationale: [summary of trade-off analysis]

## Critical Warnings
- [Deprecated APIs, breaking changes, security vulnerabilities]
- [Known pitfalls and workarounds]

## Recommendations
- [Clear, actionable recommendations]
- [Next step: transition to spec-first-development or architecture-planner]
```

**Output:** Structured research synthesis report.

---

## Worked Example

**Scenario:** A Node.js API service needs to process outbound emails and PDF exports asynchronously. The team wants a background-job library. No job queue exists in the repo yet.

### Phase 1 — Context Compilation

Scan findings:
- Runtime: Node.js 20 LTS, TypeScript 5.4, Express 4.
- Existing persistence: PostgreSQL 16 via `pg` driver. No Redis instance in docker-compose.
- `package.json` has no existing job/queue dependency.
- Related files: `src/mailer.ts`, `src/exports/pdf.ts` — both called inline from request handlers (blocking the event loop on large exports).

**Context map conclusion:** We need async processing with durable job storage. PostgreSQL is already present; adding Redis would mean a new infrastructure component. TypeScript support is mandatory.

### Phase 2 — Web Research (version check, 2026-05)

```bash
npm view bull version          # 4.16.3  (latest stable)
npm view bullmq version        # 5.12.0  (latest stable)
npm view pg-boss version       # 10.1.2  (latest stable)
```

BullMQ 5.x requires Redis 7.2+. Bull 4.x (predecessor) is in maintenance mode — no new features, security patches only. `pg-boss` runs entirely on PostgreSQL with no additional infrastructure.

### Phase 3 — Documentation Review

- **BullMQ v5 migration guide:** `Queue` constructor options renamed; `createBullBoard` adapter updated. Breaking change from v4: workers must be created with `new Worker(…)` — the v3 `process()` callback is removed.
- **pg-boss v10 changelog:** `pg-boss` now requires `pg` ≥ 8.11. Project uses `pg` 8.12 — compatible. New in v10: `sendAfter` API replaces `publishAfter` from v8.
- **Bull (v4):** Docs mark several queue methods deprecated (`add` options `delay` shape changed in v5, but v4 is frozen).

### Phase 4 — Solution Discovery

GitHub search: `site:github.com background jobs node postgres no redis`. Top result: `pg-boss` (4.2 k stars, last commit 3 weeks ago, 23 open issues / 4 labeled `bug`). No awesome-list entry for a maintained pure-Postgres queue with TypeScript types that outranks it.

### Phase 5 — Alternative Analysis

| Criterion | BullMQ 5 | Bull 4 (legacy) | pg-boss 10 |
|-----------|-----------|-----------------|------------|
| Infrastructure | Redis 7.2+ required | Redis required | PostgreSQL only — already present |
| Maintenance status | Active | Security patches only | Active |
| TypeScript types | First-class (`@types` bundled) | `@types/bull` (community) | Bundled |
| Throughput (jobs/s) | ~10 000+ | ~8 000 | ~500–2 000 |
| Durable across restarts | Yes (Redis persistence) | Yes | Yes (WAL-backed) |
| License | MIT | MIT | MIT |
| New infra cost | Redis instance + ops | Redis instance + ops | None |
| Known issues | Cluster mode config subtle | Frozen; won't fix new bugs | Advisory locks can block under very high concurrency |

**Trade-off analysis:**
- BullMQ is the performance leader but forces a Redis deployment. For the expected load (hundreds of jobs/hour, not thousands/second) this is over-engineering.
- Bull 4 is ruled out — maintenance-only status is a disqualifying flag for a new dependency.
- pg-boss fits the constraint set: no new infrastructure, durable, TypeScript-native, actively maintained, and adequate throughput for the workload.

### Phase 6 — Version & Compatibility Verification

```bash
npm view pg-boss peerDependencies   # {"pg": ">=8.11"}
node -e "require('./package.json').dependencies.pg"  # "^8.12.0" — satisfied
npm audit                           # 0 vulnerabilities
```

pg-boss v10.1.2: no open CVEs, peer-dep satisfied, no deprecated API used by this project.

### Phase 7 — Community Wisdom

Stack Overflow (`site:stackoverflow.com pg-boss`): top-voted Q&A warns that `pg-boss` schema migrations run automatically on `start()` — they must not be called concurrently from multiple processes during a rolling deploy. Solution: use the `noSupervisor` option in workers and run `boss.start()` only from a single designated process or a migration job.

GitHub Issues (`pg-boss` label `bug`, open): 4 issues. None affect `sendAfter` or basic worker patterns. One is a niche issue with `LISTEN`/`NOTIFY` under PgBouncer transaction pooling — project uses session pooling, so not affected.

### Phase 8 — Synthesis

**Recommendation: adopt `pg-boss` v10.1.2.**

Rationale: It is the only candidate that adds zero new infrastructure. Throughput (≤ 2 000 jobs/s) comfortably covers the projected load. TypeScript types are bundled. License is MIT. The one real pitfall — concurrent `start()` calls during rolling deploys — is well-documented and has a one-line mitigation (`noSupervisor: true` on worker processes, `start()` only in the main API process).

BullMQ would be revisited if throughput requirements exceed ~5 000 jobs/minute — at that point the Redis operational cost is justified.

**Next step:** hand this report to `spec-first-development` to define the job schemas and retry policies before writing any code.
