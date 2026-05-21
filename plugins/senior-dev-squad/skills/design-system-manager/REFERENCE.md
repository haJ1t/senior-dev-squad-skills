# Design System Manager — Reference

Detailed catalog, comparison tables, installation examples, theming code, component matrix, and migration recipes. Linked from [SKILL.md](SKILL.md).

---

## Phase 1: Design System Catalog

Category-based map of 72+ open-source design systems.

```
MATERIAL DESIGN-BASED
├── Material UI (MUI)     — React, most popular, massive component set
├── Angular Material      — Angular, official Angular implementation of Material Design
├── Vuetify               — Material Design for Vue 3
├── Materialize           — Vanilla HTML/CSS/JS

SHADCN / RADIX-BASED
├── shadcn/ui             — React, Tailwind-based on Radix primitives, copy-paste architecture
├── Radix Themes          — React, unstyled primitives with full control
├── Park UI               — React/Vue, Radix + Panda CSS

ENTERPRISE / COMPREHENSIVE
├── IBM Carbon            — React/Vue/Svelte/Angular, dashboard-heavy, extremely comprehensive
├── Shopify Polaris       — React, e-commerce-focused, Shopify admin UI
├── Adobe Spectrum        — React, designed for Adobe products
├── Microsoft Fluent UI   — React, Office/Teams-like UI
├── Oracle Redwood        — React, enterprise SaaS
├── Salesforce Lightning  — Web Components, Salesforce ecosystem

DUI / COMPOUND
├── Ant Design            — React, Chinese ecosystem, very extensive, enterprise-grade
├── Chakra UI             — React, style props-driven, accessibility-first
├── Chakra UI Vue         — Chakra port for Vue 3

TAILWIND-BASED
├── Tailwind UI           — Tailwind CSS, premium paid components, ultra-high quality
├── DaisyUI               — Tailwind-based, free, extensive pre-built themes
├── Preline               — Tailwind-based, Tailwind UI alternative
├── Flowbite              — Tailwind-based, Figma + React/Vue
├── Headless UI           — Tailwind team, unstyled, accessible primitives

MINIMAL / UTILITY
├── Pico CSS              — 12KB, semantic HTML-focused, zero classes required
├── Bulma                 — CSS-only, Flexbox-based
├── Primer                — GitHub's CSS framework
├── Pure CSS              — 4KB, minimal responsive modules
├── Tachyons              — Functional CSS, atomic design

BOOTSTRAP ECOSYSTEM
├── Bootstrap             — Oldest, largest ecosystem, jQuery-free since v5
├── BootstrapVue          — Bootstrap for Vue 3
├── React Bootstrap       — Bootstrap for React
├── Bootswatch            — Bootstrap themes
├── Tabler                — Dashboard template built on Bootstrap

SPECIALIZED / NICHE
├── Semantic UI           — React, natural language class names
├── Evergreen             — React, Segment UI kit
├── Grommet               — React, Hewlett Packard Enterprise, highly focused on a11y
├── Nes.css               — Retro 8-bit CSS framework
├── XP.css                — Windows XP-style CSS
├── 98.css                — Windows 98-style CSS
├── Primer React          — GitHub PRs and Issues UI
├── Reach UI              — React, accessibility primitives (pre-Radix)
├── Ariakit               — React, accessibility primitives
├── Base Web              — React, Uber UI framework
├── Gestalt               — React, Pinterest UI
├── Orbit                 — React, Kiwi.com UI
├── Thunderbird           — UI for Microsoft Edge
├── Braid Design System   — React, Seek Australia, CSS-in-JS
├── Paste                 — React, Twilio
├── Constellation         — React, Lumen (CenturyLink)
├── LeafyGreen            — React, MongoDB
├── Pajamas               — Vue, GitLab UI
├── Elastic UI            — React, Elastic
├── Wix Style React       — React, Wix
├── Halfmoon              — Bootstrap alternative, native dark mode support
├── Vanilla Framework     — CSS-only, Canonical/Ubuntu
├── UIKit                — CSS + JS, comprehensive yet lightweight
├── Foundation            — CSS framework by ZURB
├── SUI                   — Semantic UI, Vue port
├── Buefy                 — Vue, Bulma-based
├── Fish UI               — Vue 3, Chinese ecosystem
├── Naive UI              — Vue 3, TypeScript-native, tree-shakeable
├── PrimeVue              — Vue 3, massive component collection
├── PrimeReact            — React, Prime ecosystem
├── PrimeNG               — Angular, Prime ecosystem
├── PrimeFlex             — CSS utility library, Prime ecosystem
├── Smooth UI             — React, Radix-like
├── Mantine               — React, comprehensive hooks + components
├── Tamagui               — React Native + Web, cross-platform
├── Gluestack             — React Native + Web, NativeBase successor
├── System UI             — React, theme-ui-based
├── Theme UI               — React, design tokens first
├── Lerp                  — React, minimal primitives
├── Catalyst              — React, Tailwind UI team, premium
├── React Aria            — React, Adobe, accessibility hooks
├── Spectrum              — Adobe's design system (includes React Native)
```

