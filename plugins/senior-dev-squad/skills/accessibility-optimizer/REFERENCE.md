# Accessibility Optimizer — Reference

Detailed audit checklists, code patterns, and worked examples for each phase. Linked from [SKILL.md](SKILL.md).

---

## Phase 1: WCAG 2.2 Auditing — Four Principles Scan

**BEFORE proceeding:**

1. **Start Perceivable audit:**
   - Is there a text alternative for all non-text content?
   - Is color not the sole carrier of information?
   - Can content be perceived through different senses?
2. **Start Operable audit:**
   - Are all functions usable via keyboard?
   - Are users given sufficient time?
   - Is there flashing content that could trigger seizures?
3. **Start Understandable audit:**
   - Is the page language defined correctly?
   - Are navigation and interactions consistent?
   - Are error messages explanatory and corrective?
4. **Start Robust audit:**
   - Does the HTML comply with standards?
   - Is ARIA usage correct and meaningful?
   - Is the site compatible with assistive technologies?

```html
<!-- Example: Robust HTML structure -->
<html lang="en">
<head>
  <title>Accessible Page</title>
</head>
<body>
  <header role="banner">
    <nav aria-label="Main navigation">
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/about">About Us</a></li>
      </ul>
    </nav>
  </header>
</body>
</html>
```

---

## Phase 2: Color Contrast Audit

**BEFORE proceeding:**

1. **Test all color combinations** — Calculate text color + background color pairs.
2. **Verify AA level** — 4.5:1 for normal text, 3:1 for large text.
3. **Verify AAA level** — 7:1 for normal text, 4.5:1 for large text.
4. **Verify focus indicators** — Focus ring contrast must be at least 3:1.
5. **Non-text contrast** — At least 3:1 for UI components and graphic elements.
6. **Recommend automatic fixes** — Generate suggestions to darken/lighten colors that do not meet contrast criteria.

```javascript
// Color contrast calculation
function getContrastRatio(hex1, hex2) {
  const l1 = getRelativeLuminance(hexToRgb(hex1));
  const l2 = getRelativeLuminance(hexToRgb(hex2));
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Recommended fixes
const FIXES = {
  primary: { from: '#4A90D9', to: '#2B6CB0', ratio: 4.8 }, // AA ✓
  danger:  { from: '#E53E3E', to: '#C53030', ratio: 4.6 }, // AA ✓
}
```

---

## Phase 3: Keyboard Navigation Audit

**BEFORE proceeding:**

1. **Test tab order** — Do all interactive elements have tab index values in a logical sequence?
2. **Verify focus indicators** — Does every focusable element have a visual focus indicator?
3. **Verify skip links** — Is there a "Skip to content" link at the top of the page?
4. **Verify focus trap** — Does the focus trap work correctly in elements like modals and dialogs? (Must be able to exit via ESC)
5. **Keyboard shortcuts** — Custom keyboard shortcuts using a single letter must be disableable.

```html
<!-- Skip link -->
<a href="#main-content" class="skip-link">Skip to main content</a>

<!-- Focus style -->
<style>
  *:focus-visible {
    outline: 3px solid var(--color-focus);
    outline-offset: 2px;
    border-radius: 2px;
  }
  /* Never use outline: none! */
</style>

<!-- Focus trap (modal example) -->
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
  <button onclick="closeModal()" aria-label="Close">✕</button>
  <!-- Focus is locked here, exited via ESC -->
</div>
```

---

## Phase 4: Screen Reader Audit

**BEFORE proceeding:**

1. **Verify ARIA labels** — Use `aria-label` or `aria-labelledby` for all icons, buttons, and non-text elements.
2. **Verify ARIA roles** — Are `role="banner"`, `role="navigation"`, `role="main"`, `role="complementary"`, etc., used correctly?
3. **Live regions** — Is `aria-live="polite"` or `aria-live="assertive"` used for dynamic content updates?
4. **Alt text** — Is there a meaningful `alt` text for all images? (Use `alt=""` for decorative images)
5. **Heading hierarchy** — Is the h1 → h2 → h3 sequence correct? Are there skipped levels?
6. **Form labels** — Does every form input have a visible `<label>` bound to it?

```html
<!-- Good ARIA usage -->
<button aria-label="Show notifications" aria-expanded="false">
  <span class="icon-bell"></span>
  <span class="badge" aria-live="polite">3</span>
</button>

<!-- Dynamic content with live region -->
<div aria-live="polite" aria-atomic="true" class="toast-container">
  <!-- Notifications are appended here -->
</div>

<!-- Heading hierarchy -->
<h1>Page Title</h1>
  <h2>Section 1</h2>
    <h3>Subsection 1.1</h3>
  <h2>Section 2</h2>
```

---

## Phase 5: Form Accessibility Audit

**BEFORE proceeding:**

1. **Is there a label for each input?** — Check that each input is bound to a visible `<label>` element.
2. **Error messages** — Are errors bound to inputs via `aria-describedby`?
3. **Required indicators** — Are required fields marked with `required` and `aria-required="true"`?
4. **Error announcements** — Are errors announced on form submission via an `aria-live` region?
5. **Autofill** — Are `autocomplete` properties configured correctly?
6. **Error prevention** — Is there a confirmation step (undo/review) for critical operations?

