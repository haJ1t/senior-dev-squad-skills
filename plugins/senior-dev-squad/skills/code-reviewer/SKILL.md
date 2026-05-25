---
name: code-reviewer
description: "PR, API design, and planning-document review: blocking issues, missing tests, security, API consistency, spec completeness. Use when reviewing a PR, API design, or planning doc."
---

# Code Reviewer

## Overview

Review code, API designs, and planning documents like a senior engineer. Find everything that would cause a bug in production, a maintenance headache six months from now, or a security incident tonight. "It works" is not enough.

**Core principle:** EVERY LINE OF CODE AND EVERY DOCUMENT IS A LIABILITY. Review as if you'll be paged at 3 AM because of it.

## The Iron Law

```
NEVER APPROVE A PR THAT HAS AN UNANSWERED SECURITY QUESTION
NEVER HAND OFF A DOCUMENT THAT HASN'T PASSED ITS QUALITY CHECKLIST
```

If you can't say "this is safe" or "this is complete" with confidence, you can't approve.

## When to Use

**Use this when:**
- A pull request is ready and needs review before merge
- Code changes touch authentication, authorization, or data persistence
- A feature was built without prior spec or architecture review
- The PR author is junior or the domain is unfamiliar to the team
- Designing or auditing a REST, GraphQL, or gRPC API for naming, versioning, error handling, and DX
- A planning document (spec, architecture, tasks, prompt) was generated and needs a quality gate before handoff

**Use this ESPECIALLY when:**
- The PR is labeled "urgent" or "hotfix" (pressure is when review gets skipped most)
- Changes touch payment processing, user data, or access control logic
- The diff is large (>200 lines) and risk of missing something is high
- A security-sensitive library or dependency is added or upgraded

**Don't skip when:**
- The code "looks fine at a glance" (surface appearance hides logic bugs)
- The author is senior (seniority reduces typos, not blind spots)
- Tests pass (tests prove the happy path works, not that the code is correct)

## Project Context

Before significant work, check for a project glossary and decision log:
- If `CONTEXT.md` exists, use its ubiquitous-language glossary for all naming, and respect the decisions recorded in `docs/adr/`.
- If they are missing and the work is non-trivial, consider `/senior-dev-squad:grill` (alignment + glossary/ADR capture) or `/senior-dev-squad:setup-senior-dev-squad` first.

## What to Check (Every PR)

### 1. Correctness

- Does the code do what the spec says? (not more, not less)
- Are edge cases handled? (empty, error, boundary, concurrent)
- Are assumptions documented?
- Does error handling recover gracefully?

### 2. Security

| Check | If Missing |
|-------|-----------|
| No hardcoded secrets | BLOCKING |
| Input validated at boundary | BLOCKING |
| SQL injection prevented | BLOCKING |
| Auth + authZ checked | BLOCKING |
| No XSS vectors | BLOCKING |
| IDOR prevented | BLOCKING |
| Rate limiting present | SUGGESTION |

### 3. Testing

- Are there tests for the new code?
- Do tests cover error states?
- Are edge cases tested?
- Do all tests pass?
- Are there flaky tests? (flag immediately)

### 4. Code Smells

| Smell | Why Bad | Action |
|-------|---------|--------|
| Function > 30 lines | Hard to understand | SUGGESTION: Split |
| Component > 200 lines | Too many responsibilities | SUGGESTION: Split |
| Magic number/string | Meaningless | SUGGESTION: Constant |
| `any` type | Type safety lost | SUGGESTION: Proper type |
| console.log left | Debug leftover | BLOCKING: Remove |
| Nested ternaries | Unreadable | SUGGESTION: Simplify |

## API Design Review

When reviewing an API design (REST, GraphQL, gRPC), apply these additional checks. See **REFERENCE.md §API Design Review Checklist** for the full pipeline, iron laws, and verification checklist.

**Stop immediately if:**
- A breaking change (field removed, type changed) ships in a minor/patch version
- API keys or tokens appear in URLs or query parameters
- Different endpoints return different error shapes
- Any list endpoint lacks pagination support

**Core checks:**
- Naming is consistent across all endpoints
- Error responses have a consistent shape with actionable messages
- Backward compatibility is preserved; breaking changes get a new major version
- Authentication uses headers, not query parameters
- Documentation matches the implementation