---

## Phase 2: Selection Comparison Tables

### Project Type → Recommended Design Systems

| Project Type | Option 1 | Option 2 | Option 3 | Why |
|--------------|----------|----------|----------|-----|
| **Dashboard / Admin** | MUI | Ant Design | IBM Carbon | Data-heavy components (tables, charts, complex forms) |
| **E-commerce** | Shopify Polaris | Chakra UI | Tailwind UI | Carts, product listings, filtering flows |
| **SaaS / B2B** | shadcn/ui | Mantine | Ant Design | Rapid iteration, styling flexibility |
| **Documentation Site** | Primer | Pico CSS | DaisyUI | Minimalist, highly readable, low bundle footprint |
| **Landing Page** | Tailwind UI | DaisyUI | Pico CSS | Fast-loading, SEO-friendly, lightweight |
| **Enterprise SaaS** | IBM Carbon | Adobe Spectrum | Ant Design | Comprehensive, enterprise-ready, i18n support |
| **Mobile-first Web** | Chakra UI | Tamagui | Gluestack | Responsive, touch-friendly interactions |
| **Open Source Projects** | Pico CSS | Primer | DaisyUI | MIT-licensed, active community support |
| **Internal Tools** | Ant Design | PrimeReact | Mantine | High-speed prototyping, rich form components |

### Bundle Size Comparison

```
Pico CSS           ~12 KB (CSS only)
DaisyUI            ~30 KB (CSS only)
Bulma              ~40 KB (CSS only)
Bootstrap          ~50 KB (CSS+JS)
Primer             ~60 KB (CSS only)
Tailwind UI        ~80 KB (JIT, payload matches usage)
shadcn/ui          ~100 KB (dependent on component usage)
Mantine            ~150 KB (with tree-shaking)
Chakra UI          ~200 KB (with tree-shaking)
MUI                ~250 KB (with tree-shaking)
Ant Design         ~300 KB (with tree-shaking)
IBM Carbon         ~350 KB (with tree-shaking)
```

### Accessibility (WCAG) Levels

```
Pico CSS           AA                   (natural via semantic HTML)
Primer             AA                   (GitLab/GitHub standards)
Radix Themes       AA+ (AAA-ready)      (accessibility-first primitives)
shadcn/ui          AA                   (built on Radix)
Chakra UI          AA+                  (WCAG 2.1 AA certified)
MUI                AA                   (comprehensive a11y tested)
IBM Carbon         AAA-ready            (highest enterprise standards)
Adobe Spectrum     AA                   (Adobe product standards)
Ant Design         AA                   (Chinese GB/T 35786-2017 + WCAG)
Bootstrap 5        AA                   (significant improvements in v5)
Tailwind UI        AA                   (built on Headless UI)
DaisyUI            A                    (basic styling only)
```

### Dark Mode Support