```html
<!-- Accessible form structure -->
<form novalidate aria-label="Contact form">
  <div class="form-group">
    <label for="email">Email address <span aria-hidden="true">*</span></label>
    <input
      type="email"
      id="email"
      name="email"
      required
      aria-required="true"
      aria-describedby="email-error email-hint"
      autocomplete="email"
    />
    <span id="email-hint" class="hint">E.g., user@example.com</span>
    <span id="email-error" class="error" role="alert" aria-live="assertive">
      Please enter a valid email address.
    </span>
  </div>
  <button type="submit">Submit</button>
</form>
```

---

## Phase 6: Motion Sensitivity

**BEFORE proceeding:**

1. **Add `prefers-reduced-motion` media query** — Turn off or minimize all animations.
2. **Make animations disableable** — Turn off properties such as `animation`, `transition`, and `scroll-behavior`.
3. **Parallax and scrolling effects** — Disable when `prefers-reduced-motion` is active.
4. **Autoplay** — Stop/pause autoplaying content such as videos and carousels.
5. **Flashing content** — No content should contain more than 3 flashes in a second (WCAG 2.3.1).

```css
/* Motion sensitivity styles */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  .parallax {
    transform: none !important;
  }

  .carousel {
    scroll-snap-type: none;
  }

  video[autoplay] {
    autoplay: false;
  }
}

/* Option to disable animations completely */
.animations-disabled * {
  animation: none !important;
  transition: none !important;
}
```

---

## Phase 7: Cognitive Accessibility

**BEFORE proceeding:**

1. **Clear language** — Are complex sentences avoided? Are abbreviations explained?
2. **Consistent navigation** — Are navigation structures and sequences identical across all pages?
3. **Error prevention and correction** — Is undo support available for financial or legal operations?
4. **Time limit** — If session timeouts exist, are users warned in advance and can the time be extended?
5. **Help and guidance** — Is there step-by-step guidance for complex forms and operations?
6. **Visual consistency** — Are similar functions represented by similar visual elements?

```html
<!-- Step-by-step form guidance -->
<nav aria-label="Checkout steps" role="progressbar" aria-valuenow="2" aria-valuemin="1" aria-valuemax="4">
  <ol class="steps">
    <li class="step--completed">Enter Details</li>
    <li class="step--active" aria-current="step">Payment Info</li>
    <li class="step--pending">Review</li>
    <li class="step--pending">Completed</li>
  </ol>
</nav>
```

---

## Phase 8: Automated Fixing (Auto-Fix)

**BEFORE proceeding:**

1. **Categorize issues** — Critical (AA violation), Medium (AAA violation), Improvement (suggestion).
2. **Generate corrected code** — Output corrected HTML/CSS/JS for each issue.
3. **ARIA fixes** — Add missing ARIA attributes and correct improper ARIA usage.
4. **Color fixes** — Recommend updated color values that meet contrast requirements.
5. **HTML fixes** — Correct `lang`, `title`, heading hierarchy, and form structures.
6. **Change log** — Explain what changes were made and why.

```diff
--- invalid-form.html
+++ fixed-form.html
@@ -1,9 +1,11 @@
- <form>
-   <input type="text" placeholder="Name" />
+ <form aria-label="User registration form">
+   <label for="name">Name</label>
+   <input type="text" id="name" name="name" autocomplete="given-name" required aria-required="true" />
+   <span class="error" id="name-error" role="alert" aria-live="assertive"></span>
     <button type="submit">Submit</button>
   </form>

--- invalid-color.css
+++ fixed-color.css
@@ -1,2 +1,2 @@
-.text-muted { color: #999999; } /* Contrast: 2.8:1 — FAILED */
+.text-muted { color: #6B7280; } /* Contrast: 4.6:1 — AA PASSED */
```

---

## Phase 9: Self-Review Questions and Legal Compliance

After completing all phases, review these questions before marking the audit complete:

1. **Scope Check:** Have all four principles (Perceivable, Operable, Understandable, Robust) been audited?
2. **AA/AAA Level:** Is at least AA level ensured? Were additional AAA improvements implemented?
3. **Color Contrast Check:** Were all text+background combinations checked? Are non-text elements included?
4. **Keyboard Navigation Check:** Is the tab order logical? Is there any focus trap? Does the skip link work?
5. **Screen Reader Check:** Was at least one pass done with VoiceOver/NVDA? Is ARIA usage correct and sufficient?
6. **Form Accessibility:** Does every input have a label? Are errors announced? Are required fields marked?
7. **Motion Sensitivity:** Is prefers-reduced-motion supported? Is there flashing content?
8. **Zoom Test:** Is the page usable at 200% zoom? Does content not overflow? Are buttons clickable?
9. **Automated Fix Report:** Were detected issues documented and fixed? Are the justifications for changes clear?
10. **Legal Compliance:** Are additional legal requirements (e.g. ADA, European Accessibility Act) met?
