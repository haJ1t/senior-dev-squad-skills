---
name: design-system-manager
description: "Design system catalog, comparison, setup, theming, migration across 72+ systems. Use when selecting, adopting, or migrating a design system."
---

# Design System Manager

## Overview

Instead of writing a design system from scratch for every project, this skill catalogs and matches 72+ open-source design systems based on project type, and guides you through every step from initial setup to theming and migration. Adhering to the Open Design approach (e.g., nexu-io/open-design — 46K★), it manages component inventory, design tokens, framework adapters, accessibility compliance, bundle size, license compatibility, and dark mode support from a single source.

**Core principle:** SELECTING A DESIGN SYSTEM IS NOT JUST A TECHNICAL DECISION — IT IS THE INTERSECTION OF PRODUCT, PERFORMANCE, TEAM, AND LICENSE STRATEGY. IT MUST NEVER BE CHOSEN ARBITRARILY.

## The Iron Law

```
SELECT EXACTLY ONE DESIGN SYSTEM FOR EVERY PROJECT. IF YOU MUST MIGRATE LATER, ENSURE YOU HAVE A DOCUMENTED MIGRATION PLAN.
```

Never say "let's throw in Bootstrap now, we'll migrate to shadcn/ui later." Without calculating migration costs, token structures, theme APIs, and component compatibility upfront, half the project will end up being rewritten.

## When to Use

**When it must be used:**
- Starting a new web application — undecided on which design system to choose.
- Integrating a design system into an existing project — setup, provider wrappers, global styles.
- The team is considering migrating between multiple design systems — requires a migration plan.
- The current design system no longer scales with the project — time to re-evaluate.
- The project is failing to meet accessibility (WCAG) or performance targets due to the current system.

**ESPECIALLY when:**
- Someone says "let's quickly drop in Bootstrap and figure it out later" — never proceed without a migration plan.
- There are arguments between designers and developers like "why does this component look different?" — indicating a token mismatch.
- The project spans both web and mobile applications — cross-platform compatibility is critical.
- A new frontend developer joins the team and onboarding is difficult — due to missing documentation.

**Never skip when:**
- "It's just a 3-page landing page" — even small projects have accessibility and performance goals.
- "It's an internal tool, visuals don't matter" — internal tools have users too; consistency and accessibility are required everywhere.

## Workflow

Work through the six phases in order. Each gate must be confirmed before proceeding.

**Phase 1 — Scan the catalog.** Identify project type, framework, team size, performance budget, and WCAG target. See [REFERENCE.md](REFERENCE.md) for the full catalog of 72+ design systems organized by category.

**Phase 2 — Select.** Pick the top 3 candidates using the project-type mapping, then eliminate via bundle size, WCAG level, dark mode support, and license. See [REFERENCE.md](REFERENCE.md) for all four comparison tables (project-type map, bundle sizes, WCAG levels, dark mode, license matrix).

**Phase 3 — Install and configure.** Confirm Phase 1-2 are done, verify framework version requirements, and check for existing systems that need a transition plan. See [REFERENCE.md](REFERENCE.md) for per-system install commands and provider wrapper patterns.

**Phase 4 — Theme and tokens.** Collect the brand kit (color palette, typography, spacing, border radius) and map values to the chosen system's token API. See [REFERENCE.md](REFERENCE.md) for the cross-system token mapping table and theme customization code for MUI, Chakra, Ant Design, Mantine, and DaisyUI, including dark mode wiring.

**Phase 5 — Component inventory.** List every component the project needs, identify gaps in the chosen system, and size the effort to build any missing components. See [REFERENCE.md](REFERENCE.md) for the full component comparison matrix (19 component types across 6 systems).

**Phase 6 — Migration plan (if applicable).** Choose Big Bang, Gradual, or Strangler Fig based on project size. See [REFERENCE.md](REFERENCE.md) for strategy descriptions, a worked Bootstrap → Mantine example, and a token migration mapping table.

## Red Flags — STOP and Follow Process

If you find yourself rationalizing like this, STOP:

- "Let's just use Bootstrap because everyone knows it" — Familiarity is good, but it might not suit the actual project requirements.
- "MUI is heavy, but we don't care about performance yet" — Bundle size budgets must be determined at the start, not as an afterthought.
- "shadcn/ui is copy-paste, we can modify it however we want" — True, but it makes downstream updates and syncs manual and conflict-prone.
- "Carbon is too corporate, we're a startup" — If scalability is in your roadmap, starting with a robust primitive library pays off.
- "No need to check licenses, they're all open source" — Ant Design is Apache 2.0, Primer is MIT, but Oracle Redwood uses custom enterprise restrictions.
- "We'll add dark mode later" — Selecting a system without native dark mode makes adding it later up to 30% more expensive.
- "Migrating is easy, all systems do the same thing" — Token structures, props APIs, and state mechanisms are radically different.
- "This system is tailored for a specific region, it won't fit us" — Ant Design is fully global, with exhaustive English documentation.

**ANY OF THESE MEAN: STOP. Go back to the selection phase and justify decisions with data.**

## Common Rationalizations

| Rationalization | Reality |
|-----------------|---------|
| "Everyone uses Bootstrap, it's the standard." | Bootstrap is popular but not universally optimal. A complex data dashboard is better served by MUI or Ant Design. |
| "Bundle size doesn't matter; everyone has fast connections." | At least 15% of global users operate on constrained mobile networks. Every kilobyte counts. |
| "We will implement dark mode later." | Retrofitting dark mode onto a design system that doesn't support it natively can require rewriting up to 30% of your frontend. |
| "Migrating is easy since the concepts are identical." | MUI to Mantine: Token architectures, API properties, state hooks, and Providers are completely different. Expect a 2-4 week effort. |
| "There's no need to analyze licenses." | Permissive licenses like MIT, Apache 2.0, and BSD have distinct conditions regarding patents and liabilities. Enterprise usage requires compliance. |
| "This is a small project, no design system needed." | Small projects grow. Failing to implement tokens and modular components early makes refactoring painful within 6 months. |
| "shadcn/ui is copy-paste, so updates aren't an issue." | Custom component overrides make subsequent automatic updates via CLI highly prone to merge conflicts. |
| "Ant Design is only for Chinese regional projects." | Ant Design is developed by global contributors, fully localized to English, and deployed in enterprise apps worldwide. |
| "Carbon is an IBM product, so we'll be vendor-locked." | Carbon is fully open-source (MIT/BSD-licensed) with massive community contributions. IBM dependency is non-existent. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these feedback indicators:**

- "Why does this button look different on another page?" — Mismatched theme instances or inconsistent token overrides.
- "Are we adding another design system to the bundle?" — Attempting to combine systems without an isolation or coexistence strategy.
- "Why did we select this library?" — You skipped the systematic selection process and failed to document a data-driven justification.
- "Why is this essential component missing?" — You did not verify the component inventory ahead of time.
- "Why is the initial page load so slow?" — You failed to verify bundle sizes.
- "Screen readers cannot focus this button" — Accessibility defaults were not audited.
- "Are we allowed to use this commercially?" — You skipped the licensing audit.

**When you receive these signals:** STOP. Return to the relevant phase: decision validation, component inventory, bundle auditing, or licensing verification.

## Related Skills

- **backend-senior-engineer** — To implement high-quality APIs feeding the frontend components.
- **spec-first-development** — To draft comprehensive design system integration specs.
- **performance-engineer** — To audit bundle sizes, LCP/CLS metrics, and critical render paths.
- **edge-case-hunter** — To intercept component behavioral anomalies and responsive layout breaks.

## Verification

After completing this process, verify:

1. **Scope Check:** Does the selected design system meet all project requirements (components, tokens, dark mode, a11y, performance, licensing)?
2. **Justification Check:** Can you defend the design system choice using comparative data rather than superficial popularity?
3. **Migration Check:** Is a gradual coexistence strategy mapped out if migrating from a legacy stack?
4. **Edge Case Check:** Is there a fallback strategy for component requirements that the selected system does not natively cover?
5. **Team Alignment:** Is the choice communicated clearly with developer onboarding documentation ready?

Final checklist before marking complete:

- [ ] Selected design system aligned with project type, team size, and scalability goals.
- [ ] License compatibility verified (especially for enterprise commercial use).
- [ ] Bundle size fits within the project's performance budget.
- [ ] Accessibility targets (WCAG AA/AAA) met by the default component primitives.
- [ ] Dark mode support fully matching design system requirements.
- [ ] All critical component types available; gaps have a fallback plan.
- [ ] Provider wrapper and global stylesheet configured correctly.
- [ ] Theme tokens customized to match the brand kit.
- [ ] For migrations: coexistence layer functional and cleanup timeline defined.
- [ ] Quickstart onboarding document written for team integration.
- [ ] Designers and developers notified and aligned on the choice.
