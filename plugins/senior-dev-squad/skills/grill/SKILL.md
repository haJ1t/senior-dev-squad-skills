---
name: grill
description: "Relentlessly interviews the user one question at a time to reach shared understanding before any code is written. Use when aligning on requirements, stress-testing a plan, or starting a feature."
---

# Grill

## Overview

Before writing a single line of code, use a structured interview to surface assumptions, resolve terminology, and confirm that everyone involved shares the same mental model of what is being built and why. Misaligned understanding is the leading cause of rework; this skill front-loads the alignment cost so implementation is cheap and correct.

The process is deliberately slow and deliberate: one question at a time, each answered before the next is asked, with your own recommended answer offered alongside every question. You are not interrogating the user — you are thinking out loud together, walking the design tree branch by branch until no unresolved fork remains.

**Core principle:** NO BUILDING BEFORE ALIGNMENT. Shared understanding is the deliverable of this phase.

## The Iron Law

```
ONE QUESTION AT A TIME — NEVER ASK TWO THINGS IN THE SAME MESSAGE
```

Every question you ask must be fully answered before you ask the next. Bundling questions is a red flag that you are rushing toward implementation.

## When to Use

**Use this when:**
- A new feature, product area, or integration is requested
- Requirements are stated in vague or overloaded terms ("make it smart", "handle edge cases", "be flexible")
- The user has a plan they want to stress-test before committing to it
- You are uncertain which of two reasonable interpretations the user intends
- The project is entering a phase with hard-to-reverse decisions (data model, public API contract, auth strategy)

**Use this ESPECIALLY when:**
- Someone says "let's just start and figure it out" — the interview costs minutes; course-correction costs days
- The feature has been described differently in different conversations
- Multiple stakeholders are involved and you have only heard from one
- You notice that key terms are used inconsistently (e.g., "user", "account", "workspace" all meaning different things)

**Don't skip when:**
- Under time pressure (a 10-minute alignment session beats a 3-day rewrite)
- The feature seems small (small features still have forks in the design tree)

## Interview Protocol

### Starting the Session

Open by stating the topic and asking the single most load-bearing question first — the one whose answer constrains the most other answers. Do not list all the questions you intend to ask. Do not explain your process at length. Ask one question and wait.

Format every question like this:

> **Question:** [The question, stated simply and precisely]
>
> **My recommended answer:** [Your honest recommendation with brief rationale]

This makes it easy for the user to confirm your recommendation or correct it, without requiring them to construct an answer from scratch.

### Walking the Design Tree

After each answer, do one of three things before asking the next question:

1. **Confirm understanding** — restate what was just decided in one sentence so the user can catch misinterpretation immediately.
2. **Note a dependency unlocked** — if the answer resolves a downstream question, say so before moving on.
3. **Probe further** — if the answer reveals a new ambiguity, ask about that next rather than moving down your original list.

This is not a linear checklist. It is depth-first traversal of the decision tree, guided by what you learn at each node.

### Reading the Codebase First

Before asking the user any question that the codebase can answer, read the relevant files. If you can resolve "how is authentication currently handled?" by reading the code, do that — do not ask. Questions should cover decisions that have not yet been made, not facts that already exist. Demonstrating that you read the code before asking builds trust and saves time.

### Resolving Terminology

When a term is used in a way that could mean two different things — or when the same concept has been called different names in different messages — pause and challenge it directly:

> **Term under review:** "session"
>
> I notice this word has been used to mean both (a) a browser authentication session and (b) a collaborative editing session. These are different concepts that will need different data structures and lifecycle rules. I propose we call them **auth-session** and **collab-session** going forward.
>
> **Question:** Does that distinction match your mental model, or should we draw the boundary differently?

Once agreed, record the canonical term and its definition in `CONTEXT.md` at the project root (or `docs/CONTEXT.md` if a `docs/` directory exists). This is the project's ubiquitous language. Every subsequent conversation, spec, and ADR should use only these canonical terms.

### Stress-Testing with Edge Cases

After the core design is understood, introduce concrete edge-case scenarios to probe the plan:

- "What happens if the user submits the form twice in rapid succession?"
- "What should the system do if the third-party payment provider returns a 500?"
- "What is the expected behavior if two users edit the same record simultaneously?"

These are not adversarial — they are gifts. A scenario that breaks the plan before code is written is far more valuable than one that breaks it in production. When a scenario reveals a gap, treat it as a new question and walk it through the protocol.

