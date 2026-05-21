---
name: error-message-optimizer
description: "Improve error messages for developer experience — clarity, actionability, context, and debugging speed. Use when reviewing or rewriting error messages."
version: 1.0.0
platforms: [linux, macos]
---

# Error Message Optimizer

## What It Does
Audits and improves error messages across a codebase for developer experience. Analyzes existing error messages against clarity standards, identifies "mystery errors" that waste debugging time, and rewrites them to answer three questions: What happened? Why did it happen? What do I do about it? Reduces mean-time-to-resolution (MTTR) by making errors self-diagnosing.

## Iron Laws (NEVER violate)
1. **What + Why + Fix** — Every error message must answer: what went wrong, why it happened, and how to fix it. Two out of three is failure.
2. **Context is not optional** — Include relevant state: input values, configuration, environment, stack trace (when safe). "Something went wrong" is not an error message.
3. **No blame, no jargon** — Errors must not blame the user or use internal jargon. "Invalid input" → "Expected a number between 1-100, got 'abc'."
4. **Error codes are not messages** — "Error E1452" without explanation is hostile. Codes supplement messages, not replace them.

## Red Flags (STOP immediately)
- **Information leak** — Error message exposes secrets, internal paths, or database structure → security vulnerability
- **Misleading error** — Error message points to wrong cause → developers debug in the wrong place; fix the message
- **Silent failure** — Operation fails but produces no error message → invisible bug; add logging
- **Error cascade** — First error triggers 50 meaningless follow-up errors → catch and suppress cascading errors

## Common Rationalizations (self-deception)
- "Developers will figure it out from the stack trace" → Stack traces show WHERE, not WHY. Context reduces debugging time by 10x.
- "Good error messages take too long to write" → A good error message saves 100+ developer-hours of debugging. ROI is enormous.
- "This error rarely happens" → Rare errors have the worst messages because nobody invested in them. That's when you need them most.

## When To Use
- Auditing a codebase for developer experience quality
- User complains about cryptic error messages
- Reducing support ticket volume from confusing errors
- Establishing error message standards for a team
- Debugging a production incident caused by unclear error reporting

## Human Partner Signals (escalate to human)
- **Security boundary** — Error message must not reveal information in untrusted contexts → security review
- **Localization** — Error messages shown to end-users in multiple languages → i18n coordination
- **Compliance** — Error message content regulated (PCI, HIPAA) → compliance review
- **UX conflict** — Technical accuracy vs user-friendly language → product/UX decision

## Pipeline
1. Inventory: catalog all error messages in the codebase — error codes, messages, context
2. Classify: categorize by clarity — clear (all 3 questions answered), partial (1-2 answered), mystery (0 answered)
3. Prioritize: rank by frequency × debugging cost — most expensive mystery errors first
4. Redesign: rewrite top offenders using What/Why/Fix template with context
5. Validate: test new messages with developers unfamiliar with the code → can they fix the issue?
6. Standardize: create error message style guide and linting rules for future code
7. Monitor: track error frequency before/after, measure reduction in related support tickets

## Verification Checklist
- [ ] All error messages answer What/Why/Fix (tested by sampling top 20 errors)
- [ ] No secrets, internal paths, or DB structure in error messages
- [ ] Context included: input values (sanitized), relevant config, environment hint
- [ ] Error codes supplement messages, not replace them
- [ ] Silent failures eliminated — every failure path produces an observable error
- [ ] Cascading errors suppressed beyond the root cause
- [ ] New error message standard enforced via linting/CI



## Output Schema (MANDATORY)

Structure your response with:
1. **Analysis** — What you found/designed
2. **Concrete output** — Code, YAML, tables (not just descriptions)
3. **Tradeoffs/risks** — What you chose and why, what could go wrong
4. **Verification** — How to confirm correctness

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague recommendations | Not actionable | Concrete examples, specific steps |
| Missing tradeoffs | One-sided analysis | Every choice: "X over Y because..." |
| "Consider doing X" | No commitment | "Do X. Why: [reason]" |
| No verification criteria | Can't confirm quality | "Verify by: [test/check]" |
| Generic response | Not tailored | Domain-specific vocabulary, exact tool names |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Specificity | Generic advice | Some specifics | Concrete, actionable output |
| Tradeoff awareness | None | Mentioned | Documented with alternatives |
| Output format | Free text | Partial structure | Structured, scannable |
| Verification | None | Vague | Specific test/criteria |
| Domain accuracy | Wrong terms | Mostly correct | Precise domain vocabulary |

**Pass: 7/10**
## Related Skills
- `systematic-debugging` — Better error messages accelerate all 4 phases of debugging
- `code-reviewer` — Error message quality is a review criterion
- `documentation-generator` — Error message catalog as living documentation
- `observability-pro` — Structured error logging for production observability
