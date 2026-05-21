---
name: session-memory
description: "Cross-session memory, past decisions, mistakes, repository context. Use when persisting context across sessions to avoid repeating prior work."
---

# Session Memory (Cross-Session Memory)

## Overview

This skill prevents the AI agent from starting from scratch in every session. It draws inspiration from ECC's continuous learning system and Harness Craft's repository memory. The agent records decisions, discoveries, mistakes, and repository context from past sessions; it loads this information at the start of each new session to continue exactly where it left off. Thanks to this accumulated knowledge over time, the agent makes fewer mistakes, makes faster decisions, and remembers project standards.

**Core Principle:** Every session is a continuation of the previous one. The agent does not erase its history; it accumulates it, becoming smarter every time.

## The Iron Law

```
AT LEAST ONE DECISION, ONE MISTAKE, AND ONE CONTEXT RECORD MUST BE MADE AT THE END OF EVERY SESSION.
NO SESSION ENDS WITHOUT RECORDING.
```

## When to Use

**Always use when:**
- Working on multiple sessions in a long-running project.
- Working regularly on the same codebase and making repetitive mistakes.
- You need to remember project conventions, library quirks, or tool tips.
- You waste time trying to remember what you did in the previous session.
- You work on the same repository with your teammates and need to share decision rationales.

**Use this ESPECIALLY when:**
- Returning to the project after a gap of a few days — context loss is highest at these moments.
- Making a critical architectural decision, the rationale for which will need to be remembered in the future.
- Making the same mistake a second time — this skill exists specifically to prevent this.

**Never skip when:**
- Making "a very small change" — small decisions build up to form a large footprint.
- Saying "I already remember it" — unless you record it, what you think you remember will vanish in the next session.
- Under time pressure — recording takes seconds, while recovering lost context takes minutes.

## Phase 1: Session Start — Context Loading

**In every new session, as the very first step:**

1. **Load the Session Digest** — Read the latest `digest.md` file in the `session-memory/` directory. This file summarizes what was done in the previous session, what decisions were made, and what was left incomplete.
2. **Load the Repo Context Snapshot** — Read `session-memory/last-snapshot.json`. It contains the current branch, modified files, WIP items, and the latest commit information.
3. **Load the Knowledge Base** — Read `session-memory/knowledge-base.md`. It contains accumulated project-specific knowledge (library version quirks, tool errors, conventions).
4. **Verify the Environment** — Does the branch in the snapshot match the current branch? Are the modified files still there? If there is a conflict, notify the user.

```
# Automatic context loading commands (within the shell/agent)
cat session-memory/digest.md 2>/dev/null || echo "No digest yet"
cat session-memory/knowledge-base.md 2>/dev/null || echo "No knowledge base yet"
```

## Phase 2: During Work — Continuous Recording

**While working, record the following events immediately:**

1. **Decision Log** — Record every architectural or design decision in the following format:
   - **Date:** [ISO 8601]
   - **Decision:** What decision was made?
   - **Context:** Why did you make this decision? What were the alternatives?
   - **Consequences:** What are the expected impacts of this decision?
   - **File:** File/directory where the decision was applied.

2. **Mistake Journal** — Record every mistake in the following format:
   - **Date:** [ISO 8601]
   - **Mistake:** What happened?
   - **Root Cause:** Why did it happen?
   - **Fix:** How was it solved?
   - **Prevention:** What will be done to avoid making the same mistake again?

3. **Discovery Log** — Record newly discovered information:
   - **Discovery:** What was learned?
   - **Source:** Where was it learned (documentation, trial, error message)?
   - **Severity:** Low / Medium / High

```
## Decision Log Example
| Date | Decision | Context | Consequences | File |
|-------|-------|--------|----------|-------|
| 2026-05-19 | Use SQLite | Lightweight, embedded, no migration needed | Potential scaling issues | backend/db.py |
```

## Phase 3: Session End — Memory Processing

**Before ending the session, execute the following steps in order:**

1. **Learning Loop** — After completing the last task, answer these questions:
   - What did I learn in this session?
   - What would I do differently next time?
   - Which tool or approach was the most efficient?
   - What information will be useful in the next session?

2. **Repo Context Snapshot** — Save the current state:
   - Current branch name
   - List of modified files (`git diff --name-only`)
   - WIP items (incomplete work)
   - Latest commit message
   - Pending changes (`git status --short`)

3. **Create Session Digest** — Write a concise summary of this session:
   - Actions taken (bulleted list)
   - Decisions made (referenced from the decision log)
   - Mistakes made (referenced from the mistake journal)
   - Incomplete work / next steps

4. **Memory Compaction** — If the decision log, mistake journal, or knowledge base exceeds a certain size (e.g., 50+ records):
   - Summarize old records (preserving their core meaning).
   - Clean up low-severity records.
   - Maintain critical records.
   - Keep a compaction history (when and how many records were compacted).

