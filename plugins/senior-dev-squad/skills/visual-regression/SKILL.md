---
name: visual-regression
description: "Visual regression testing, screenshot comparison, pixel diffing, cross-browser validation. Use when detecting unintended UI changes between builds."
version: 1.0.0
platforms: [linux, macos]
---

# Visual Regression Testing

## What It Does
Implements automated visual regression testing to catch unintended UI changes before they reach production. Takes screenshots of UI components and pages, compares them against approved baselines using pixel-by-pixel and perceptual diffing, and flags visual differences for human review. Integrates with Storybook, Playwright, and CI/CD pipelines to make visual testing a routine part of development.

## Iron Laws (NEVER violate)
1. **Visual tests are functional tests** — A broken layout is a broken feature. Visual regressions are bugs, not cosmetic issues.
2. **Deterministic rendering required** — Visual tests fail if rendering is non-deterministic. Lock fonts, disable animations, mock time/random, use fixed viewport.
3. **Baseline is sacred** — Approved baselines must be version-controlled. Accidental baseline overwrite = all future tests pass against broken UI.
4. **Human reviews every diff** — Automated pixel diffing produces false positives. Every visual change must be reviewed by a human: intentional (approve) or regression (fix).

## Red Flags (STOP immediately)
- **Baseline drift** — Baseline updated without human review → visual regression may have been silently approved
- **Flaky visual tests** — Same screenshot produces different results across runs → non-deterministic rendering; fix root cause
- **Diff inflation** — One change produces diffs across 50 components → component coupling; refactor to isolate visual changes
- **Anti-aliasing noise** — Pixel differences caused by font rendering differences across OS → use perceptual diffing, not pixel-exact

## Common Rationalizations (self-deception)
- "It's just a pixel, nobody will notice" → Pixels accumulate. "Just one pixel" × 50 changes = broken UI.
- "Visual tests are too slow" → Run on changed components only. Storybook + Chromatic make it fast.
- "We'll catch UI bugs in manual QA" → Manual QA catches 30% of visual regressions. Automated catches 95%+.

## When To Use
- Design system or component library with shared UI components
- Responsive web application where layout changes are high-risk
- Cross-browser testing to catch rendering differences
- Preventing CSS refactoring from breaking existing pages
- Mobile app screenshot testing across device sizes

## Human Partner Signals (escalate to human)
- **Design intent unclear** — Visual change could be intentional or accidental → designer review needed
- **Accessibility impact** — Visual change affects readability, contrast, or keyboard navigation → a11y review
- **Cross-browser discrepancy** — Rendering difference between Chrome and Safari → browser-specific fix
- **Baseline conflict** — Two developers approve conflicting baselines → design system conflict resolution

## Pipeline
1. Setup: configure screenshot tool (Playwright, Puppeteer, Storybook + Chromatic) with deterministic settings
2. Baseline: capture initial screenshots for all components/pages; human review and approve
3. Compare: on each PR, capture new screenshots and diff against approved baselines
4. Review: present diffs for human review — approve intentional changes, flag regressions for fix
5. Update: approved changes become new baselines with version history
6. Monitor: track visual regression escape rate (visual bugs reaching production)

## Verification Checklist
- [ ] Rendering is deterministic — fixed viewport, locked fonts, disabled animations, mocked time/random
- [ ] Baselines version-controlled with approval history
- [ ] Visual diff review integrated into PR workflow
- [ ] Perceptual diffing used (not pixel-exact) to handle anti-aliasing differences
- [ ] Cross-browser screenshots captured (Chrome + Firefox + Safari minimum)
- [ ] Responsive breakpoints tested (mobile, tablet, desktop)
- [ ] No flaky visual tests (same input → same screenshot every time)



## Output Schema (MANDATORY)

```markdown
# [Test Type]: [Target]
## Findings
### [ID]: [Title]
**Scenario:** [Given/When/Then]
**Expected:** [What should happen]
**Actual:** [What happens / what could break]
**Severity:** [CRITICAL/HIGH/MEDIUM]
**Fix:** [Concrete fix]
## Summary
- Total findings: N
- By severity: C=, H=, M=
- Coverage: [dimensions/categories covered]
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Happy path only | Misses failures | Test error/edge/empty states |
| Vague scenarios | Not reproducible | Exact Given/When/Then |
| Missing severity | Can't prioritize | CRITICAL/HIGH/MEDIUM on every finding |
| "Fix later" | Never gets fixed | Concrete fix with every finding |
| Single dimension | Blind spots | Cover all categories systematically |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Coverage breadth | 1-2 dimensions | 4-6 | All categories |
| Scenario specificity | Vague | Partial | Exact Given/When/Then |
| Severity accuracy | None | Some | All correctly rated |
| Fix quality | "Fix it" | Partial | Complete fix |
| Reproducibility | Can't reproduce | Hard | Easy to reproduce |

**Pass: 8/10**
## Related Skills
- `test-engineer` — Visual tests are part of the testing pyramid
- `ui-generator` — Generated UI components need visual regression testing
- `accessibility-optimizer` — Visual regression can detect accessibility-impacting changes
- `responsive-layout-engine` — Responsive layouts need cross-breakpoint visual testing
