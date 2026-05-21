---
name: i18n-localization-engineer
description: "ICU MessageFormat, RTL/bidi layout, Intl API, locale fallback chains, pseudo-localization, TMS handoff, plural/gender rules. Use when internationalizing or localizing a UI."
---

# I18n Localization Engineer

## Overview

Internationalization (i18n) is the engineering discipline of structuring code so every user-facing string, number, date, currency, and layout adapts to any locale without changing source code. Localization (l10n) is the act of producing those locale-specific assets. Done well, the two are invisible to users and seamless for translators. Done poorly, they produce garbled text, broken layouts, untranslatable strings, and shipping delays every release.

This skill covers the full pipeline: externalizing strings, writing ICU MessageFormat messages, wiring the `Intl` API for dates/numbers/currencies, handling RTL and bidi layout, designing locale fallback chains, generating pseudo-locales for early testing, and handing off catalogs to a translation management system (TMS).

**Core principle:** Every user-visible string is a locale resource. If it lives in source code, it is a bug.

## The Iron Law

```
NO HARDCODED UI TEXT — EVERY STRING LIVES IN A LOCALE CATALOG
```

If a string is rendered to the user and is not looked up through the i18n layer, the feature is not shippable to non-English locales.

## When to Use

**Use this when:**
- Adding any new UI text, labels, error messages, tooltips, or notifications
- Implementing date, time, number, or currency display
- Supporting a new locale or language in the product
- Designing the initial i18n architecture for a frontend or backend service
- Auditing an existing codebase for hardcoded strings

**Use this ESPECIALLY when:**
- The product is expanding to a new region or language for the first time
- A feature contains plural forms ("1 item" vs "2 items"), gender-inflected strings, or ordinals
- The layout must support right-to-left scripts (Arabic, Hebrew, Persian, Urdu)
- Translators report missing context, broken interpolations, or strings they cannot translate
- The CI pipeline does not yet catch new hardcoded strings

**Don't skip when:**
- The feature "is just for English for now" — retrofitting i18n is 5× the work of doing it upfront
- Strings are generated dynamically or concatenated from parts — these are the hardest to localize later
- A design uses absolute pixel positioning — RTL will break it

## String Externalization

Every user-facing string must be extracted to a locale catalog before the feature ships. The canonical format for structured messages is ICU MessageFormat.

**Directory layout (flat + namespace):**
```
src/
  locales/
    en/
      common.json
      checkout.json
      errors.json
    ar/
      common.json
      checkout.json
      errors.json
    pseudo/
      common.json        ← generated, never hand-edited
```

**Bad — hardcoded string:**
```tsx
// WRONG: string lives in component source
<p>You have 3 unread messages.</p>
```

**Good — externalized with ICU plural:**
```tsx
// messages/en/inbox.json
{
  "unread_count": "{count, plural, =0 {No unread messages} one {You have # unread message} other {You have # unread messages}}"
}

// Component
import { useIntl } from 'react-intl';
const { formatMessage } = useIntl();
<p>{formatMessage({ id: 'unread_count' }, { count: unreadCount })}</p>
```

**Rule:** Never concatenate translated strings. "Hello " + name produces incorrect word order in many languages. Always use a single message key with named placeholders.

### ICU MessageFormat Patterns

ICU MessageFormat handles plurals, gender, selects, and nested combinations in a single string that translators can reorder freely.

```
// Plural
{count, plural, =0 {No files} one {# file} other {# files}}

// Select (gender)
{gender, select, male {He rated this} female {She rated this} other {They rated this}}

// Nested plural + select
{host, select,
  female {{count, plural, one {{host} invited # guest} other {{host} invited # guests}}}
  other  {{count, plural, one {{host} invited # guest} other {{host} invited # guests}}}
}

// Date/time (use Intl, not ICU, in runtime code — ICU here is for TMS context)
{lastSeen, date, medium}
```

Always provide a translator note (context comment) next to each key in the catalog file or as a `_comment` sibling key:

```json
{
  "file_count": "{count, plural, one {# file selected} other {# files selected}}",
  "file_count_comment": "Shown in the toolbar after the user selects files in the document list. 'count' is always >= 1."
}

```

### Intl API for Dates, Numbers, and Currencies

Never format dates or numbers with hand-rolled logic. Use the ECMA-402 `Intl` API, which is available in every modern runtime.

