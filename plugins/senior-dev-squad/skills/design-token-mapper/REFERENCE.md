# Design Token Mapper — Reference

Detailed mapping templates, semantic token examples, component override code, breakpoint/dark-mode mappings, theme override patterns, and migration recipes. Linked from [SKILL.md](SKILL.md).

---

## Phase 1: Defining Source and Target Systems

**BEFORE proceeding:**

1. **Identify source tokens** — read the output from brand-to-design (CSS custom properties, JSON, YAML).
2. **Identify target system(s)** — MUI Theme, Chakra Theme, Tailwind Config, CSS Custom Properties, or a custom system.
3. **Analyze the target system's token structure:**
   - How are colors pathed? (`theme.palette.primary.main` vs. `colors.primary.500`)
   - How is typography defined? (`theme.typography.h1.fontSize` vs. `fontSize.4xl`)
   - What is the spacing system like? (`theme.spacing(4)` vs. `spacing.4`)
4. **Create a mapping template** — a mapping dictionary defining the target system equivalent for each source token.

```yaml
# Example: Source → Target mapping template (MUI & Tailwind)
mappings:
  colors:
    brand.color.primary.500:
      mui: palette.primary.main
      tailwind: colors.primary.500
    brand.color.primary.600:
      mui: palette.primary.dark
      tailwind: colors.primary.600
    brand.color.neutral.100:
      mui: palette.grey.100
      tailwind: colors.gray.100
  typography:
    brand.typography.base_size:
      mui: typography.fontSize
      tailwind: fontSize.base
```

---

## Phase 2: Creating the Semantic Token Layer

**BEFORE proceeding:**

1. **Define semantic meanings:**
   - danger/error, success, warning, info, primary, secondary
   - Link each semantic meaning to a brand token.
2. **Generate all variants for each semantic token:**
   - main, light, dark, contrastText (MUI standard)
   - Or 500, 200, 700, on-* (Tailwind/CSS standard)
3. **Map each semantic token to its equivalent in the target system.**

```javascript
// Example: Semantic token map
const semanticTokens = {
  error: {
    main: 'brand.color.accent.500',    // #F59E0B → MUI: palette.error.main
    light: 'brand.color.accent.300',   // #FCD34D → MUI: palette.error.light
    dark: 'brand.color.accent.700',    // #B45309 → MUI: palette.error.dark
    contrastText: 'brand.color.onAccent', // #FFFFFF → MUI: palette.error.contrastText
  },
  success: {
    main: 'brand.color.success',
    light: 'brand.color.success-100',  // Derived
    dark: 'brand.color.success-700',
    contrastText: '#FFFFFF',
  },
};
```

---

## Phase 3: Component-Level Mapping

**BEFORE proceeding:**

1. **Identify all component properties in the target system:**
   - MUI: `Button` → `color="primary"`, `variant="contained"`
   - Chakra: `Button` → `colorScheme="blue"`, `variant="solid"`
   - Tailwind: `Button` → `className="bg-primary-500"`
2. **Bind each component property to a semantic token:**
   - `Button.color="primary"` → `semantic.primary.main`
   - `Alert.severity="error"` → `semantic.error.main`
3. **Generate theme overrides:**
   - Map all token assignments for a single component's variants.
   - Export component overrides in a format compatible with the target system's theme structure.

```javascript
// Example: MUI Component-Level Mapping
const MuiButtonOverride = {
  styleOverrides: {
    root: ({ ownerState, theme }) => ({
      backgroundColor: ownerState.color
        ? theme.palette[ownerState.color].main
        : theme.palette.primary.main,
      borderRadius: theme.shape.borderRadius,
      padding: theme.spacing(1, 2),
      transition: `all ${theme.transitions.duration.short}ms`,
    }),
    containedPrimary: {
      backgroundColor: 'var(--color-primary-500)',
      '&:hover': {
        backgroundColor: 'var(--color-primary-600)',
      },
    },
  },
};
```

---

## Phase 4: Breakpoint and Dark Mode Mapping

**BEFORE proceeding:**

1. **Breakpoint mapping:**
   - Map brand breakpoints (xs, sm, md, lg, xl) to target system breakpoints.
   - Systems may have different breakpoint values (MUI: 600/900/1200, Tailwind: 640/768/1024).
2. **Dark mode cross-mapping:**
   - Generate dark mode token equivalents for all target systems.
   - Implementation varies by system:
     - MUI: `createTheme({ palette: { mode: 'dark' } })`
     - Chakra: `extendTheme({ config: { initialColorMode: 'dark' } })`
     - Tailwind: `dark:` prefix or CSS custom properties override.
   - Verify dark mode produces the exact same visual results across all target systems.

```javascript
// Example: Cross-system dark mode mapping
const darkModeMap = {
  mui: {
    palette: {
      mode: 'dark',
      background: { default: '#0F172A', paper: '#1E293B' },
      primary: { main: '#60A5FA' },
    },
  },
  chakra: {
    config: { initialColorMode: 'dark' },
    colors: {
      brand: { bg: '#0F172A', surface: '#1E293B' },
    },
  },
  tailwind: {
    // CSS custom properties override
    ':root.dark': {
      '--color-background': '#0F172A',
      '--color-surface': '#1E293B',
    },
  },
};
```

---

## Phase 5: Generating Theme Overrides

**BEFORE proceeding:**

1. **Create theme override files for each target system:**
   - Ensure overrides are safe from design system package updates.
   - Keep overrides in a separate layer; do not modify system themes directly.
2. **Override strategy:**
   - **Layered:** Base theme → Brand override layer → Component override layer.
   - **Isolated:** Each override can be updated independently.
   - **Preservative:** Overrides are preserved when system updates are applied.
3. **Structure the override format based on the target system:**

```javascript
// Example: Chakra Theme Override (layered)
import { extendTheme } from '@chakra-ui/react';

const brandOverrides = {
  colors: {
    brand: {
      50: '#EFF6FF',
      500: '#3B82F6',
      900: '#1E3A8A',
    },
  },
  fonts: {
    heading: "'Inter', sans-serif",
    body: "'Inter', sans-serif",
  },
  space: {
    1: '8px',
    2: '16px',
    4: '32px',
  },
};

const componentOverrides = {
  components: {
    Button: {
      baseStyle: { borderRadius: '8px' },
      variants: {
        solid: (props) => ({
          bg: `${props.colorScheme}.500`,
        }),
      },
    },
  },
};

export default extendTheme(brandOverrides, componentOverrides);
```

---

## Phase 6: Migrations — Switching Between Systems

**BEFORE proceeding:**

1. **Record all token mappings of the current system:**
   - Which brand token maps to which system token?
   - Note any custom/overridden mappings.
2. **Analyze the target system's token structure:**
   - Find tokens carrying the same semantic meaning.
   - Identify discrepancies (e.g., MUI's `palette.primary.light` = Chakra's `colors.brand.200`).
3. **Build a migration mapping:**
   - Map each token from the source system to its target system equivalent.
   - Set up a fallback strategy for tokens with no equivalents.
4. **Execute the migration script:**
   - Update all component overrides, theme files, and style references.
   - Search for old token references and replace them with new ones.

```bash
# Example: Migration Checklist
# 1. Export source system tokens (e.g., MUI theme object)
# 2. Analyze target system token structure (e.g., Chakra)
# 3. Generate mapping dict
# 4. Execute the migration script
# 5. Perform visual regression testing
# 6. Remove obsolete system dependencies
```