## Document / Spec Quality Review

When reviewing a planning document generated upstream (spec, architecture, TASKS.md, PROMPT.md), apply the per-type checklist from **REFERENCE.md §Document / Spec Quality Checklists**.

**Core principle:** A document with gaps produces wrong implementation. Every time.

**Gate rule:** The verdict is PASS only if zero checklist items fail. Partial compliance is non-compliance. Hand gaps back to the generating skill before any downstream handoff.

## Review Format

Every review follows this structure:

```markdown
## Review: PR #[number]

**Files:** X changed | **Lines:** +Y / -Z

### 🔴 BLOCKING (Must Fix Before Merge)
1. **[file:line]** Unvalidated user input in SQL query — injection risk
2. **[file:line]** Missing auth check on DELETE endpoint

### 🟡 SUGGESTIONS
1. **[file:line]** Function is 60 lines — consider splitting

### 🔵 PRAISE
- Error handling is thorough with recovery paths

### Summary
**Blocking:** 2 | **Suggestions:** 3 | **Verdict:** Changes requested
```

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I trust this developer, I'll skim it"
- "I'll approve now, looks fine"
- "The tests pass, it must be correct"
- "I don't need to check for security issues — that's someone else's job"
- "I'll leave the comments but approve anyway"
- "The code works on my machine"

**ALL of these mean: STOP. Read every changed line before approving.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The tests pass, the code must be correct" | Tests prove the happy path. They don't prove the auth check is right, the input is validated, or the edge case is handled. |
| "I trust this developer, I'll skim it" | Trust is not a review strategy. The best developers have blind spots and make typos. |
| "It's a small change, doesn't need deep review" | The most dangerous bugs hide in "small" changes — a single missing null check or inverted condition. |
| "I'll add a comment but approve anyway" | Approving with unresolved blocking issues transfers the risk to production. Block until fixed. |
| "Security review is someone else's job" | Every reviewer is responsible for flagging security issues they see. No passing the buck. |
| "We'll document the API later" | Undocumented APIs are unusable. Documentation is part of the API contract. |
| "The doc is probably fine, the author is experienced" | Quality gaps hide in confident writing. Check every item regardless of author seniority. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "You approved this but it broke in production" — you skimmed instead of reading every changed line
- "This was already flagged in the last PR" — you're not tracking whether prior review comments were actually resolved
- "Why is this a suggestion and not a blocker?" — your severity ratings are too lenient and blocking issues are being soft-pedaled
- "Can you check the security angle more carefully?" — your review focused on style and missed the logic-level risk
- "You left 10 comments but no summary" — the review format was incomplete, leaving the author without clear direction
- "Wait, what happens when X fails?" — you approved a document that didn't cover error states or edge cases
- "The agent built the wrong thing" — you signed off on acceptance criteria that were vague enough to be misinterpreted

**When you see these:** STOP. Re-read the changed lines or reopen the relevant checklist from scratch. Apply checks in order: correctness, security, testing, code smells. Complete the full review format before submitting.

## Recommended Chaining

**When complete, recommended next (invoke manually or wire via hooks):**
- `cross-model-reviewer` — start multi-model review if PR is high-risk
- `refactor-simplifier` — initiate refactoring if code smells are detected
- `security-reviewer` — trigger if a security vulnerability is suspected
- `performance-engineer` — trigger if a performance issue is found

## Related Skills

- **security-reviewer** — deep security audit
- **test-engineer** — verifies test coverage
- **refactor-simplifier** — fixes code smells found in review
- **spec-first-development** — API specs written before implementation
- **ship-readiness-checklist** — final production gate (this skill covers intermediate review)

## Self-Review (Before Marking Review Complete)

- [ ] Every changed line read
- [ ] No blockers remain (security, correctness, data loss)
- [ ] Tests exist for new code
- [ ] Code smells flagged
- [ ] Review format followed (blocking → suggestions → praise)
- [ ] Unanswered questions documented
- [ ] If API design: API checklist in REFERENCE.md applied
- [ ] If planning document: per-type checklist in REFERENCE.md applied, zero failed items
