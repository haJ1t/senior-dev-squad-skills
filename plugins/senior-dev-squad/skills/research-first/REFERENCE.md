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
