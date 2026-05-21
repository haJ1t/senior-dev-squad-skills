---
name: brand-to-design
description: "Brand identity to design tokens, color, typography, spacing, shadow conversion. Use when translating brand guidelines into a token-based design system."
---

# Brand-to-Design: Transforming Brand Identity into Design System Tokens

## Overview

This skill takes brand identity documents from branding-generator and transforms them into full-fledged design system tokens (color palettes, typography scales, spacing systems, shadow tokens, animation curves, dark mode overrides). It bridges the gap between strategic branding decisions and UI implementation. Outputs can be exported to any target system (MUI, Chakra, Tailwind, CSS custom properties).

**Core principle:** Every decision in the brand identity must have a traceable counterpart in the design tokens — no brand characteristic should get lost in the "interpretation" layer.

## The Iron Law

```
EVERY BRAND COLOR, TYPOGRAPHY DECISION, AND SPACING PREFERENCE MUST BE CONVERTED INTO A DESIGN SYSTEM TOKEN BEFORE THE PROCESS IS CONSIDERED COMPLETE. NO TOKEN IS GENERATED WITHOUT WCAG CONTRAST VERIFICATION.
```

## When to Use

**Use this when:**
- When receiving a new brand identity output from branding-generator
- When migrating an existing brand to a new design system
- When updating all tokens during a rebranding process
- When creating source tokens to be used with design-token-mapper

**Use this ESPECIALLY when:**
- "The brand kit is ready, the designer will extract tokens manually" — automate the process, eliminate human error
- "Colors are set, the developer will handle the rest" — provide all tokens ready without requiring interpretation by the developer

**Don't skip when:**
- If you are starting with only 2-3 colors and a font — even if it seems incomplete, the entire system (50-900 palette, typography scale, spacing system) can be derived
- "We don't need this many tokens, it's a small project" — consistency is independent of project scale; token standardization in small projects saves massive time down the road

## Phase 1: Collecting and Verifying Brand Inputs

**BEFORE proceeding:**

1. **Obtain branding-generator output** — read the brand decisions in JSON or YAML format
2. **Check required fields:**
   - Colors: primary, secondary, accent (hex or HSL)
   - Typography: font family/font stack, body and heading sizes
   - Spacing preference: base unit (4px, 8px, 12px) or a term like "compact"/"comfortable"
3. **Identify missing fields** — if brand personality (rounded/sharp, modern/classic) is missing, assign a default and flag it
4. **Note optional fields:** shadow density, animation style, border radius preference

```yaml
# Example input structure (branding-generator output)
brand:
  colors:
    primary: "#3B82F6"
    secondary: "#8B5CF6"
    accent: "#F59E0B"
    neutral: "#6B7280"
  typography:
    font_family_heading: "Inter, sans-serif"
    font_family_body: "Inter, sans-serif"
    base_size: "16px"
    scale_ratio: 1.25  # Major Second
  spacing:
    base_unit: 8
    density: "comfortable"
  personality:
    shape: "rounded"
    shadow: "soft"
    animation: "playful"
```

## Phase 2: Color System — Generating the Full Palette

**BEFORE proceeding:**

1. **Generate a 50-900 scale for each brand color:**
   - For primary, secondary, accent, and neutral colors
   - 10 shades ranging from 50 (lightest) to 900 (darkest)
   - Use a color blending algorithm (HSL manipulation or color matrix)
2. **Derive surface/background colors:**
   - background (derived from primary or close to white)
   - surface (derived from secondary)
   - surfaceVariant (derived from neutral)
3. **Derive text colors:**
   - onBackground, onSurface, onPrimary, onSecondary, onAccent
   - Normal and muted variants for each
4. **Determine state colors:**
   - success, warning, error, info — derive from brand colors or select from the accent palette

```css
/* Example Output: CSS Custom Properties */
:root {
  /* Primary Palette */
  --color-primary-50: #EFF6FF;
  --color-primary-100: #DBEAFE;
  --color-primary-200: #BFDBFE;
  --color-primary-300: #93C5FD;
  --color-primary-400: #60A5FA;
  --color-primary-500: #3B82F6;
  --color-primary-600: #2563EB;
  --color-primary-700: #1D4ED8;
  --color-primary-800: #1E40AF;
  --color-primary-900: #1E3A8A;

  /* Semantic Colors */
  --color-success: #10B981;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  /* Surface & Text */
  --color-background: #FFFFFF;
  --color-surface: #F3F0FF;
  --color-on-background: #111827;
  --color-on-surface: #1F2937;
  --color-on-primary: #FFFFFF;
}
```

## Phase 3: Typography System

**BEFORE proceeding:**

1. **Create type scale:**
   - Use the brand's base_size and scale_ratio values
   - At least 7 levels: xs, sm, base, lg, xl, 2xl, 3xl
   - Responsive sizing: separate scale values for mobile and desktop
2. **Define font weights:**
   - regular (400), medium (500), semibold (600), bold (700)
