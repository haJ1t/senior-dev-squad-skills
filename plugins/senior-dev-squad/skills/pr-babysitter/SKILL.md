---
name: pr-babysitter
description: "PR monitoring, CI error correction, review replying, merge conflict resolution, and rebase management. Use when managing an open PR through to merge."
---

# PR Babysitter

## Overview

A Pull Request observer and automated caretaker. It monitors open PRs, interprets CI build failures, replies to review comments, resolves merge conflicts, and ensures PRs remain in a mergeable state. This allows human developers to focus on writing code instead of managing PR logistics.

**Core principle:** EVERY OPEN PR REQUIRES MAINTENANCE. A PR must not sit idle while its CI is red, should not remain unmerged when conflicts exist, and review comments must never go unanswered.

## The Iron Law

```
BEFORE CLOSING A PR (EITHER VIA MERGING OR CLOSING): THE CI MUST BE GREEN, ALL REVIEWS MUST BE ANSWERED, AND ALL CONFLICTS MUST BE RESOLVED.
```

## When to Use

**Use this when:**
- There are 5+ open PRs in a repository, and tracking CI cycles becomes overwhelming.
- Reviews are arriving but left unanswered (causing a backlog of pending PRs).
- Merge conflicts occur frequently, and resolving them manually wastes developer time.
- CI fails sporadically, requiring root cause and pattern analysis.

**Use this ESPECIALLY when:**
- The team lacks dedicated human resources for PR maintenance.
- All PRs must be green before a major release (feature freeze).
- Development is occurring concurrently across multiple feature branches.

**Don't skip when:**
- "There is only one open PR" — even a single PR requires maintenance and status checking.
- "CI rarely breaks" — prompt intervention when it does break makes a significant difference.

## Phase 1: PR Discovery and Status Assessment

**BEFORE proceeding:**

1. **Scan open PRs** — List all open PRs in the repository (checking their status, target branch, and labels).
2. **Generate a status report for each PR:**
   - CI pipeline status (Success/Failure/Pending).
   - Review status (Approved/Changes Requested/Awaiting Review).
   - Merge conflict status (Is there a conflict?).
   - Git lag (How many commits behind the target branch?).
3. **Prioritize work** — Prioritize red CI failures > active conflicts > rebase requirements.

```bash
# List open PRs with GitHub CLI
gh pr list --state open --json number,title,headRefName,baseRefName,statusCheckRollup,reviews,mergeable

# View details for a specific PR
gh pr view <PR_NUMBER> --json body,comments,statusCheckRollup,reviews,mergeable,additions,deletions
```

## Phase 2: CI Failure Analysis and Automated Fixes

**BEFORE proceeding:**

1. **Examine CI logs** — Pinpoint the failing job and extract the exact error.
2. **Classify the error:**
   - **Test Failure:** Assertion failed, timeout, or flaky test behavior.
   - **Compilation Error:** Syntax error, import mismatch, or type mismatch.
   - **Linting/Formatting Error:** Code style guide violation or formatting issue.
   - **Configuration Error:** Missing environment variables or dependency resolution issue.
3. **Determine the correction strategy:**
   - Test Failure → Analyze code logic and apply a patch.
   - Linting Failure → Run the automated formatter.
   - Compilation Failure → Fix the source syntax/imports.
4. **Apply and push the fix** — Commit directly to the PR branch.

```bash
# View CI run logs
gh run view <RUN_ID> --log --job <JOB_NAME>

# Commit and push after applying the fix
git add -A && git commit -m "fix: resolve CI failure - [error description]"
git push origin <PR_BRANCH>
```

## Phase 3: Replying to and Implementing Reviews

**BEFORE proceeding:**

1. **Scan pending reviews** — Read all comments categorized as "changes requested" or generic feedback.
2. **Define an action for each comment:**
   - **Code change required:** Apply the fix, then reply confirming the correction.
   - **Explanation required:** Clarify why the code was written this way and discuss alternatives.
   - **Already addressed:** Reply stating "this has been resolved in commit [SHA]."
3. **Resolve review threads** — Close conversations on GitHub once resolved.
4. **Re-request review** — Tag reviewers for a re-review when all items are addressed.

```bash
# Retrieve PR review comments
gh pr view <PR_NUMBER> --json comments --jq '.comments[] | {body, author, path, position}'

# Reply to a review comment
gh pr comment <PR_NUMBER> --body "Fixed: [explanation]. Commit: [SHA]"

# Re-request review
gh pr review <PR_NUMBER> --request-reviewer <REVIEWER>
```

## Phase 4: Merge Conflict Resolution

**BEFORE proceeding:**

1. **Identify conflict files** — Pinpoint which files and specific lines are conflicting.
2. **Analyze the source of the conflict:**
   - Changes introduced in our PR branch.
   - Changes merged into the target branch.
3. **Select a resolution strategy:**
   - **Simple Conflict:** Appending lines within the same function → Preserve both changes.
   - **Same-Line Conflict:** Both branches modified the exact same line → Perform intent analysis.
   - **File Deleted/Moved:** A file was deleted or moved in one branch → Use the new location and update references.
