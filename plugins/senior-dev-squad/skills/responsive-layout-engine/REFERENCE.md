# Responsive Layout Engine — Reference

Detailed phase steps, breakpoint/grid tables, CSS/HTML/JS code samples, and worked examples. Linked from [SKILL.md](SKILL.md).

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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

---

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
