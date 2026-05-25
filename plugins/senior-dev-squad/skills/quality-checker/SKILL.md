---
name: quality-checker
description: "Post-generation verification: runs checklists on specs, plans, tasks to catch gaps before handoff. Use when reviewing AI output for completeness and correctness."
---

# Quality Checker

## Overview

After generating any planning document (spec, architecture, tasks, prompt), run a structured quality check before handing off to the next phase. Catches missing sections, vague language, and unverified assumptions.

**Core principle:** EVERY DOCUMENT GENERATED IS A CONTRACT. QUALITY-CHECK EVERY CONTRACT BEFORE SIGNING IT.

## The Iron Law

```
NEVER HAND OFF A DOCUMENT THAT HASN'T PASSED ITS QUALITY CHECKLIST
```

A document with gaps will produce wrong implementation. Every time.

## When to Use

**Use this when:**
- After spec-first-development generates SPECIFICATION.md
- After architecture-planner generates architecture doc
- After task-breaker generates TASKS.md
- After agent-prompt-builder generates PROMPT.md
- After any document generation

## Quality Checklists

### After SPECIFICATION.md

```
☐ Every user story has at least one acceptance criterion
☐ Every criterion is in Given/When/Then format
☐ All four states documented (loading, empty, error, success)
☐ Edge cases documented (empty, error, boundary, concurrent)
☐ Non-goals explicitly listed
☐ Data model changes identified
☐ Security implications assessed
```

### After Architecture Doc

```
☐ Every bounded context has clear responsibility
☐ API contract documented before implementation
☐ Database schema has additive migration plan
☐ Auth model covers authN + authZ
☐ Deployment model covers dev/staging/prod
☐ Risk register has mitigations for High/Critical
☐ Every decision has documented tradeoffs
```

### After TASKS.md

```
☐ Every task completable in one session
☐ Tasks ordered by strict dependency
☐ Each task specifies exact files (Create/Modify/Test)
☐ No "implement all" or similar vagueness
☐ Phases have clear milestones
☐ Test step exists for every implementation task
```

### After PROMPT.md

```
☐ Agent can execute without asking questions
☐ All dependencies have specific versions
☐ All file paths are exact
☐ All code patterns are complete (not placeholders)
☐ Verification method after every step
☐ No "TBD" or "TODO" remain
```

## Red Flags

Any document that passes all checklist items but still "feels wrong." Any checklist item you're tempted to skip because "the document is good enough." Any item you answer "yes" without actually verifying.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The author is experienced, the doc is probably fine" | Quality gaps hide in confident writing. Check every item, regardless of author seniority. |
| "We're behind schedule, ship the doc" | A document with gaps will cause rework in implementation that costs far more time than a 10-minute review. |
| "I skimmed it and it looks complete" | Skimming misses vague acceptance criteria, missing edge cases, and undocumented assumptions every time. |
| "The team already reviewed this verbally" | Verbal agreements do not survive handoffs. What isn't written isn't agreed. |
| "Only a few items failed, the rest is solid" | A document that fails any checklist item is incomplete. Partial compliance is non-compliance. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Wait, what happens when X fails?" — You approved a document that didn't cover error states or edge cases.
- "I thought we agreed the scope didn't include Y" — Non-goals were not explicitly listed in the document you cleared.
- "The agent built the wrong thing" — You signed off on acceptance criteria that were vague enough to be misinterpreted.
- "Why does this task reference a file that doesn't exist yet?" — You passed a TASKS.md without verifying dependency order.
- "This has TBDs in it" — You marked a PROMPT.md complete without confirming every field was resolved.

**When you see these:** STOP. Reopen the checklist for the relevant document type, identify which items were incorrectly marked passing, and re-run the full check.

## Verification

Before declaring a document checked:

- [ ] Selected the correct checklist for the document type (spec / architecture / tasks / prompt)
- [ ] Every checklist item verified against the actual text, not assumed
- [ ] Each failed item recorded with the specific gap (section + what is missing)
- [ ] Verdict is PASS only if zero items failed (partial compliance = fail)
- [ ] Gaps handed back to the generating skill before any downstream handoff

## Related Skills

- **code-reviewer** — applies to code (this skill applies to documents)
- **ship-readiness-checklist** — final gate for production (this is for intermediate docs)
- Every document-generating skill — this checker validates their output
