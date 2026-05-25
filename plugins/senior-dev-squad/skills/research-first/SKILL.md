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

## Workflow

Work through the eight phases in order. Each phase builds on the last.

**Phase 1 — Context Compilation.** Scan the codebase, recognize existing patterns, find related files, and read configuration files. See [REFERENCE.md](REFERENCE.md) for example scan queries and expected outputs.

**Phase 2 — Web Research.** Check the latest versions of all dependencies, search for current best practices, and explore alternative libraries. See [REFERENCE.md](REFERENCE.md) for version-check commands per ecosystem.

**Phase 3 — Documentation Review.** Scan official docs for breaking changes, verify API signatures, and analyze sample code currency. See [REFERENCE.md](REFERENCE.md) for documentation lookup patterns.

**Phase 4 — Solution Discovery.** Search GitHub, GitLab, and awesome-lists for existing solutions before writing anything from scratch. See [REFERENCE.md](REFERENCE.md) for search examples and the use/fork/scratch decision criteria.

**Phase 5 — Alternative Analysis.** Identify 2-3 candidate approaches, build a comparison table, and perform trade-off analysis. See [REFERENCE.md](REFERENCE.md) for the full comparison table template and recommendation format.

**Phase 6 — Version & Compatibility Verification.** Confirm latest stable versions, run deprecation checks, verify peer-dependency compatibility, and scan for known vulnerabilities. See [REFERENCE.md](REFERENCE.md) for per-ecosystem audit commands.

**Phase 7 — Community Wisdom.** Search Stack Overflow, GitHub Issues, and developer blogs for known pitfalls and workarounds. See [REFERENCE.md](REFERENCE.md) for search query patterns.

**Phase 8 — Synthesis.** Compile all findings into a structured research synthesis report before writing any code. See [REFERENCE.md](REFERENCE.md) for the full report template.

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

## Common Rationalizations

| Excuse | Reality |
|--------|--------|
| "I already know it, no need for research" | What you know might have changed 6 months ago. APIs, best practices, and libraries are updated constantly. |
| "This is very simple, I can write it in 5 minutes" | Pitfalls of simple things usually appear at the last minute. 5 minutes of research prevents hours of debugging. |
| "Everyone is using X, so it must be the best" | Popularity ≠ quality. The most suitable solution for your need might not be the most popular one. |
| "Research is a waste of time, let's write code immediately" | Rewriting code written on a faulty foundation takes 10 times longer than the initial research. |
| "We'll look at Stack Overflow later" | Learning known pitfalls before encountering the problem is much faster than solving them afterward. |
| "Version checks are useless, if it works don't touch it" | Outdated versions = known security vulnerabilities, performance issues, and missing features. |
| "No need to think about alternatives, I'll use the first one that comes to mind" | The first solution that comes to mind is rarely the best. Evaluating 2-3 alternatives takes 15 minutes. |

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

## Related Skills

- **spec-first-development** — used to write specifications after the research synthesis report is completed
- **architecture-planner** — research findings feed architectural decisions
- **tech-stack-advisor** — research findings form input for stack selection, working alongside this skill
- **grill** — clarifies project requirements before research
- **edge-case-hunter** — pitfalls discovered during research feed the edge case list
- **security-reviewer** — security vulnerabilities detected during research provide input to this skill

## Verification

After completing this process, verify:

1. **Scope Check:** Have you scanned all relevant files in the project? Have you skipped any modules?
2. **Alternative Check:** Have you evaluated at least 2 alternative approaches? Did you justify your decision?
3. **Currency Check:** Have you verified the latest stable version of every dependency you use?
4. **Deprecation Check:** Is it true that no library/function is deprecated?
5. **Security Check:** Have you performed a known vulnerability scan? (npm audit, pip audit, etc.)
6. **Community Check:** Have you researched known pitfalls on Stack Overflow and GitHub Issues?
7. **Synthesis Check:** Have you collected all findings in a structured synthesis report?
8. **Iron Law Check:** Did you complete the research before writing a single line of code?

Final checklist before marking complete:

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
