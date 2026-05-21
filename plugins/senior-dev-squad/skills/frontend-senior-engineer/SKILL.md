---
name: frontend-senior-engineer
description: "Senior React/Next.js: responsive, a11y, states, forms, performance. Use when building or reviewing frontend UI components."
---

# Frontend Senior Engineer

## Overview

Implement UI at a senior engineer quality level. Every component accounts for loading, error, empty, and edge case states. Accessibility is not optional — it's a requirement. Performance is a feature, not an afterthought.

**Core principle:** A COMPONENT IS NOT DONE UNTIL IT HANDLES EVERY STATE. If it only shows the happy path, it's not finished.

## The Iron Law

```
EVERY DATA-FETCHING COMPONENT MUST HANDLE FOUR STATES: LOADING, EMPTY, ERROR, SUCCESS
```

No exceptions. Not for "simple" components. Not when "it's just internal." Not ever.

## When to Use

**Use this when:**
- Implementing UI from a spec + architecture plan
- Reviewing existing frontend code
- Adding new pages, components, or features
- Debugging frontend rendering issues

**Use this ESPECIALLY when:**
- The component seems "too simple for error handling"
- Someone says "we'll add loading states later"
- You're tempted to use `useEffect` for data fetching
- The design only shows the happy path

**Don't skip when:**
- "It's just a demo/prototype" (prototypes become production)
- "The API is internal and always works" (it won't)
- "It's a small component" (small components can fail too)

## The Four States (Mandatory)

```tsx
function ProjectList() {
  const { data, isLoading, error } = useQuery(...)

  // 1. LOADING — Show immediately (no artificial delays)
  if (isLoading) return <ProjectListSkeleton />

  // 2. ERROR — Human-readable + actionable
  if (error) return (
    <ErrorState
      title="Failed to load projects"
      message={error.message}
      action={<Button onClick={refetch}>Try Again</Button>}
    />
  )

  // 3. EMPTY — Informative + next action
  if (!data?.length) return (
    <EmptyState
      title="No projects yet"
      description="Create your first project to get started."
      action={<CreateProjectButton />}
    />
  )

  // 4. SUCCESS — The actual data
  return <ProjectCards projects={data} />
}
```

## Mandatory Checks (Every Component)

### 1. Accessibility (WCAG 2.1 AA)

| Check | Implementation | Why You'll Skip | Reality |
|-------|---------------|-----------------|---------|
| Semantic HTML | `<nav>`, `<main>`, `<button>` not `<div onClick>` | "A div works fine" | Screen readers need semantics |
| Keyboard nav | All interactive elements reachable via Tab | "Everyone uses a mouse" | 1 in 4 users has a motor disability |
| Focus management | Trap focus in modals, return on close | "It's a small modal" | Keyboard users get stuck |
| Color contrast | 4.5:1 text, 3:1 large text | "The brand colors look fine" | 8% of users are colorblind |
| Screen reader | ARIA labels, live regions | "I'll add it later" | You won't. Do it now. |

### 2. Responsive Design

```
Mobile-first CSS (base = mobile, md = tablet, lg = desktop)
Test at: 320px (small phone), 768px (tablet), 1024px (desktop), 1440px (wide)
Touch targets: ≥ 44×44px (WCAG 2.5.5 — thumb zone)
No horizontal scroll at ANY breakpoint
```

### 3. Form Validation Patterns

```tsx
// DO THIS:
// - Validate on blur (not every keystroke)
// - Validate on submit (always)
// - Inline errors next to field
// - Server errors map to correct field
// - Double-submit prevention

const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
  resolver: zodResolver(schema),
})

// DON'T DO THIS:
// - Validation only on submit
// - Alert/Toast for field errors
// - Clear fields on validation error
// - No loading state on submit button
```

### 4. Performance Budget

| Metric | Target | Hard Limit |
|--------|--------|-----------|
| Bundle per page | < 200KB gzipped | 300KB |
| LCP | < 2.5s | 4.0s |
| INP | < 200ms | 500ms |
| CLS | < 0.1 | 0.25 |
| Lighthouse score | > 90 | > 80 |

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll add loading states later"
- "This component is too simple for error handling"
- "The design doesn't show error states, so I'll skip them"
- "useEffect is fine for this one fetch"
- "I don't need to test on mobile"
- "The colors have enough contrast" (without checking)
- "Keyboard navigation works fine" (without testing)

**ALL of these mean: STOP. Handle the missing state first.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "What happens when this fails?" — You didn't handle error state
- "What does it look like on mobile?" — You didn't test responsive
- "I can't tab to this button" — You missed keyboard navigation
- "The colors blend together" — You didn't check contrast

**When you see these:** STOP. Fix the missed state before adding new features.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "I'll add error handling later" | You'll forget. Production will remember for you. |
| "The skeleton is ugly, I'll skip it" | A spinner is worse. Blank screen is worst. |
| "It works on my screen" | Your screen is not the only screen. |
| "This component is internal only" | Internal tools have users too. |
| "useEffect is standard for data fetching" | Not anymore. Use RSC or React Query. |

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

- **spec-first-development** — spec defines all four states
- **test-engineer** — tests verify loading, empty, error states
- **performance-engineer** — measures Core Web Vitals
- **edge-case-hunter** — finds missing mobile/responsive scenarios

## Self-Review (Before PR)

- [ ] Every data-fetching component handles all four states
- [ ] Keyboard navigation tested (Tab through entire flow)
- [ ] Screen reader tested (VoiceOver/NVDA)
- [ ] Tested at 320px, 768px, 1024px, 1440px
- [ ] No `console.log`, no `any`, no unused imports
- [ ] Lighthouse score > 90
- [ ] Form validation: blur + submit + inline errors + double-submit prevention
- [ ] Error boundaries wrap each feature module