```
Native dark mode:
├── DaisyUI       — Instant theme changes via data-theme attribute
├── Pico CSS      — Native via data-theme="dark"
├── Mantine       — Via useMantineColorScheme hook
├── Chakra UI     — Via ColorModeScript
├── MUI           — Via createTheme + ThemeProvider
├── Ant Design    — Via ConfigProvider + algorithm.dark
├── IBM Carbon    — Via theme prop
└── DaisyUI       — 40+ pre-built themes

Via config/token override:
├── shadcn/ui     — Via CSS variables override
├── Tailwind UI   — Via dark: prefix
└── Primer        — Via color-modes

Manual implementation required:
├── Bootstrap     — Native dark mode support added in v5.3+ via CDN
├── Bulma         — Via custom CSS overrides
└── Foundation    — Via custom overrides
```

### License Compatibility

```
MIT (Free, highly permissive for all projects):
├── Chakra UI, Mantine, shadcn/ui, Radix Themes
├── DaisyUI, Pico CSS, Bulma, Primer
├── PrimeReact, PrimeVue, PrimeNG
├── Naive UI, Fish UI, Buefy
└── Headless UI, Reach UI, Ariakit

Apache 2.0:
├── MUI, Ant Design, Materialize
└── Bootstrap, React Bootstrap

MIT + Premium Paid Components:
└── Tailwind UI (components paid, underlying framework MIT)

BSD:
└── IBM Carbon, Semantic UI

Custom / Enterprise:
├── Shopify Polaris — MIT + Shopify trademark guidelines
├── Adobe Spectrum   — Apache 2.0
├── Fluent UI        — MIT
└── Oracle Redwood   — Oracle License (restricted enterprise)
```

---

## Phase 3: Installation and Configuration

### Installation Command Examples

```bash
# MUI (React)
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material

# shadcn/ui (React, with Tailwind)
npx shadcn@latest init
npx shadcn@latest add button card dialog form

# Ant Design (React)
npm install antd @ant-design/icons

# Chakra UI (React)
npm install @chakra-ui/react @emotion/react @emotion/styled framer-motion

# IBM Carbon (React)
npm install @carbon/react @carbon/styles @carbon/icons-react

# Mantine (React)
npm install @mantine/core @mantine/hooks @mantine/form @mantine/notifications

# DaisyUI (with Tailwind)
npm install -D daisyui
# tailwind.config.js: plugins: [require("daisyui")]

# Pico CSS (Vanilla)
npm install @picocss/pico
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">

# Bootstrap (Vanilla)
npm install bootstrap @popperjs/core

# PrimeReact
npm install primereact primeicons
```

### Provider Wrapper Setup

Each design system has its own distinct provider or ThemeProvider structure. Use the following patterns:

```tsx
// MUI
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

// Chakra UI
import { ChakraProvider, extendTheme } from '@chakra-ui/react';

// Mantine
import { MantineProvider } from '@mantine/core';

// Ant Design
import { ConfigProvider } from 'antd';

// IBM Carbon
import { Theme } from '@carbon/react';
```

```tsx
// Example: Mantine setup with Next.js App Router
// app/layout.tsx
import '@mantine/core/styles.css';
import { MantineProvider, ColorSchemeScript } from '@mantine/core';

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <head>
        <ColorSchemeScript />
      </head>
      <body>
        <MantineProvider defaultColorScheme="light">
          {children}
        </MantineProvider>
      </body>
    </html>
  );
}
```

---

## Phase 4: Theme API and Design Tokens

### Token Types and System Mappings

Different design systems define tokens differently. Use this table to map equivalents:

| Token | MUI | Chakra | Ant Design | Mantine | Carbon | DaisyUI |
|-------|-----|--------|-----------|---------|--------|---------|
| Primary | palette.primary.main | colors.blue.500 | token.colorPrimary | theme.primaryColor | interactive.01 | --p |
| Secondary | palette.secondary.main | colors.gray.600 | token.colorInfo | theme.secondaryColor | interactive.02 | --s |
| Background | palette.background.default | colors.gray.550 | token.colorBgLayout | theme.colors.gray[0] | background | --b3 |
| Text Primary | palette.text.primary | colors.gray.800 | token.colorText | theme.black | text.primary | --bc |
| Border Radius | shape.borderRadius | radii.md | token.borderRadius | theme.defaultRadius | layer.borderRadius | --rounded |
| Font Family | typography.fontFamily | fonts.body | token.fontFamily | theme.fontFamily | type.family | --font |
| Spacing | spacing.unit | space.4 | token.marginXXS | theme.spacing.xs | spacing.05 | --p |

