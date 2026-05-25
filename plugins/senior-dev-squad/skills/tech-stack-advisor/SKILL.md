---
name: tech-stack-advisor
description: "Interactive tech stack selection: decision trees, tradeoff tables, stack templates. Use when choosing technologies for a new project or migration."
---

# Tech Stack Advisor

## Overview

When a user doesn't know which tech stack to use, guide them through an interactive decision tree. Present options with trade-offs, not opinions. Let the user's project requirements drive the choice.

**Core principle:** THE BEST TECH STACK IS THE ONE THAT FITS THE PROJECT, NOT THE ONE THAT'S TRENDING.

## The Iron Law

```
NEVER RECOMMEND A VERSION WITHOUT VERIFYING IT'S THE CURRENT STABLE RELEASE
```

Web search for the latest version. Don't guess. Last month's version might be outdated.

## When to Use

**Use this when:**
- User says "help me choose a stack" during discovery
- User has no preference on language/framework
- User is unsure about database or deployment choices
- Before architecture-planner (stack decision feeds architecture)

**Don't skip when:**
- "Everyone uses [popular stack]" (popular ≠ right for this project)
- "Just pick whatever" (they'll blame you when it doesn't fit)

## Stack Selection Flow

### Step 1: Determine Project Type

From discovery output (or ask now):

| Type | Recommended Approach |
|------|--------------------|
| Web Application | Full-stack framework (Next.js, Nuxt, SvelteKit, Remix, Rails, Django, Laravel, Blazor) |
| API / Backend | Dedicated framework (FastAPI, Express, Gin, Fiber, Actix) |
| CLI / Library | Language-native (Node, Python, Go, Rust) |
| Mobile | React Native, Flutter, SwiftUI (iOS), Jetpack Compose (Android) |
| Desktop | Tauri, Electron, .NET MAUI, Qt |

### Step 2: Language Preference (AskUserQuestion)

```
What programming language?
  ["TypeScript/JavaScript — fullstack ecosystem, most libraries, huge community"]
  ["Python — data/ML, rapid prototyping, scientific computing"]
  ["Go — performance, concurrency, single binary, devops tools"]
  ["Rust — maximum performance, safety, systems programming"]
  ["Java/Kotlin — enterprise, Android, JVM ecosystem"]
  ["C#/.NET — enterprise, Windows, Unity, Blazor"]
  ["Ruby — rapid web dev, Rails ecosystem"]
  ["PHP — web, Laravel, WordPress"]
  ["No preference — recommend for this project type"]
```

### Step 3: Framework Decision Tree

**If Web + TypeScript:**

```
Framework preference?
  ["Next.js (React) — SSR, static, app router, Vercel ecosystem"]
  ["Remix (React) — web standards, forms, progressive enhancement"]
  ["Nuxt (Vue) — SSR, modules, Vue ecosystem"]
  ["SvelteKit — minimal JS, fast dev experience"]
  ["Astro — content sites, islands architecture"]
  ["Express/plain — minimal, DIY everything"]
```

**If Web + Python:**

```
Framework preference?
  ["Django — batteries included, admin, ORM, auth"]
  ["FastAPI — async, Pydantic, OpenAPI, modern Python"]
  ["Flask — minimal, flexible, extensions"]
```

**If Web + Go:**

```
Framework preference?
  ["Gin — fast, minimalist, most popular"]
  ["Echo — similar to Gin, more features built-in"]
  ["Fiber — Express-inspired, fast"]
  ["Chi — lightweight, idiomatic, composable"]
  ["Buffalo — Rails-like full framework"]
```

### Step 4: Database Decision

```
Database preference?
  ["PostgreSQL — relational, ACID, extensions, most versatile"]
  ["SQLite — embedded, zero-config, good for CLIs/desktop"]
  ["MySQL — relational, widely hosted, good for CMS"]
  ["MongoDB — document, flexible schema, Node ecosystem"]
  ["SQLite + Postgres — SQLite for dev, Postgres for prod (best DX)"]
  ["Help me choose based on data shape"]
```

If "Help me choose":

```
What best describes your data?
  ["Structured with relationships (users→orders→items)"] → PostgreSQL
  ["Flexible documents (profiles, configs, content)"] → MongoDB
  ["Time-series / event logs"] → TimescaleDB / ClickHouse
  ["Key-value / cache-heavy"] → Redis / DragonflyDB
```

### Step 5: Auth Decision

```
Auth approach?
  ["Built-in (NextAuth, Lucia, Django auth) — simple, self-hosted"]
  ["Third-party (Clerk, Auth0, Supabase) — feature-rich, paid at scale"]
  ["Session-based — traditional, server-side"]
  ["JWT — stateless, API-friendly"]
  ["OAuth/SSO — enterprise, social login"]
```

### Step 6: Deployment Decision

```
How will this be deployed?
  ["Vercel — Next.js/Nuxt/SvelteKit optimized, serverless"]
  ["Railway — simple deploy, databases included"]
  ["Fly.io — edge compute, global, Docker-native"]
  ["AWS (ECS/EKS/Lambda) — full control, complex"]
  ["Self-hosted (Docker/VPS) — maximum control, ops overhead"]
  ["Kubernetes — at scale, multi-service, complex"]
```

## Stack Templates (Quick Start)

| Template | Stacks |
|----------|--------|
| Web App (TS/JS) | Next.js + Prisma + PostgreSQL + Tailwind + Vercel |
| Web App (Python) | FastAPI + SQLAlchemy + PostgreSQL + React + Railway |
| API (TS) | Express/Fastify + Prisma + PostgreSQL + Railway |
| API (Go) | Gin + sqlx + PostgreSQL + Docker |
| CLI (Rust) | clap + anyhow + serde + cargo |
| CLI (Go) | cobra + viper + Docker |
| Mobile (TS) | React Native + Expo + Supabase + EAS |
| Desktop (Rust) | Tauri + React + SQLite |

## Red Flags — STOP

Recommending without asking project type first. Recommending without checking if they have team experience. Guessing versions instead of verifying. "Use what I know" instead of "use what fits."

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Everyone uses React, recommend it" | React is popular but not always the right choice. |
| "I know Node, so recommend it" | The project might need Go or Rust. |
| "I'll just say the latest version" | Verify it. Last month's version may be outdated. |
| "The stack doesn't matter that much" | Stack choice affects every decision for years. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "We're not using React, we told you that" — You recommended based on your familiarity, not the project's stated language preference
- "That framework is overkill for this" — You over-fit to an enterprise or popular-trend stack instead of matching the stated scope
- "We're not deploying to the cloud" — You skipped or ignored the deployment decision step
- "Is that version still current?" — You stated a version from training data without verifying via web search
- "Why did you pick that without asking?" — You chose from a template without walking through the decision flow with the user

**When you see these:** STOP. Return to the relevant Stack Selection Flow step, ask the missing question, and re-derive the recommendation from the user's actual answers.

## Related Skills

- **grill** — provides project type + scope this skill needs
- **architecture-planner** — uses stack decision for detailed architecture
- **version-checker** — verify latest stable versions before recommending

## Verification

- [ ] Project type determined
- [ ] Language chosen (or user approved recommendation)
- [ ] Framework chosen with rationale
- [ ] Database chosen with rationale
- [ ] Auth approach decided
- [ ] Deployment platform decided
- [ ] All versions verified (web search for latest stable)
