---
name: documentation-generator
description: "Auto-generate documentation from code — API references, READMEs, architecture docs, and ADRs. Use when generating or updating project documentation."
version: 1.0.0
platforms: [linux, macos]
---

# Documentation Generator

## What It Does
Automatically generates high-quality documentation from codebases. Produces API reference docs from OpenAPI/GraphQL schemas, README files from package structure, architecture decision records (ADRs) from design discussions, and codebase overviews from directory structure and module docstrings. Ensures docs stay in sync with code through CI/CD integration.

## Iron Laws (NEVER violate)
1. **Docs as code** — Documentation lives alongside code in version control. Generated docs are build artifacts, not source of truth.
2. **Every public API documented** — Any function, class, endpoint, or type marked public MUST have a docstring. No exceptions.
3. **Examples are mandatory** — Every API reference entry must include at least one working code example. Docs without examples are puzzles.
4. **Drift detection** — CI must detect when docs are out of sync with code. Stale docs are worse than no docs.

## Red Flags (STOP immediately)
- **Doc drift** — Documentation describes behavior that no longer matches the code → fix docs or fix code
- **Auto-generated noise** — Generated docs full of "TODO: document this" → generation pipeline broken
- **Broken examples** — Code examples in docs don't compile/run → examples are lies; fix immediately
- **Missing context** — API reference exists but no architecture overview → developers can't see the big picture

## Common Rationalizations (self-deception)
- "The code is self-documenting" → Code explains WHAT and HOW, not WHY. Documentation explains intent.
- "We'll write docs after the launch" → Post-launch documentation never happens. Write alongside development.
- "Auto-generated docs are good enough" → Auto-generation handles structure. Humans must provide context and examples.

## When To Use
- Setting up documentation infrastructure for a new project
- Generating API reference docs from OpenAPI/GraphQL schemas
- Creating README files that auto-update from package metadata
- Writing Architecture Decision Records (ADRs) for key design decisions
- Auditing documentation coverage and freshness

## Human Partner Signals (escalate to human)
- **Doc ownership gap** — Critical component has no doc owner → assign ownership
- **External-facing docs** — Documentation will be public → marketing/legal review
- **Translation needed** — Docs needed in multiple languages → localization planning
- **Sensitive architecture** — Architecture docs expose security-sensitive design → review before publishing

## Pipeline
1. Audit: scan codebase for documentation coverage — what's documented, what's missing, what's stale
2. Generate: extract API schemas → generate reference docs; extract docstrings → generate module docs
3. Enrich: add context — architecture overview, getting-started guide, common workflows, examples
4. Structure: organize docs logically — overview → getting started → guides → API reference → ADRs
5. Integrate: add CI checks for doc freshness, broken links, example validity
6. Publish: generate static site (MkDocs, Docusaurus, VitePress) or integrate with existing docs platform

## Verification Checklist
- [ ] All public APIs have docstrings with working code examples
- [ ] CI pipeline detects doc drift (docs out of sync with code)
- [ ] All code examples in docs compile and pass tests
- [ ] Architecture Decision Records exist for major design decisions
- [ ] Getting-started guide takes new developer from zero to first PR in <30 minutes
- [ ] Documentation search works and returns relevant results

## 1. Components/Contexts
[Table: Name | Responsibility | Data | Dependencies]
## 2. Decisions (ADR format)
### ADR-001: [Title]
**Context:** [Why] **Options:** [2+ alternatives] **Decision:** [What] **Tradeoffs:** [+gain / -sacrifice]
## 3. Communication Matrix
[Table: From→To | Pattern | Protocol | Timeout | Retry]
## 4. Data & CAP Analysis
[Per store: Type | CP/AP | Partition behavior]
## 5. Deployment Topology
[ASCII diagram]
## Verdict: READY / NEEDS CLARIFICATION
```

## Related Skills
- `api-design-reviewer` — API design provides the schema that docs are generated from
- `spec-first-development` — Specs are documentation written before code
- `onboarding-automator` — Generated docs accelerate developer onboarding
- `dev-environment-manager` — Docs include environment setup instructions