```ts
// Date formatting
const fmt = new Intl.DateTimeFormat(locale, { dateStyle: 'medium', timeStyle: 'short' });
fmt.format(new Date(timestamp)); // "May 21, 2026 at 3:45 PM" in en-US

// Relative time
const rel = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' });
rel.format(-1, 'day'); // "yesterday" in en-US, "أمس" in ar

// Number formatting
const num = new Intl.NumberFormat(locale, { maximumFractionDigits: 2 });
num.format(1234567.89); // "1,234,567.89" in en-US, "1.234.567,89" in de-DE

// Currency
const cur = new Intl.NumberFormat(locale, { style: 'currency', currency: currencyCode });
cur.format(price); // "$1,234.56" in en-US, "1.234,56 €" in de-DE

// List formatting
const list = new Intl.ListFormat(locale, { style: 'long', type: 'conjunction' });
list.format(['apples', 'oranges', 'pears']); // "apples, oranges, and pears"
```

**Never** pass a raw `Date.toLocaleString()` without a locale argument — it falls back to the runtime locale, producing inconsistent results across environments.

### RTL and Bidi Layout

Right-to-left support is a layout concern, not just a text concern. Every directional CSS property must have a logical-property equivalent.

```css
/* WRONG — breaks in RTL */
.card { padding-left: 16px; margin-right: 8px; text-align: left; }

/* CORRECT — logical properties, direction-agnostic */
.card { padding-inline-start: 16px; margin-inline-end: 8px; text-align: start; }
```

Set `dir` and `lang` on the `<html>` element at runtime:

```ts
document.documentElement.setAttribute('lang', locale);
document.documentElement.setAttribute('dir', isRTL(locale) ? 'rtl' : 'ltr');
```

RTL locales include: `ar`, `he`, `fa`, `ur`, `ps`, `ug`, `yi`, `dv`. Maintain a static set and check membership; do not rely on `Intl` to expose directionality.

For inline bidi text (e.g., a user-entered English URL inside an Arabic sentence), wrap with `<bdi>` or apply `unicode-bidi: isolate` to prevent the Unicode Bidi Algorithm from corrupting surrounding text.

### Locale Fallback Chains and Bundle Loading

A locale like `zh-Hant-TW` must fall back gracefully: `zh-Hant-TW` → `zh-Hant` → `zh` → `en`. Define this chain explicitly rather than relying on browser behavior.

```ts
function buildFallbackChain(locale: string): string[] {
  const parts = locale.split('-');
  const chain: string[] = [];
  for (let i = parts.length; i > 0; i--) {
    chain.push(parts.slice(0, i).join('-'));
  }
  chain.push('en'); // ultimate fallback
  return chain; // ['zh-Hant-TW', 'zh-Hant', 'zh', 'en']
}
```

Lazy-load locale bundles to avoid shipping all translations to every user:

```ts
async function loadMessages(locale: string): Promise<Record<string, string>> {
  const chain = buildFallbackChain(locale);
  for (const candidate of chain) {
    try {
      const messages = await import(`./locales/${candidate}/common.json`);
      return messages.default;
    } catch {
      continue;
    }
  }
  throw new Error(`No locale bundle found for ${locale}`);
}
```

Dynamic `import()` with a static path prefix allows bundlers (webpack, Vite) to generate per-locale chunks automatically.

### Pseudo-Localization for Early Testing

Pseudo-localization transforms the English catalog into a synthetic locale that exposes layout overflow, hardcoded strings, and missing interpolation slots before any translator is involved.

A pseudo-locale should:
- Replace ASCII characters with accented equivalents to catch non-Unicode rendering
- Expand strings by ~30–40% (most European translations are longer than English)
- Wrap each string in `[` `]` brackets to identify untranslated strings by inspection
- Leave ICU placeholders (`{name}`, `#`) intact so interpolation still works

```ts
function pseudoLocalize(str: string): string {
  const map: Record<string, string> = {
    a:'à', b:'ƀ', c:'ć', d:'ď', e:'è', f:'ƒ', g:'ĝ', h:'ĥ',
    i:'î', j:'ĵ', k:'ķ', l:'ĺ', m:'m̂', n:'ñ', o:'ô', p:'p̀',
    q:'q̂', r:'ŕ', s:'ŝ', t:'ţ', u:'û', v:'v̂', w:'ŵ', x:'x̂', y:'ŷ', z:'ź',
  };
  // Preserve ICU placeholders: {name}, {count, plural, ...}
  const parts = str.split(/(\{[^}]*\}|#)/g);
  return '[' + parts.map(p => /^\{|^#$/.test(p) ? p : [...p].map(c => map[c.toLowerCase()] ?? c).join('')).join('') + '_extra]';
}
```

Add a `pseudo` locale to the CI build and run visual regression against it to catch overflow before code review.