4. **Use merge tools** (`git merge-file`, `git merge-tree`) or resolve the conflicts manually.
5. **Verify the conflict resolution** — Ensure the codebase compiles and all tests pass post-resolution.

```bash
# Fetch target branch updates
git fetch origin <TARGET_BRANCH>

# Resolve conflict via rebase (recommended)
git rebase origin/<TARGET_BRANCH>
# If conflicts occur, edit the files, stage them, and continue
git add <RESOLVED_FILES>
git rebase --continue

# Resolve conflict via merge (alternative)
git merge origin/<TARGET_BRANCH>
# Edit files to resolve conflicts, stage, and commit
git add <RESOLVED_FILES>
git merge --continue
```

## Phase 5: Rebase and Branch Updates

**BEFORE proceeding:**

1. **Calculate lag behind target branch:** `git rev-list --count HEAD..origin/<target>`
2. **Threshold check:** If the branch is 10+ commits behind or has overlapping changes, perform a rebase.
3. **Rebase strategy:**
   - **Standard Rebase:** Move the PR branch to the tip of the target branch.
   - **Interactive Rebase:** Reorganize the last N commits (squashing or fixing up where appropriate).
4. **Force push post-rebase** — Run `git push --force-with-lease` on the PR branch.

```bash
# Rebase and push
git fetch origin <TARGET_BRANCH>
git rebase origin/<TARGET_BRANCH>
git push --force-with-lease origin <PR_BRANCH>
```

## Phase 6: Status Reporting and Merge Decisions

**BEFORE proceeding:**

1. **Generate a PR status summary:**
   - CI status (Have all checks passed?).
   - Review status (How many approvals vs. changes requested?).
   - Conflict status (Are there unresolved conflicts?).
   - Branch synchronicity (Is the branch up to date with target?).
   - Last activity time.
2. **Merge decision logic:**
   - CI green + Approved + No conflicts → Merge automatically (or add to the merge queue).
   - CI green + Awaiting approval → Wait for reviewers.
   - CI red → Return to Phase 2.
   - Unresolved conflicts → Return to Phase 4.
3. **Select the merge strategy:**
   - **Squash Merge:** Best for small, single-commit changes.
   - **Merge Commit:** Best for larger feature branches.
   - **Rebase Merge:** Best for maintaining a clean, linear git history.

```bash
# View PR summary
gh pr view <PR_NUMBER> --json title,state,mergeable,reviews,statusCheckRollup,headRefName,baseRefName

# Merge the PR if conditions are met
gh pr merge <PR_NUMBER> --squash --subject "feat: PR title" --body "PR description"
```

## Phase 7: Final Verification

Before marking complete:

- [ ] All open PRs have been scanned and a status summary generated.
- [ ] Fixes have been committed for all PRs with failing CI, and runs have been re-triggered.
- [ ] All review comments have been answered (resolved or explained).
- [ ] All merge conflicts have been resolved.
- [ ] Branches are fully synchronized with their target branches (rebased if necessary).
- [ ] Eligible PRs have been merged or queued.
- [ ] Blocked PRs are labeled with their blockers (e.g., review pending, CI red).

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "This CI failure is probably flaky; it will pass if I just re-run it" — Flaky tests have root causes; analyze the failure.
- "This review comment is minor, I don't need to respond" — Every review thread must be formally answered or resolved.
- "This conflict is too complex; I will just fix it manually on the fly" — Use structured git tools to minimize human error.
- "Rebase is overkill; a merge commit is fine" — Linear history and clean git logs are key to project health.
- "Let's merge this quickly and let CI complete later" — NEVER merge a PR with a failing or incomplete CI run.

**ALL OF THESE MEAN: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Why didn't you re-trigger the failing CI run?" — You skipped checking CI logs. Return to Phase 2.
- "You didn't reply to the reviewer's feedback" — You skipped review comments. Return to Phase 3.
- "The conflict resolution broke the build" — You failed to verify the resolution. Return to Phase 4.
- "This branch is way out of sync with the base" — You skipped updating the branch. Return to Phase 5.
- "You merged with a failing CI run!" — You skipped final status verification. Return to Phase 7.

**When you see these:** STOP. Return to the relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "CI failed, but it's probably not my code." | Every failure must be investigated; ignoring failures introduces instability. |
| "It's just a tiny conflict, resolving it manually in the editor is fine." | Manual conflict resolution without verifying compilation often breaks builds. |
| "The reviewer only asked a question; no action needed." | Questions require answers, or the PR will remain blocked. |
| "A merge commit is easier than rebasing." | Merge commits clutter commit history; rebases maintain a clean commit trail. |
| "I'll merge now and fix any issues directly on master." | Master/main should always be green; merging broken code violates core safety rules. |

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

- **code-reviewer** — To better analyze and address incoming review feedback.
- **test-engineer** — To troubleshoot flaky tests and fix CI check runs.
- **devops-release-engineer** — For CI/CD configuration management.
- **edge-case-hunter** — To locate subtle bugs introduced during conflict resolution.

## Self-Review

After completing this process:

1. **Verification Check:** Have you checked all open PRs and their current CI statuses?
2. **Resolution Check:** Are all conflicts resolved and verified to compile?
3. **Communication Check:** Have all comments been addressed and re-reviews requested?