3. **Determine line heights:**
   - Heading: tighter (1.1-1.2), body: normal (1.5), code: monospace (1.4)
4. **Assign letter spacing:**
   - Tighter for headings (-0.02em), normal for regular text

```css
/* Example typography tokens */
:root {
  --font-family-heading: 'Inter', sans-serif;
  --font-family-body: 'Inter', sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;

  /* Desktop Scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;

  /* Mobile Scale */
  --text-xs-mobile: 0.75rem;
  --text-2xl-mobile: 1.25rem;
  --text-3xl-mobile: 1.5rem;

  --font-weight-regular: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.15;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.75;
}
```

## Phase 4: Spacing System

**BEFORE proceeding:**

1. **Generate spacing scale using the base unit:**
   - 0, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8, 10, 12 (in units)
   - Each unit = base_unit × value (e.g. 8px × 3 = 24px)
2. **Adjust based on density mode:**
   - "compact": base_unit / 2 or base_unit × 0.75
   - "comfortable": base_unit × 1 or base_unit × 1.25
3. **Add semantic spacing tokens:**
   - spacing-section, spacing-card, spacing-element, spacing-gap

```css
/* Example spacing tokens (base: 8px) */
:root {
  --spacing-0: 0px;
  --spacing-0_5: 4px;
  --spacing-1: 8px;
  --spacing-1_5: 12px;
  --spacing-2: 16px;
  --spacing-3: 24px;
  --spacing-4: 32px;
  --spacing-5: 40px;
  --spacing-6: 48px;
  --spacing-8: 64px;
  --spacing-10: 80px;
  --spacing-12: 96px;

  /* Semantic */
  --spacing-section: var(--spacing-12);
  --spacing-card: var(--spacing-4);
  --spacing-element: var(--spacing-2);
  --spacing-gap: var(--spacing-3);
}
```

## Phase 5: Shadows, Border Radius, and Animations

**BEFORE proceeding:**

1. **Create shadow system:**
   - Determine density based on brand personality ("soft": low opacity, "hard": high opacity)
   - At least 3 levels: sm, md, lg (and optionally xl, 2xl)
   - Specify x, y, blur, spread, color for each level
2. **Create border radius:**
   - "rounded": high radius values (8px-16px)
   - "sharp": low radius values (0-4px)
   - "mixed": combination
   - Levels: none, sm, md, lg, xl, full
3. **Create animation tokens:**
   - Timing: "playful" → ease-out-bounce, "professional" → ease-in-out
   - Duration: fast (150ms), normal (300ms), slow (500ms)
   - Easing curves: CSS cubic-bezier values

```css
/* Example effect tokens */
:root {
  /* Shadows (soft personality) */
  --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1), 0 4px 6px -4px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.1);

  /* Border Radius (rounded) */
  --radius-none: 0px;
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;

  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
  --easing-playful: cubic-bezier(0.34, 1.56, 0.64, 1);
  --easing-professional: cubic-bezier(0.4, 0, 0.2, 1);
  --easing-enter: cubic-bezier(0, 0, 0.2, 1);
  --easing-exit: cubic-bezier(0.4, 0, 1, 1);
}
```

## Phase 6: Dark Mode Adaptation

**BEFORE proceeding:**

1. **Create dark mode color overrides:**
   - Background: darkest shade (primary-900, close to black)
   - Surface: primary-800 or custom dark shade
   - Text: white/near-white shades
   - Determine dark mode equivalent for each semantic color
2. **Perform contrast verification:**
   - Verify WCAG AA (4.5:1 for normal text, 3:1 for large text) for each color pair
   - Auto-adjust tones for failures
3. **CSS media query or class-based approach:**
   - `@media (prefers-color-scheme: dark)` or `.dark` class overrides

```css
/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: #0F172A;
    --color-surface: #1E293B;
    --color-on-background: #F8FAFC;
    --color-on-surface: #E2E8F0;

    /* Palette shift */
    --color-primary-500: #60A5FA;  /* Brighter primary */
    --color-primary-600: #93C5FD;
  }
}
```

## Phase 7: Export to Target System

**BEFORE proceeding:**

1. **Determine the target system:** MUI Theme, Chakra Theme, Tailwind Config, CSS Custom Properties
2. **Generate appropriate format for each target:**
   - **CSS Custom Properties:** `:root` blocks as shown above
   - **Tailwind Config:** `tailwind.config.js` or `tailwind.config.ts`
   - **MUI Theme:** object compatible with `createTheme()`
   - **Chakra Theme:** object compatible with Chakra's theme structure
3. **Export all tokens:** No token should be skipped