### Theme Customization Examples

```tsx
// === MUI ===
const theme = createTheme({
  palette: {
    primary: { main: '#2563EB', light: '#60A5FA', dark: '#1D4ED8' },
    secondary: { main: '#7C3AED' },
    background: { default: '#F9FAFB' },
  },
  typography: {
    fontFamily: '"Inter", "Roboto", sans-serif',
    h1: { fontSize: '2.5rem', fontWeight: 700 },
  },
  shape: { borderRadius: 12 },
});

// === Chakra ===
const theme = extendTheme({
  colors: {
    brand: {
      50: '#EFF6FF', 100: '#DBEAFE', 500: '#2563EB', 900: '#1E3A5F',
    },
  },
  fonts: { heading: '"Inter", sans-serif', body: '"Inter", sans-serif' },
  radii: { md: '12px' },
  space: { 4: '1rem' },
});

// === Ant Design ===
// app/theme.ts
import type { ThemeConfig } from 'antd';
const theme: ThemeConfig = {
  token: {
    colorPrimary: '#2563EB',
    borderRadius: 12,
    fontFamily: '"Inter", sans-serif',
    colorBgLayout: '#F9FAFB',
  },
  components: {
    Button: { controlHeight: 40, borderRadius: 8 },
    Card: { paddingLG: 24 },
  },
};

// === Mantine ===
import { createTheme } from '@mantine/core';
const theme = createTheme({
  primaryColor: 'blue',
  defaultRadius: 'md',
  fontFamily: '"Inter", sans-serif',
  colors: {
    brand: ['#EFF6FF', '#DBEAFE', '#BFDBFE', '#93C5FD', '#60A5FA',
            '#3B82F6', '#2563EB', '#1D4ED8', '#1E40AF', '#1E3A5F'],
  },
  spacing: { xs: '0.5rem', sm: '0.75rem', md: '1rem', lg: '1.5rem', xl: '2rem' },
});

// === DaisyUI (CSS variables) ===
/* globals.css */
:root {
  --p: #2563EB;
  --s: #7C3AED;
  --b3: #F9FAFB;
  --bc: #1F2937;
  --rounded: 12px;
  --font: "Inter", sans-serif;
}
```

### Dark Mode Integration

```tsx
// Mantine (built-in)
<MantineProvider defaultColorScheme="auto">
  {/* auto = matches system preferences, "light" or "dark" can also be explicitly forced */}
</MantineProvider>

// Chakra (built-in)
<ChakraProvider>
  <ColorModeScript initialColorMode="system" />
</ChakraProvider>

// MUI
const darkTheme = createTheme({
  palette: { mode: 'dark', primary: { main: '#60A5FA' } },
});
<ThemeProvider theme={isDark ? darkTheme : lightTheme}>

// Ant Design
import { ConfigProvider, theme } from 'antd';
<ConfigProvider theme={{ algorithm: theme.darkAlgorithm }}>
  {/* algorithm.defaultAlgorithm = light */}
</ConfigProvider>

// DaisyUI (HTML attribute)
<html data-theme={currentTheme}>
{/* 40+ pre-built themes: "light", "dark", "cupcake", "retro", "cyberpunk", ... */}
```

---

## Phase 5: Component Inventory Matrix