Also cross-check stated plans against the actual codebase. If the user says "we already handle retries in the API client", verify that claim by reading the relevant file before accepting it as a constraint.

### Recording Hard Decisions as ADRs

When the interview produces a decision that is hard to reverse — a data model choice, a public contract, a dependency on a specific vendor, an authentication strategy — record it as an Architecture Decision Record. Point to `docs/adr/` for the file location and `templates/ADR-FORMAT.md` for the required format. Do not write the ADR yourself during the interview; flag that the decision warrants one and confirm the user will create it before implementation begins.

> **ADR warranted:** Choosing to store audit logs in a separate PostgreSQL schema rather than a separate service is a deployment-topology decision that will be expensive to undo. This should be captured as an ADR before we proceed.

### Stop Condition

The interview is complete when:

1. Every question in the design tree has been answered or explicitly deferred with a written rationale.
2. All key terms used in the spec are recorded in `CONTEXT.md`.
3. Any ADR-worthy decisions have been flagged and queued.
4. Open questions that cannot be resolved yet are captured in a numbered list, not left implicit.

Summarize the session: list what was decided, what was deferred, and what ADRs are needed. Then explicitly hand off to the next skill (typically `spec-first-development` or `architecture-planner`).

## Red Flags — STOP and Follow Process

If you catch yourself doing any of the following, stop and return to the protocol:

- Asking two questions in the same message
- Offering implementation suggestions before the interview is complete
- Accepting a vague answer without requesting precision ("flexible" is not an answer)
- Using a term that has not been defined in `CONTEXT.md` as if its meaning is obvious
- Moving to the next question without confirming the previous answer
- Skipping the codebase read and asking a question the code already answers
- Treating the interview as a formality and rushing to get it over with
- Writing any code, schema, or config during the interview phase

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I already understand what they want, the interview is a waste of time" | You understand your interpretation of what they said. Those are different things. Run the interview. |
| "We can align as we go during implementation" | Mid-implementation corrections are 5-10x more expensive than pre-implementation ones. Align first. |
| "The feature is simple enough that we don't need this" | Simple features have forks too. A five-minute interview on a simple feature costs almost nothing. |
| "They seem confident in their plan, I shouldn't challenge it" | Stress-testing a confident plan is a service, not a criticism. Unchallenged plans have unchallenged blind spots. |
| "I'll just note the ambiguity and handle it later" | Ambiguity deferred is a decision made by accident. Make it on purpose, now, in writing. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "That's not what I meant" — You moved on from an answer without confirming your interpretation.
- "Can we back up?" — You went too far down one branch before resolving a higher-level fork.
- "Why are you asking that?" — Your question is not load-bearing; you are asking out of habit, not because the answer matters.
- "Just build it, I'll tell you when it's wrong" — The user has lost confidence in the interview process, likely because previous questions felt redundant or low-value. Return to the highest-priority open question and make the value of that question explicit.
- "You already asked that" — You forgot to record the answer. Update `CONTEXT.md` and continue.
- "You're overthinking it" — Your recommended answer for a question was more complex than the situation warrants. Simplify and re-ask.

**When you see these:** STOP. Name what you observed, acknowledge it, and correct course.

## Related Skills

- **spec-first-development** — the natural successor; run after alignment is complete to turn decisions into formal acceptance criteria
- **project-discovery** — use before grilling when the codebase is unfamiliar and you need to map the territory before asking intelligent questions
- **architecture-planner** — use after grilling when the decisions made warrant a formal architecture design pass
- **setup-senior-dev-squad** — use when onboarding to a new project before any feature work begins
- **user-story-refiner** — use after grilling to sharpen user stories that surfaced during the interview into well-formed, testable form

## Verification

- [ ] Every question was asked one at a time with your recommended answer provided
- [ ] No implementation suggestions were made before the interview concluded
- [ ] All vague or overloaded terms have been challenged and resolved
- [ ] Canonical terms are recorded in `CONTEXT.md` with definitions
- [ ] At least one concrete edge-case scenario was used to stress-test the plan
- [ ] Codebase was read before asking any question the code could have answered
- [ ] All hard/irreversible decisions have been flagged for ADR creation
- [ ] Open questions that could not be resolved are captured in a numbered list
- [ ] A session summary was produced: decisions made, deferred items, ADRs needed
- [ ] Handoff to the next skill (spec-first-development or architecture-planner) was explicit
