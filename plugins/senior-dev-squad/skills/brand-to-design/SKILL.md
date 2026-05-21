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

## Conversion Workflow

Work through eight sequential phases. See [REFERENCE.md](REFERENCE.md) for full input/output examples, CSS/JS code dumps, and the detailed Phase 8 checklist.

1. **Phase 1 — Collect & verify inputs:** Obtain branding-generator output (JSON/YAML). Confirm colors (primary, secondary, accent), typography (family, base size, scale ratio), spacing base unit, and personality flags. Flag missing fields and apply defaults.
2. **Phase 2 — Color system:** Generate a 50-900 scale for every brand color. Derive surface/background, text (`onPrimary`, `onSurface`, etc.), and semantic state colors (success, warning, error, info).
3. **Phase 3 — Typography:** Build a 7-level type scale (xs → 3xl) from `base_size` × `scale_ratio`. Define weights (400–700), line heights, and letter spacing. Produce separate mobile and desktop values.
4. **Phase 4 — Spacing:** Generate a spacing scale from `base_unit`. Apply density mode ("compact" / "comfortable") multipliers. Add semantic aliases (`spacing-section`, `spacing-card`, `spacing-element`, `spacing-gap`).
5. **Phase 5 — Shadows, radius, animation:** Map brand personality → shadow opacity, border-radius range, and easing curve. Minimum: sm/md/lg shadow levels; none/sm/md/lg/xl/full radius; fast/normal/slow durations.
6. **Phase 6 — Dark mode:** Override surface, background, and text tokens for dark context. Run WCAG AA contrast verification (4.5:1 normal, 3:1 large text) on every color pair; auto-adjust tones on failure.
7. **Phase 7 — Export:** Produce the format(s) required by the project: CSS custom properties, Tailwind config, MUI `createTheme()` object, or Chakra theme object. No token is omitted.
8. **Phase 8 — Final verification:** Walk the checklist in [REFERENCE.md](REFERENCE.md). Every item must pass before the output is considered complete.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "These colors are enough, the developer will handle the rest" — **No.** Every shade of every color must be defined as a token.
- "We'll add dark mode later" — **No.** The output is not complete without dark mode tokens.
- "These colors look nice, no need for contrast checks" — **Wrong.** WCAG verification is mandatory.
- "A single CSS file is enough, no Tailwind config needed" — **Wrong.** Separate exports are required for each target system.
- "Skip brand personality, colors and fonts are enough" — **No.** Shadows, radius, and animation are also part of the brand.

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "There are only 3 colors, no need for a full palette" | 30+ tokens can be derived from 3 colors. Every project needs a comprehensive palette. |
| "It's a small project, no need for so much formality" | Token standardization ensures consistency regardless of project scale. |
| "We will handle dark mode using a CSS filter" | CSS filters cause contrast issues and cannot be fine-tuned. |
| "The developer already knows which color to use where" | Tokens eliminate interpretation and minimize developer errors. |
| "WCAG contrast will be checked later" | If not checked during token generation, the entire system will have to be revised later. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "This primary color has insufficient contrast" — You skipped WCAG verification. Go back to Phase 6.
- "This font size is too large on mobile" — Responsive typography was skipped. Go back to Phase 3.
- "These shadows do not match the brand" — You skipped the brand personality analysis. Go back to Phase 5.
- "design-token-mapper cannot use these tokens" — Export format does not comply with the standard. Go back to Phase 7.
- "Text is unreadable in dark mode" — Dark mode contrast verification was not performed. Go back to Phase 6.

**When you see these:** STOP. Return to relevant phase.

## Related Skills

- **design-token-mapper** — takes brand-to-design output and maps it to the target design system's token structure
- **branding-generator** — generates the input for this skill; brand-to-design does not work without branding-generator
- **wcag-validator** — auxiliary tool for contrast verification (this skill performs its own verification)
- **theme-generator** — takes brand-to-design output and converts it to full theme files

## Verification

After completing this skill's process:

1. **Scope Check:** Has every brand decision (color, typography, spacing, shadow, animation, dark mode) been converted into a token? No brand characteristic should be skipped.
2. **Consistency Check:** Are all tokens compatible with the brand personality? (e.g., a "rounded" brand should not have a sharp 0px radius)
3. **Export Check:** Have all tokens been exported in a format suitable for the target system (Tailwind/MUI/Chakra/CSS)? Can they be used with design-token-mapper?
4. **Quality Check:** Was the Iron Law followed? Has every token been verified for WCAG contrast? Do the dark mode overrides meet the same standard?

See [REFERENCE.md](REFERENCE.md) for the full Phase 8 checklist.