| Component | MUI | Ant Design | Chakra | Mantine | Carbon | DaisyUI |
|-----------|-----|-----------|--------|---------|--------|---------|
| **BUTTON** | Full | Icon+Text | Variant+size | Full featured | Primary+Secondary | 6 colors |
| **FORM** | TextField, Select | Form, Validation | useForm hook | useForm + Zod | FormGroup | Limited |
| **INPUT** | TextField | Input, InputNumber | Input | TextInput, NumberInput | TextInput | input |
| **SELECT** | Select, Autocomplete | Select, TreeSelect | Select | Select, MultiSelect | ComboBox | select |
| **DATE PICKER** | DatePicker | DatePicker (robust) | @chakra-ui/date-picker | DatePickerInput | DatePicker | None |
| **MODAL** | Dialog | Modal (robust) | Modal | Modal | Modal | modal |
| **DRAWER** | Drawer | Drawer | Drawer | Drawer | SideNav | None |
| **TABLE** | DataGrid (paid) | Table (very robust) | Basic | Table | DataTable | None |
| **TABS** | Tabs | Tabs | Tabs | Tabs | Tabs | tabs |
| **ACCORDION** | Accordion | Collapse | Accordion | Accordion | Accordion | collapse |
| **CHIP / BADGE** | Chip | Tag, Badge | Tag, Badge | Badge, Chip | Tag, Badge | badge |
| **TOAST** | Snackbar | message | useToast | Notifications | ToastNotification | toast |
| **PROGRESS** | Linear, Circular | Progress | Progress | Progress | ProgressBar | progress |
| **SIDEBAR** | Via Drawer | Menu + Sider | Via Drawer | NavLink | SideNav | drawer |
| **AVATAR** | Avatar | Avatar | Avatar | Avatar | Avatar | avatar |
| **CARD** | Card | Card | Card | Card | Tile | card |
| **STEPPER** | Stepper | Steps | Basic | Stepper | ProgressStep | None |
| **TREE** | TreeView | Tree | None | None | TreeView | None |
| **UPLOAD** | None (3rd party) | Upload (robust) | None | None (3rd party) | FileUploader | file-input |

> **LEGEND:** Full = Full Support | Basic/Limited = Limited Support / Extension required | None = Missing (must build manually)

---

## Phase 6: Migration Strategies and Examples

### Migration Strategy Comparison

```
BIG BANG (Fast, High Risk)
  └── Small projects (< 10 pages), MVP cleanups
  └── Risk: Everything can break simultaneously

GRADUAL (Slower, Secure)
  └── Large projects (> 10 pages), active production apps
  └── Steps:
        1. Run both systems in parallel (Coexistence layer)
        2. Implement new components using the target system
        3. Migrate legacy components incrementally
        4. Remove the legacy system package

STRANGLER FIG (Most Secure)
  └── Massive applications (50+ pages), legacy systems
  └── Route-level routing partitioning
  └── Each route is migrated independently from end-to-end
```

### Transition Example: Bootstrap → Mantine

```bash
# 1. Install both systems
npm install bootstrap @mantine/core @mantine/hooks @mantine/notifications

# 2. Add the provider wrapper (both systems remain operational)
# app/layout.tsx
import '@mantine/core/styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { MantineProvider } from '@mantine/core';

# 3. Prevent global style collisions
/* globals.css — Isolate Bootstrap styles from Mantine domains */
.mantine-wrapper * {
  /* Elements in Mantine scope will not inherit Bootstrap style overrides */
}

# 4. Progressively replace components
# Bootstrap → Mantine Equivalents:
# <div className="container">       → <Container>
# <button className="btn btn-primary"> → <Button color="blue">
# <div className="card">            → <Card>
# <div className="modal">           → <Modal>
# <div className="alert">           → <Alert>
# <div className="badge">           → <Badge>
# <nav className="navbar">          → <AppShell.Header>
```

```tsx
// Example: Bootstrap Button → Mantine Button
// BEFORE (Bootstrap)
<button className="btn btn-primary" onClick={handleClick} disabled={loading}>
  {loading ? <span className="spinner-border spinner-border-sm" /> : null}
  Save
</button>

// AFTER (Mantine)
<Button onClick={handleClick} loading={loading}>
  Save
</Button>
```

### Token Migration Mappings

| CSS Variable (Bootstrap) | Token Target | Example (Mantine) |
|--------------------------|--------------|-------------------|
| `--bs-primary` | Primary Color | theme.colors.blue[6] |
| `--bs-secondary` | Secondary Color | theme.colors.gray[6] |
| `--bs-border-radius` | Border Radius | theme.defaultRadius="md" |
| `--bs-font-family` | Font Family | theme.fontFamily |
| `--bs-spacer` | Spacing Value | theme.spacing |