```javascript
// Example: Tailwind Config export
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EFF6FF',
          100: '#DBEAFE',
          // ... full scale
          900: '#1E3A8A',
        },
        semantic: {
          success: '#10B981',
          warning: '#F59E0B',
          error: '#EF4444',
          info: '#3B82F6',
        },
      },
      fontFamily: {
        heading: ['Inter', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        0: '0px',
        0.5: '4px',
        1: '8px',
        // ... full scale
      },
      boxShadow: {
        sm: '0 1px 2px 0 rgba(0,0,0,0.05)',
        md: '0 4px 6px -1px rgba(0,0,0,0.1)',
        // ...
      },
      borderRadius: {
        none: '0px',
        sm: '4px',
        // ...
      },
    },
  },
};
```

## Phase 8: Final Verification

**BEFORE proceeding:**

- [ ] Has a 50-900 palette been generated for all brand colors?
- [ ] Is there a legible text equivalent (onPrimary, onSurface, etc.) for each color?
- [ ] Does the typography scale contain at least 7 levels?
- [ ] Is responsive typography (mobile/desktop) separated?
- [ ] Is the spacing scale consistent with the chosen base_unit?
- [ ] Are shadow, border radius, and animation tokens compatible with the brand personality?
- [ ] Are dark mode overrides defined?
- [ ] **Has WCAG contrast verification been performed?** (AA standard: 4.5:1 normal, 3:1 large text)
- [ ] Is the appropriate export for the target system (Tailwind/MUI/Chakra/CSS) ready?
- [ ] Do any tokens require "interpretation"? (the developer should know exactly what to do)
- [ ] Is the output format compatible with design-token-mapper?

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "These colors are enough, the developer will handle the rest" — **No.** Every shade of every color must be defined as a token.
- "We'll add dark mode later" — **No.** The output is not complete without dark mode tokens.
- "These colors look nice, no need for contrast checks" — **Wrong.** WCAG verification is mandatory.
- "A single CSS file is enough, no Tailwind config needed" — **Wrong.** Separate exports are required for each target system.
- "Skip brand personality, colors and fonts are enough" — **No.** Shadows, radius, and animation are also part of the brand.

**ALL of these mean: STOP. Return to the relevant phase.**

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "This primary color has insufficient contrast" — You skipped WCAG verification. Go back to Phase 6.
- "This font size is too large on mobile" — Responsive typography was skipped. Go back to Phase 3.
- "These shadows do not match the brand" — You skipped the brand personality analysis. Go back to Phase 5.
- "design-token-mapper cannot use these tokens" — Export format does not comply with the standard. Go back to Phase 7.
- "Text is unreadable in dark mode" — Dark mode contrast verification was not performed. Go back to Phase 6.

**When you see these:** STOP. Return to relevant phase.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "There are only 3 colors, no need for a full palette" | 30+ tokens can be derived from 3 colors. Every project needs a comprehensive palette. |
| "It's a small project, no need for so much formality" | Token standardization ensures consistency regardless of project scale. |
| "We will handle dark mode using a CSS filter" | CSS filters cause contrast issues and cannot be fine-tuned. |
| "The developer already knows which color to use where" | Tokens eliminate interpretation and minimize developer errors. |
| "WCAG contrast will be checked later" | If not checked during token generation, the entire system will have to be revised later. |

## Output Schema (MANDATORY)

```markdown
# [Architecture Name]
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

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| No tradeoffs | Decision without context | Every choice: "X over Y because..." |
| Vague tech ("use Kafka") | No justification | ADR format with 2+ alternatives |
| Missing CAP | Ignores partition reality | Every store: CP or AP? |
| No deployment diagram | Paper architecture | ASCII topology with AZs |
| Single option presented | No real analysis | Always compare 2+ choices |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Component decomposition | None | Listed | Bounded contexts with ownership |
| ADR tradeoffs | None | Some | Every decision: 2+ alternatives |
| CAP awareness | None | Mentioned | Per-store CP/AP + behavior |
| Communication matrix | None | Patterns only | Timeout+retry+circuit breaker |
| Deployment topology | None | "Deploy to cloud" | AZ diagram with counts |
| Risk register | None | 1-2 risks | 5+ with mitigation+owner |

**Pass: 8/12**

## Related Skills

- **design-token-mapper** — takes brand-to-design output and maps it to the target design system's token structure
- **branding-generator** — generates the input for this skill; brand-to-design does not work without branding-generator
- **wcag-validator** — auxiliary tool for contrast verification (this skill performs its own verification)
- **theme-generator** — takes brand-to-design output and converts it to full theme files

## Self-Review

After completing this skill's process:

1. **Scope Check:** Has every brand decision (color, typography, spacing, shadow, animation, dark mode) been converted into a token? No brand characteristic should be skipped.
2. **Consistency Check:** Are all tokens compatible with the brand personality? (e.g., a "rounded" brand should not have a sharp 0px radius)
3. **Export Check:** Have all tokens been exported in a format suitable for the target system (Tailwind/MUI/Chakra/CSS)? Can they be used with design-token-mapper?
4. **Quality Check:** Was the Iron Law followed? Has every token been verified for WCAG contrast? Do the dark mode overrides meet the same standard?