### TMS Handoff and Translator Context

When exporting catalog files to a translation management system (Lokalise, Phrase, Crowdin, Transifex), include:

- **Key naming:** hierarchical, noun-first (`checkout.summary.total_label`, not `label_for_checkout_total`)
- **Screenshots or UI context URLs:** embed `_screenshot` or `_context_url` sibling keys or use TMS metadata APIs
- **Max-length hints:** many TMS platforms enforce character limits per key; set them to prevent UI overflow
- **Do-not-translate tokens:** mark brand names, product names, and code identifiers as non-translatable placeholders (`<ph name="brand">Acme</ph>` in XLIFF, or `{brand}` as a named placeholder in ICU)

```json
{
  "checkout.cta.place_order": "Place order with {brand}",
  "checkout.cta.place_order_comment": "CTA button at checkout. {brand} is always 'Acme' and must not be translated. Max 40 chars in translation.",
  "checkout.cta.place_order_maxlength": 40
}
```

Never export raw ICU syntax to TMS without verifying the platform supports it. If the TMS does not support ICU, convert plurals to platform-native plural categories before export and convert back on import.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:

- "I'll just hardcode this label, it's a one-off" — every hardcoded string blocks a locale
- "The translator will figure out the word order" — concatenated strings are untranslatable
- "We can add RTL support later, we don't have Arabic users yet" — logical-property CSS costs nothing upfront; retrofitting costs days
- "I'll use `toLocaleDateString()` without a locale argument, it'll be fine" — it produces undefined behavior in server-side rendering and CI
- "The plural rule for Chinese is simple, I won't bother with ICU" — Chinese has one plural category, but adding ICU upfront costs nothing and prevents rework if the product adds Polish, Arabic, or Russian (which have 3–6 categories)
- Missing translator context on any key
- A new feature ships with zero entries in the locale catalog

**ALL of these mean: STOP. Return to the relevant phase.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "English only for now, we'll i18n later" | Retrofitting i18n into an existing codebase takes weeks and touches every component. Do it first. |
| "It's just a number, I'll format it inline" | `1,234.56` vs `1.234,56` vs `1 234,56` — number formats differ by locale and break trust. |
| "Translators don't need context, the string is obvious" | "Order" is a noun in one place and a verb in another. Without context, translators guess wrong. |
| "We don't have RTL locales in our user base" | CSS logical properties are a zero-cost habit. Skipping them creates a weeks-long migration when you do expand. |
| "Pseudo-localization is only needed before launch" | New strings are added every sprint. Pseudo-locale CI catches overflow continuously, not just at launch. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**

- "The Arabic layout looks like a mirror image only in some places" — you used physical CSS properties (`left`, `right`, `margin-left`) instead of logical ones
- "Translators are asking what this string is for" — you shipped keys without context comments
- "Some strings in production are still in English" — your CI does not enforce full catalog coverage, or a string was added after the translation freeze
- "The date looks wrong in Germany" — you formatted with `Date.toLocaleString()` without a locale, or used `MM/DD/YYYY` directly

**When you see these:** STOP. Return to the relevant phase and fix the root cause — do not patch individual strings.

## Related Skills

- **frontend-senior-engineer** — component architecture that the i18n layer must integrate with; use together for new feature builds
- **accessibility-optimizer** — `lang` attributes, bidi markup, and screen-reader announcements overlap with i18n concerns
- **content-strategist** — source string quality and tone directly affect translatability; coordinate on key naming and content guidelines
- **responsive-layout-engine** — RTL layout work belongs in the responsive system; logical properties must be enforced at the design-system level

## Verification

- [ ] Zero hardcoded user-visible strings in new or modified components (grep for string literals in JSX/templates)
- [ ] All new message keys use ICU MessageFormat for plural, select, and interpolation
- [ ] Every new key has a `_comment` or TMS context note explaining usage and any non-translatable tokens
- [ ] Dates, times, numbers, and currencies use `Intl` API with an explicit locale argument
- [ ] CSS uses logical properties (`inline-start/end`, `block-start/end`) — no `left`, `right`, `margin-left`, `padding-right` in new styles
- [ ] `<html>` element receives `lang` and `dir` attributes at runtime based on active locale
- [ ] Locale fallback chain is defined and tested for all supported locales
- [ ] Locale bundles are lazy-loaded; no single bundle contains all locales
- [ ] Pseudo-locale build passes without layout overflow in visual regression
- [ ] TMS export includes max-length hints and non-translatable token markers
- [ ] CI lint rule (e.g., `eslint-plugin-i18next` or equivalent) blocks new hardcoded strings in PRs
