---
name: responsive-layout-engine
description: "Generates responsive layouts with design system tokens for each breakpoint — mobile-first, tablet, desktop, wide screen. Use when building multi-breakpoint UI layouts."
---

# Responsive Layout Engine

## Overview

Responsive Layout Engine generates responsive layouts for all breakpoints using design system primitives. It adopts a mobile-first approach, using grid systems, flexbox, and container queries to construct consistent and maintainable layouts. It also covers advanced features such as print styles, responsive navigation, and content reflow.

**Core principle:** Every layout is built from the smallest screen to the largest using a mobile-first approach; no breakpoint is an afterthought.

## The Iron Law

```
NO LAYOUT CAN BE DEPLOYED WITH ONLY A SINGLE BREAKPOINT GENERATED. ALL BREAKPOINTS (MOBILE, TABLET, DESKTOP, WIDE SCREEN) MUST BE GENERATED SIMULTANEOUSLY AND MOBILE-FIRST.
```

## When to Use

**Use this when:**
- Creating a page layout or restructuring an existing layout
- Adding a new component to the design system
- Fixing broken responsive behavior in an existing UI
- Generating a page that requires a print stylesheet

**Use this ESPECIALLY when:**
- A client says "just build it for desktop, we will handle mobile later"
- Under time pressure, someone says "it just needs to work on one breakpoint for now"
- A designer provides a Figma export for only one breakpoint

**Don't skip when:**
- Developing internal/admin tools where the user base is fixed on desktop
- Generating a static page that will not be responsive (e.g., a poster)

## Phase 1: Reading Design System Tokens

**BEFORE proceeding:**

1. **Discover breakpoint tokens** — Read all breakpoint values from the design system. Usually found under `theme.breakpoints` or `tokens.json`.
2. **Check container query support** — If CSS Container Queries are supported, prefer them over media queries.
3. **Retrieve grid and spacing tokens** — Identify `grid-columns`, `gap`, `padding`, and `margin` tokens.
4. **Check print tokens** — Note print-specific tokens if they exist; otherwise, generate default print styles.

```yaml
# Example breakpoint token structure
breakpoints:
  mobile: 320px
  tablet: 768px
  desktop: 1024px
  wide: 1440px
grid:
  columns: 12
  gap: 16px
container-queries: true
```

## Phase 2: Mobile-First Layout Skeleton

**BEFORE proceeding:**

1. **Set up mobile layout** — Start with a single-column layout. All content flows vertically.
2. **Apply basic flexbox/grid** — Start with the minimum CSS required to work on mobile.
3. **Prioritize content** — Decide what content should be visible on mobile.
4. **Prepare hamburger menu** — Build the structure for the mobile hamburger menu navigation.

```css
/* Mobile-first: single column, hamburger menu */
.layout {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  padding: var(--space-3);
}
```

## Phase 3: Tablet Breakpoint

**BEFORE proceeding:**

1. **Add media query or container query** — Write the query corresponding to the tablet breakpoint.
2. **Transition sidebar + content** — Switch from a single column to a 2-column layout.
3. **Transform navigation from hamburger to top nav** — Show the top navigation bar for tablet.
4. **Configure grid column count** — Structure the tablet version of the 12-column grid.

```css
@container (min-width: 480px) {
  /* or */
  @media (min-width: 768px) {
    .layout {
      display: grid;
      grid-template-columns: 250px 1fr;
    }
    .nav--hamburger {
      display: none;
    }
    .nav--top {
      display: flex;
    }
  }
}
```

## Phase 4: Desktop Breakpoint

**BEFORE proceeding:**

1. **Evaluate the holy grail layout** — Is the header, sidebar (left), content (center), sidebar (right), footer structure appropriate?
2. **Set up dashboard grid** — Create a flexible grid system for dashboard pages.
3. **Configure card grid** — Set up a responsive grid for card lists using auto-fill/auto-fit.
4. **Content reflow** — Reorder content on desktop, show new content, avoid hiding necessary content.

```css
@media (min-width: 1024px) {
  .dashboard-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: var(--space-6);
  }
  .content {
    order: 2;
  }
  .sidebar-right {
    display: block;
  }
}
```

## Phase 5: Wide Screen Breakpoint

**BEFORE proceeding:**

1. **Enforce maximum width limit** — Use `max-width` to prevent content from becoming unreadable on very wide screens.
2. **Visual enhancement** — Add additional visual elements or background graphics on wide screens.
3. **Multi-column support** — Split content text into multiple columns using CSS columns.
4. **Large card grid** — Increase card sizes and column count.

```css
@media (min-width: 1440px) {
  .container {
    max-width: 1440px;
    margin: 0 auto;
  }
  .card-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
```

## Phase 6: Responsive Navigation

**BEFORE proceeding:**

1. **Navigation transition** — Test hamburger → Top nav → Sidebar transitions across all breakpoints.
2. **Active page indicator** — Ensure the active page is visually indicated in all states.
3. **Submenus** — Make submenus responsive using dropdown or accordion structures.
4. **Keyboard accessibility** — Verify the navigation is fully navigable using a keyboard.

```javascript
// Navigation transformation logic
const breakpoint = window.matchMedia('(min-width: 768px)');
if (breakpoint.matches) {
  showTopNav();
} else {
  showHamburgerNav();
}
```

## Phase 7: Content Reflow and Images

**BEFORE proceeding:**

1. **Content ordering** — Reorder content using CSS `order` or grid `order`.
2. **Hiding/showing** — Use `display: none` and `visibility` to define what content appears at which breakpoint.
3. **Image loading** — Configure responsive images using the `<picture>` element and `srcset`.
4. **Lazy loading** — Add `loading="lazy"` for images or implement advanced lazy loading using `IntersectionObserver`.