```
# Creating a snapshot
BRANCH=$(git rev-parse --abbrev-ref HEAD)
FILES=$(git diff --name-only)
STATUS=$(git status --short)
echo "{\"branch\":\"$BRANCH\",\"files\":\"$FILES\",\"status\":\"$STATUS\"}" > session-memory/last-snapshot.json
```

## Phase 4: File Structure

**The session-memory/ directory consists of the following files:**

```
session-memory/
├── digest.md              # Latest session summary (updated at the end of every session)
├── digest-archive/         # Archived older digests
│   ├── digest-2026-05-18.md
│   └── digest-2026-05-17.md
├── last-snapshot.json      # Latest repo state snapshot
├── decision-log.md         # All architectural/design decisions
├── mistake-journal.md      # All mistakes and their fixes
├── knowledge-base.md       # Accumulated project knowledge
├── discovery-log.md        # Discoveries and lessons learned
└── compaction-history.md   # Compaction history (optional)
```

## Phase 5: Final Verification

Before finishing, check:

- [ ] Is there at least one decision recorded in the decision log for this session?
- [ ] Have the mistakes made in this session been recorded in the mistake journal? (If there are no mistakes, is a "no mistakes" note made?)
- [ ] Is the knowledge base updated? (Were newly learned details added?)
- [ ] Is the repo context snapshot up to date? (Branch, files, WIP)
- [ ] Has a session digest been created and is it concise?
- [ ] Have the learning loop questions been answered?
- [ ] Has obsolete/invalid information in the knowledge base been cleaned up?
- [ ] Has compaction been performed if necessary?
- [ ] Are all records timestamped and in ISO 8601 format?
- [ ] Is the digest file clear enough to be read in the next session?

## Red Flags — Stop and Follow Process

If you catch yourself thinking:

- "This session was too short, no need to record" — **There is no minimum threshold for recording. Even a single decision made in a 5-minute session is recorded.**
- "I'll remember it in the next session anyway" — **You won't. Memory lives in a file, not inside your head.**
- "This decision is too trivial, not worth recording" — **Accumulation of seemingly trivial decisions forms the project culture.**
- "Updating the knowledge base is too much work" — **Adding one line of information takes 10 seconds. Re-discovering the same information takes 10 minutes.**
- "I'll do compaction later" — **No, you won't. Memory compaction is part of the session-end routine.**

**ALL of these mean:** STOP. Return to Phase 3 (Session End).

## Signals Your Human Partner Warns You With

**Watch for these redirections:**

- "We talked about this before" — You are discussing the same decision again without checking the decision log. Load past decisions first.
- "You made this mistake before" — You are working without checking the mistake journal. Load mistake records and apply the prevention strategy.
- "What were we doing last session?" — You didn't read the session digest. It is mandatory to load the digest at the start of the session.
- "Why did we make this decision?" — Rationale in the decision log is missing or insufficient. Record the decision's context in more detail.
- "I keep explaining the same thing" — The knowledge base is not up to date. New information is not being added, old information is not being cleaned.

**When you see these:** STOP. Return to Phase 1 (Context Loading) and check the relevant records.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I can find this information again, Googling is enough" | Googling the same page takes 5 minutes, reading your own note takes 5 seconds. |
| "Memory files take up too much space" | 1000 decision records $\approx$ 100KB. Practically nothing alongside the project. |
| "Recording everything is obsessive" | Making the same mistakes continuously is obsessive. Recording is smart. |
| "Compaction leads to loss of meaning" | Summarization technique preserves critical information. You aren't deleting, just condensing. |
| "My teammates don't want this much recording" | Records are for the agent, not for the team. Yet, your teammates will be grateful when they see the rationale for decisions. |
| "Under time pressure, I'll handle it later" | Mistakes made under time pressure are the most expensive mistakes. Recording is protective. |

## Related Skills

- **plan-and-execute** — Use alongside session memory: plans carry over sessions, execution relies on past decisions.
- **code-review** — Decisions in the decision log are used as rationales in code reviews.
- **incident-response** — Records in the mistake journal form the basis for post-incident fixes.
- **context-assembly** — Session digest and snapshot are inputs for context assembly.
- **pr-review-checklist** — Project conventions in the knowledge base feed PR review criteria.

## Self-Audit

After completing the process of this skill:

1. **Coverage Check:** Are the decision log, mistake journal, knowledge base, and snapshot updated in every session? Are any files missing?

2. **Edge Case Check:**
   - Session with no mistakes: Did you add a "no mistakes in this session" note to the mistake journal?
   - Session with no decisions: Not making a decision is also a decision — did you record it as a "continuation decision"?
   - Session crashed/aborted: Can partial records be recovered?
   - First session (no records yet): Was the initial state managed correctly?

3. **Quality Check:**
   - Are decision records understandable when read in the next session?
   - Do records avoid unnecessary detail while not losing critical context?
   - Was the Iron Law followed? (At least one decision, one mistake, and one context record per session)
   - Is the digestion summary clear enough for a new agent (or human) to read and continue?
