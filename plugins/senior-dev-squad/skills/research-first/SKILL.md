---
name: research-first
description: "Comprehensive research before writing code: context compilation, web search, documentation review, alternative analysis, and synthesis. Use before starting implementation."
---

# Research First

## Overview

Before starting to write code, systematically research the existing code, documentation, library versions, open-source solutions, and best practices. This skill prevents reinventing the wheel, using outdated APIs, or building on top of incorrect foundations. Code written without research is technical debt waiting to be discovered.

**Core Principle:** RESEARCH BEFORE WRITING ANY CODE. Know the entire context, alternatives, and pitfalls before writing the first line of code.

## The Iron Law

```
RESEARCH MUST BE COMPLETED BEFORE WRITING CODE. NOT A SINGLE LINE OF CODE MAY BE WRITTEN.
```

No files will be created and no functions will be written before the research synthesis report is completed.

## When to Use

**Use this when:**
- Starting a new project, feature, or component.
- Seeking a solution for a library/framework.
- Understanding and refactoring existing code.
- Determining the best approach to solve a problem.
- Choosing a tech stack or making technology decisions.

**Use this ESPECIALLY when:**
- You say "I already know this, I can write it immediately" (what you think you know might be outdated).
- You are not sure about the version of the library you are using.
- You suspect there might be an open-source tool that already solves the same problem.
- You are contributing to a complex, unfamiliar codebase.

**Never skip when:**
- You say "this is too simple, no need for research" — even simple-looking problems can have updated APIs or new best practices.
- You say "this is urgent, I must solve it immediately" — research does NOT waste time; on the contrary, it SAVES time by reducing the risk of mistakes.
- You say "I already know this topic" — no information is exempt from verification.

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

## Final Verification

Complete the appropriate verification steps depending on the project's current status:

**New Project / Stack Selection:**
- [ ] At least 3 alternative libraries/frameworks evaluated.
- [ ] Comparison table created with a clear recommendation.
- [ ] Selected technology's license is appropriate.
- [ ] Latest stable versions are used.
- [ ] No dependencies are deprecated.

**Contributing to an Existing Project:**
- [ ] Context map of the codebase created.
- [ ] All related files identified.
- [ ] Current patterns and styles understood.
- [ ] Configuration files inspected.

**General Verification:**
- [ ] Versions of all dependencies verified.
- [ ] No deprecation warnings found.
- [ ] Security vulnerability scan performed (npm audit/pip audit, etc.).
- [ ] Pitfalls researched on Stack Overflow / GitHub Issues.
- [ ] Community best practices taken into account.
- [ ] Research synthesis report documented.

## Red Flags — Stop and Audit

If you find yourself thinking:

- "I already know this, no need for research" — You must verify the currency of your knowledge.
- "This is very simple, I can write it in 5 minutes" — Even simple things have pitfalls.
- "Research is a waste of time" — Code written on a faulty foundation is 10 times more expensive to fix.
- "Let me start coding first, I'll do the research later" — The sequence is wrong; research first.
- "Everyone is using X, so it must be the best" — Popularity is not a guarantee of quality.
- "This library is already in the project, so it must be the best" — It might not be the most suitable; check alternatives.
- "No need for version checks, it works" — Outdated versions mean security vulnerabilities and performance loss.

**ALL OF THE ABOVE MEAN: STOP. RETURN TO THE RELEVANT PHASE.**

## Signals Your Human Partner Warns You With

**Pay close attention to these instructions:**

- "That library is deprecated now" — Version and deprecation checks were skipped.
- "Where did you get this from?" — Source was not specified or verified.
- "This method was removed 2 years ago" — Documentation was not read.
- "How do you know this?" — Research was not conducted, assumptions were made.
- "Actually, there is a better solution" — Alternative analysis was not performed.
- "Did you look to see if anyone has solved this problem before?" — Solution discovery was skipped.

**When you see these:** STOP. Return to Phases 1-3 (context, web research, document review).

**Signals indicating that research is sufficient:**
- "Yes, this approach is correct" — Research is thorough and instills confidence.
- "Nice, I didn't know that" — Research has uncovered new information.
- "Yes, this is the latest version" — Version verification was done.
- "Okay, I'm convinced on this" — Alternative analysis is sufficient.

## Common Rationalizations

| Excuse | Reality |
|--------|--------|
| "I already know it, no need for research" | What you know might have changed 6 months ago. APIs, best practices, and libraries are updated constantly. |
| "This is very simple, I can write it in 5 minutes" | Pitfalls of simple things usually appear at the last minute. 5 minutes of research prevents hours of debugging. |
| "Everyone is using X, so it must be the best" | Popularity $\neq$ quality. The most suitable solution for your need might not be the most popular one. |
| "Research is a waste of time, let's write code immediately" | Rewriting code written on a faulty foundation takes 10 times longer than the initial research. |
| "We'll look at Stack Overflow later" | Learning known pitfalls before encountering the problem is much faster than solving them afterward. |
| "Version checks are useless, if it works don't touch it" | Outdated versions = known security vulnerabilities, performance issues, and missing features. |
| "No need to think about alternatives, I'll use the first one that comes to mind" | The first solution that comes to mind is rarely the best. Evaluating 2-3 alternatives takes 15 minutes. |

## Related Skills

- **spec-first-development** — used to write specifications after the research synthesis report is completed
- **architecture-planner** — research findings feed architectural decisions
- **tech-stack-advisor** — research findings form input for stack selection, working alongside this skill
- **project-discovery** — clarifies project requirements before research
- **edge-case-hunter** — pitfalls discovered during research feed the edge case list
- **security-reviewer** — security vulnerabilities detected during research provide input to this skill

## Self-Review

After completing the process of this skill:

1. **Scope Check:** Have you scanned all relevant files in the project? Have you skipped any modules?
2. **Alternative Check:** Have you evaluated at least 2 alternative approaches? Did you justify your decision?
3. **Currency Check:** Have you verified the latest stable version of every dependency you use?
4. **Deprecation Check:** Is it true that no library/function is deprecated?
5. **Security Check:** Have you performed a known vulnerability scan? (npm audit, pip audit, etc.)
6. **Community Check:** Have you researched known pitfalls on Stack Overflow and GitHub Issues?
7. **Synthesis Check:** Have you collected all findings in a structured synthesis report?
8. **Iron Law Check:** Did you complete the research before writing a single line of code?

## Endpoint: [METHOD] [PATH]
### Request
```json
{"field": "type (constraints)"}
```
### Success (200/201)
```json
{"data": {}, "meta": {"requestId": "uuid"}}
```
### Errors
| Status | Code | When |
### Implementation
```[lang]
[Full code with: validation, auth, transaction, logging, rate limit, idempotency]
```
```