```html
<picture>
  <source media="(min-width: 1024px)" srcset="hero-desktop.webp">
  <source media="(min-width: 768px)" srcset="hero-tablet.webp">
  <img src="hero-mobile.webp" alt="Description" loading="lazy">
</picture>
```

## Phase 8: Print Styles

**BEFORE proceeding:**

1. **Print media query** — Create a `@media print` block.
2. **Hide unnecessary elements** — Navigation, sidebars, ads, and interactive elements should be hidden in print.
3. **Font and color settings** — Remove background colors and make colors compatible with black-and-white printing.
4. **Page breaks** — Control content sections using `page-break-before` and `page-break-after`.
5. **Link URLs** — Display URLs next to anchor links.

```css
@media print {
  nav, .sidebar, .ads, .interactive {
    display: none !important;
  }
  body {
    font-size: 12pt;
    color: #000;
    background: #fff;
  }
  a[href]::after {
    content: " (" attr(href) ")";
  }
}
```

## Phase 9: Performance Optimizations

**BEFORE proceeding:**

1. **CSS code splitting** — Create separate CSS files for each breakpoint or structure layered CSS with `@layer`.
2. **Inline critical CSS** — Inline mobile-first critical CSS inside the `<head>`.
3. **Route-based splitting** — Split code on a per-page basis (lazy loading routes).
4. **Image optimization** — Use WebP/AVIF formats, size appropriately, and lazy load.
5. **Prevent layout shift** — Specify image and content dimensions in CSS (improve CLS).

```html
<!-- Inline critical CSS -->
<style>
  .layout { display: flex; flex-direction: column; gap: 16px; }
</style>
<link rel="stylesheet" href="/css/tablet.css" media="(min-width: 768px)">
<link rel="stylesheet" href="/css/desktop.css" media="(min-width: 1024px)">
```

## Phase 10: Final Verification

**BEFORE checking off:**

- [ ] All breakpoints (mobile, tablet, desktop, wide) have been tested and visual integrity is verified.
- [ ] Mobile-first approach is verified (styles flow from smaller to larger).
- [ ] Navigation is functional and accessible across all breakpoints.
- [ ] Content reflow works as expected.
- [ ] Container queries work properly (if used).
- [ ] Print styles render as expected.
- [ ] Images are responsive and optimized.
- [ ] Cumulative Layout Shift (CLS) is below 0.1.
- [ ] Lazy loading and code splitting work correctly.
- [ ] Keyboard navigation is flawless across all breakpoints.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "Let's build desktop first, we can add media query overrides for mobile later" — THIS IS A MOBILE-FIRST VIOLATION. Go back to the beginning.
- "We don't need a tablet breakpoint, most people use phones or computers anyway" — Tablet users cannot be ignored.
- "No need for print styles, nobody prints web pages" — Print styles are a standard of accessibility and professionalism.
- "A hamburger menu works everywhere, let's just use that" — Harming user experience on wide screens is unacceptable.
- "We'll optimize CSS later, as long as it works for now" — Performance is built into the foundation, not tacked on later.

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "This page looks broken on phones" — You proceeded without testing breakpoints. Go back to Phase 2.
- "The content on the right shifted out of bounds on tablets" — You skipped content reflow. Go back to Phase 3.
- "The menu doesn't work" — You skipped testing navigation transitions. Go back to Phase 6.
- "This button is not clickable on mobile" — You forgot to check touch target sizes.
- "Printing ruins the entire page layout" — You forgot print styles. Go back to Phase 8.
- "The page contents jump around as it loads" — You skipped layout shift prevention (missing image sizes). Go back to Phase 9.

**When you see these:** STOP. Return to relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Let's do desktop first, then handle mobile" | Not mobile-first. Desktop-to-mobile conversion is always harder and more error-prone. |
| "This page is too simple to need responsiveness" | Even the simplest page breaks on different screens. Simple pages must be responsive. |
| "Container queries are too complex, media queries are enough" | Container queries enforce component-level thinking and produce far more modular code. |
| "Print styles are a legacy feature" | Legal documents, recipes, and articles are still printed. It remains an accessibility standard. |
| "No time, let's launch with a single breakpoint" | Making a non-responsive site responsive later costs 2-3x more than doing it right from the start. |

## Related Skills

- **accessibility-optimizer** — Should be run after every layout design to ensure responsive navigation and content are accessible.
- **component-library-generator** — Generates components using responsive primitives to be used in layouts.
- **design-system-extractor** — Used before layout design to extract design system tokens (breakpoints, grid, spacing).
- **performance-auditor** — Used after layout design to verify CSS size, layout shift, and lazy loading performance.

## Self-Review

After completing this skill's process:

1. **Scope Check:** Have you covered all breakpoints (mobile, tablet, desktop, wide) and print styles?
2. **Mobile-First Check:** Are all media queries written with `min-width` (small to large)? Are there any `max-width` desktop-first overrides?
3. **Edge Case Check:** Have you tested very small screens (under 320px), very large screens (2560px+), landscape mobile, and tablet orientation transitions?
4. **Navigation Check:** Do all navigation states (hamburger → top nav → sidebar) work seamlessly?
5. **Performance Check:** Is CSS size optimized? Is critical CSS inlined? Are there unnecessary media query overrides?
6. **Layout Shift (CLS) Check:** Is there layout shift caused by image sizes, font loading, or dynamic content?
7. **Accessibility Check:** Is keyboard navigation, touch target sizing (min 44px), and zoom support ensured across all breakpoints?
8. **Print Check:** Do print styles show all content properly? Are navigation, sidebars, and ads hidden?

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
