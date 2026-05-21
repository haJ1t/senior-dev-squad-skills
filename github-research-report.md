# GitHub Research: Agent Skill Packs, Claude Code Plugins, MCP Collections & AI Agent Frameworks

## EXECUTIVE SUMMARY

Searched GitHub across 8+ query categories. Analyzed 100+ repos. Identified 30+ innovation sources organized by category below. The key finding: the existing senior-dev-squad-skills is strong on code quality enforcement but missing entire categories that other repos have pioneered.

---

## CATEGORY 1: MEGA-SCALE SKILL LIBRARIES (1,000+ skills)

### 1. ECC (★186,947) — affaan-m/ECC
**URL:** https://github.com/affaan-m/ECC
**Scale:** 232+ skill directories, GitHub App, npm packages
**Unique features NOT in senior-dev-squad:**
- **Instincts system** — Always-on guardrails that run automatically, not skill-invoked rules. Covers repo memory preservation, context window management, git hygiene.
- **AgentShield** — Security scanning that monitors agent behavior for prompt injection, data exfiltration, credential leaks
- **Continuous Learning System** — Agents that learn from past mistakes and improve over time
- **Agent Introspection & Debugging** — Skills that inspect an agent's own reasoning, decisions and state
- **Agentic OS** — Skills for agent-to-agent communication, filesystem management, process lifecycle
- **Agent Payment (X402)** — Skills for decentralized AI payment protocols
- **Canary Watch** — Continuous monitoring & regression detection for agent outputs
- **Research-First Development** — Skills that compile context, search web, synthesize findings before coding
- **Cross-harness architecture** — Works identically across Claude Code, Codex, Cursor, OpenCode, Gemini, Zed, Copilot
- **GitHub App integration** — PR audits, automated fixes, commit tracking

### 2. Antigravity Awesome Skills (★37,996) — sickn33/antigravity-awesome-skills
**URL:** https://github.com/sickn33/antigravity-awesome-skills
**Scale:** 1,460+ skills, bundles, workflows, npm CLI installer
**Unique features:**
- **npx installer** — `npx antigravity-awesome-skills` installs everything
- **Plugin-safe distributions** — Skills packaged for Claude Code plugins, Codex, Cursor, Gemini CLI
- **Role-based bundles** — Pre-configured skill bundles by role (developer, tester, PM, marketer)
- **Workflow-driven execution** — Chained skills that execute in sequence for complete tasks
- **V11.3.0, 38K+ stargazers** — Most comprehensive curated collection

### 3. VoltAgent/awesome-agent-skills (★22,280)
**URL:** https://github.com/VoltAgent/awesome-agent-skills
**Scale:** 1,000+ skills, curated collection
**Unique features:** Compatible with Claude Code, Codex, Gemini CLI, Cursor, and more. Well-organized catalog format.

---

## CATEGORY 2: SUBAGENT ORCHESTRATION & MULTI-AGENT SYSTEMS

### 4. Oh-My-Pi (★4,947) — can1357/oh-my-pi
**URL:** https://github.com/can1357/oh-my-pi
**Unique features NONE of the others have:**
- **Hash-anchored edits** — Edits verified by content hashing, eliminating hallucinated diffs
- **Optimized tool harness** — Custom Rust core (~27k lines) with 32 built-in tools
- **13 LSP ops, 27 DAP ops** — Full IDE-level language server + debug adapter integration
- **Benchmaxxed tools** — Measured performance improvements (e.g., 6.7% → 68.3% edit success rate)
- **Persistent Python + Bun workers** — Code execution kernels that can call back into agent tools
- **Multi-provider support** — 40+ LLM providers with per-model prompt tuning
- **Subagent system** — Parallel subagent execution, mid-run steering

### 5. Apra Fleet (★39) — Apra-Labs/apra-fleet
**URL:** https://github.com/Apra-Labs/apra-fleet
**Unique features:**
- **Cross-provider agent teams** — Claude agent and Gemini agent work same sprint, one writes other reviews
- **Doer-reviewer loop** — Built-in code writing → review → fix cycle across different AI models
- **SSH fleet** — Spread agents across every machine on your network
- **MCP-native** — Runs as an MCP server, integrates with any MCP-compatible client
- **PM skill** — Built-in project management workflow for multi-agent sprints

### 6. Maestro Orchestrate (★420) — josstei/maestro-orchestrate
**URL:** https://github.com/josstei/maestro-orchestrate
**Unique features:**
- **39 specialized specialists** — Pre-defined agent roles
- **Parallel subagents** — Run multiple agents simultaneously
- **Persistent sessions** — Agent state persists across sessions
- **Multi-harness** — Works with Gemini CLI, Claude Code, Codex, Qwen Code

### 7. Pi Subagents (★331) — tintinweb/pi-subagents
**URL:** https://github.com/tintinweb/pi-subagents
**Unique features:** Sub-agents with Claude Code look-and-feel, parallel execution, live widget, custom agent types, mid-run steering

---

## CATEGORY 3: AGENT PLATFORMS & MANAGED WORKFORCE

### 8. Multica (★29,452) — multica-ai/multica
**URL:** https://github.com/multica-ai/multica
**Unique features:**
- **Agents as Teammates** — Assign issues to agents like colleagues; agents have profiles, show on boards, post comments
- **Squads** — Group agents under a leader that delegates work
- **Full task lifecycle** — Enqueue, claim, start, complete/fail with WebSocket streaming
- **Reusable Skills** — Every solution becomes a reusable skill for the whole team
- **Open-source managed agents platform** — Vendor-neutral, self-hosted

### 9. PraisonAI (★7,837) — MervinPraison/PraisonAI
**URL:** https://github.com/MervinPraison/PraisonAI
**Unique features:**
- **24/7 AI Workforce** — Hire autonomous self-improving agents
- **5 lines of code to deploy** — Lightweight core SDK
- **MCP-native** — Registered in MCP registry
- **Dashboard + AgentFlow** — Visual agent orchestration
- **Self-improving agents** — Agents that research, plan, and execute tasks autonomously

---

## CATEGORY 4: PLAN-FIRST & APPROVAL-BASED AGENT FRAMEWORKS

### 10. OpenAgentsControl (★4,064) — darrenhinde/OpenAgentsControl
**URL:** https://github.com/darrenhinde/OpenAgentsControl
**Unique features:**
- **Pattern Control** — Agents learn YOUR coding patterns and reuse them
- **Approval Gates** — Agents ALWAYS request approval before execution (Propose → Approve → Execute)
- **Editable Agents** — Markdown files for agent behavior, no compilation needed
- **MVI (Minimal Viable Information)** — Context files <200 lines, lazy loading for token efficiency
- **Multi-language** — TypeScript, Python, Go, Rust, C#
- **Model Agnostic** — Claude, GPT, Gemini, MiniMax, local models

---

## CATEGORY 5: AUTONOMOUS REPO MAINTENANCE

### 11. Auto-Maintainer (★49) — yazinsai/auto-maintainer
**URL:** https://github.com/yazinsai/auto-maintainer
**Unique features:**
- **Write rules in plain Markdown** — No DSLs, no YAML schemas
- **Fully autonomous** — Triage issues, review PRs, fix bugs, merge code, cut releases
- **Secure by design** — Triage bot can't touch code, actions pinned to commit SHAs
- **npx auto-maintainer init** — One command setup

### 12. Oh-My-PR (★40) — yungookim/oh-my-pr
**URL:** https://github.com/yungookim/oh-my-pr
**Unique features:**
- **Local-first PR babysitter** — Watches PRs, reads review feedback + CI failures
- **Isolated worktrees** — Fixes in isolated git worktrees, pushes back
- **Dashboard** — Real-time PR status dashboard

### 13. SuperClaude (★327) — gwendall/superclaude
**URL:** https://github.com/gwendall/superclaude
**Unique features:** GitHub workflow superpowers — transforms "fix stuff" commits into professional messages, intelligent changelogs

---

## CATEGORY 6: DESIGN & CREATIVE SYSTEMS

### 14. Open Design (★46,099) — nexu-io/open-design
**URL:** https://github.com/nexu-io/open-design
**Scale:** 31 skills, 72+ design systems, 131 total skills
**Unique features:**
- **Agent-native design** — 16 coding-agent CLIs become the design engine
- **72 brand-grade Design Systems** — Pre-built design systems (Material, Shadcn, IBM Carbon, etc.)
- **31 composable Skills** — Design-specific skills for UI generation, branding, layout
- **Local-first, BYOK** — No cloud dependency
- **Alternative to Claude Design / Figma** — Unique category entirely missing from senior-dev-squad

---

## CATEGORY 7: SPECIALIZED DOMAIN SKILL PACKS

### 15. Anthropic Cybersecurity Skills (★6,457) — mukul975/Anthropic-Cybersecurity-Skills
**URL:** https://github.com/mukul975/Anthropic-Cybersecurity-Skills
**Scale:** 754 skills, 26 security domains, 5 framework mappings
**Unique features:**
- **Mapped to MITRE ATT&CK, NIST CSF 2.0, MITRE ATLAS, D3FEND, NIST AI RMF**
- **26 security domains** — Far beyond OWASP Top 10 (DFIR, threat intel, cloud security, binary analysis)
- **Digital forensics** — Volatility3 memory dump analysis, forensic artifacts
- **Purple teaming** — Both offensive and defensive security perspectives
- **Sigma rules detection** — Detection engineering skills

### 16. Product Manager Skills (★4,379) — deanpeters/Product-Manager-Skills
**URL:** https://github.com/deanpeters/Product-Manager-Skills
**Scale:** 49 skills, 6 commands
**Unique features:**
- **Battle-tested PM frameworks** — Teresa Torres, Geoffrey Moore, Amazon, MITRE
- **Opportunity solution trees** — Structured product discovery
- **Validation experiment design** — Kill bad bets fast
- **Non-technical PM support** — Claude Desktop, Claude Code, Cursor, Codex, n8n

### 17. Marketing Skills (★29,435) — coreyhaines31/marketingskills
**URL:** https://github.com/coreyhaines31/marketingskills
**Unique features:** CRO, copywriting, SEO, analytics, growth engineering

### 18. SEO & GEO Skills (★1,680) — aaron-he-zhu/seo-geo-claude-skills
**URL:** https://github.com/aaron-he-zhu/seo-geo-claude-skills
**Scale:** 20 skills
**Unique features:** SEO + Generative Engine Optimization (GEO), keyword research, technical audits, rank tracking, CORE-EEAT

### 19. Social AI Team (★114) — stevenflanagan1/social-ai-team
**URL:** https://github.com/stevenflanagan1/social-ai-team
**Unique features:** Complete AI social media team — brand setup, content calendar, captions, creative, performance review

---

## CATEGORY 8: MCP SERVER COLLECTIONS & TOOLS

### 20. Awesome MCP Servers (★87,149) — punkpeye/awesome-mcp-servers
**URL:** https://github.com/punkpeye/awesome-mcp-servers
**Scale:** Largest MCP server directory

### 21. MCP Security Hub (★552) — FuzzingLabs/mcp-security-hub
**URL:** https://github.com/FuzzingLabs/mcp-security-hub
**Scale:** 38 MCP servers, 300+ tools
**Unique features:**
- **Dockerized security tools as MCP servers** — Nmap, Nuclei, Ghidra, SQLMap, Hashcat
- **38 production-hardened MCPs** — Non-root containers, Trivy-scanned minimal images
- **CI/CD ready** — Docker Compose orchestration, GitHub Actions build/scan

### 22. IBM MCP (★378) — IBM/mcp
**URL:** https://github.com/IBM/mcp
**Unique features:** Enterprise MCP servers, clients, and dev tools from IBM

### 23. GitHub Copilot Plugins (★264) — github/copilot-plugins
**URL:** https://github.com/github/copilot-plugins
**Unique features:** Official MCP servers, skills, hooks for GitHub Copilot

### 24. Agentic AI APIs (★316) — cporter202/agentic-ai-apis
**URL:** https://github.com/cporter202/agentic-ai-apis
**Scale:** 2,396 production-ready APIs
**Unique features:** Categorized API directory for agents (604 Agents APIs, AI Models, MCP Servers)

---

## CATEGORY 9: ENGINEERING FOUNDATIONS

### 25. Open Mercato (★1,315) — open-mercato/open-mercato
**URL:** https://github.com/open-mercato/open-mercato
**Unique features:**
- **Architecture-aware AI harness** — Agents know where in the project to place code
- **Ready-made CRM/ERP domain modules** — Start at 80% done (unlike senior-dev-squad's spec-first approach)
- **Specs ship with the repo** — Reproducible AI output via spec files
- **Teachable framework** — Whole team enters AI-assisted dev

### 26. Harness Craft (★86) — YuxiaoWang-520/harness-craft
**URL:** https://github.com/YuxiaoWang-520/harness-craft
**Scale:** 46 skills, 15 rules
**Unique features:**
- **Repo memory** — Agents that remember the repo across sessions
- **Long-horizon execution** — Skills for multi-step, multi-session work
- **Multi-agent coordination** — Rules for multiple agents working simultaneously
- **Evidence for delivery** — Verification artifacts, not just "done" claims
- **46 skills for depth** — Focused on system stability, not just code generation

---

## CATEGORY 10: ECOSYSTEM DIRECTORIES & OFFICIAL SKILLS

### 27. Anthropic Official Skills (★137,431) — anthropics/skills
**URL:** https://github.com/anthropics/skills
**Unique features:** Official skills from Anthropic, includes docx/pdf/pptx/xlsx document creation skills (source-available)

### 28. Addy Osmani Agent Skills (★43,634) — addyosmani/agent-skills
**URL:** https://github.com/addyosmani/agent-skills
**Scale:** 7 slash commands, production-grade
**Unique features:** /spec → /plan → /build → /test → /review → /code-simplify → /ship pipeline, but simpler than senior-dev-squad

### 29. ComposioHQ Awesome Claude Skills (★60,615) — ComposioHQ/awesome-claude-skills
**URL:** https://github.com/ComposioHQ/awesome-claude-skills
**Scale:** 1,000+ skills
**Unique features:** Connects Claude to 500+ apps (Slack, Gmail, Jira, etc.) via Composio plugin — real actions, not just text generation

### 30. Awesome CursorRules (★39,577) — PatrickJS/awesome-cursorrules
**URL:** https://github.com/PatrickJS/awesome-cursorrules
**Unique features:** Curated .cursorrules files organized by tech stack (React, Python, Go, etc.)

---

## GAPS IDENTIFIED vs senior-dev-squad-skills

| # | What's Missing | Found In | Innovation Score |
|---|---------------|----------|------------------|
| 1 | **Instincts/Always-on guardrails** (auto rules, not skill-invoked) | ECC, Harness Craft | 🔥 HIGH |
| 2 | **AgentShield / runtime security monitoring** | ECC | 🔥 HIGH |
| 3 | **Continuous learning / session memory** | ECC, Phantom, Harness Craft | 🔥 HIGH |
| 4 | **Agent introspection & debugging skills** | ECC | 🔥 HIGH |
| 5 | **Subagent orchestration / parallel agents** | Oh-My-Pi, Apra Fleet, Maestro, Pi Subagents | 🔥 HIGH |
| 6 | **Autonomous repo maintenance** (triage, fix, merge, release) | Auto-Maintainer, Oh-My-PR | 🔥 HIGH |
| 7 | **Hash-anchored / verified edits** | Oh-My-Pi | 🔥 HIGH |
| 8 | **Cross-provider agent teams** (Claude + Gemini review each other) | Apra Fleet | 🔥 HIGH |
| 9 | **Managed agents platform** (assign issues to agents like teammates) | Multica | 🔥 HIGH |
| 10 | **24/7 AI workforce deployment** (5 lines of code) | PraisonAI | 🔥 HIGH |
| 11 | **Pattern control / approval gates** | OpenAgentsControl | 🔥 HIGH |
| 12 | **Agent-native design system** (72 design systems) | Open Design | 🔥 HIGH |
| 13 | **Cybersecurity skills mapped to 5 frameworks** (754 skills) | Anthropic Cybersecurity Skills | 🔥 HIGH |
| 14 | **Product management frameworks** (opportunity trees, validation) | Product Manager Skills | 🔥 HIGH |
| 15 | **Marketing / SEO / GEO skills** | Marketing Skills, SEO-GEO Skills | 🔥 HIGH |
| 16 | **Social media AI team** | Social AI Team | MEDIUM |
| 17 | **MCP server collections** (38+ security tools as MCPs) | MCP Security Hub, MCP for Security | 🔥 HIGH |
| 18 | **GitHub App / PR automation** | ECC, Auto-Maintainer, Oh-My-PR | 🔥 HIGH |
| 19 | **Agent payment protocols** (X402) | ECC | MEDIUM |
| 20 | **Canary Watch / regression detection** | ECC | MEDIUM |
| 21 | **npx installer & bundle system** | Antigravity | MEDIUM |
| 22 | **Architecture-aware placement** (not just code generation) | Open Mercato | 🔥 HIGH |
| 23 | **Ready-made domain modules** (CRM, ERP as starting point) | Open Mercato | 🔥 HIGH |
| 24 | **Research-first development skills** (compile context before coding) | ECC | 🔥 HIGH |
| 25 | **SSH fleet / distributed agent execution** | Apra Fleet | MEDIUM |

---

## TOP 10 INNOVATIONS TO STEAL / ADAPT

1. **Instincts system** from ECC — Always-on guardrails that prevent agents from ignoring rules
2. **Subagent orchestration** from Oh-My-Pi / Apra Fleet — Parallel execution, cross-model review, doer-reviewer loop
3. **Agent memory / session continuity** from ECC & Harness Craft — Agents remember repo context across sessions
4. **Approval gates** from OpenAgentsControl — Plan-first workflow with human-in-the-loop verification
5. **Autonomous PR maintenance** from Auto-Maintainer & Oh-My-PR — Self-healing repos
6. **Managed agent platform** from Multica — Task assignment, progress tracking, skill reuse
7. **Security framework mapping** from Anthropic Cybersecurity Skills — MITRE/NIST-aligned security skills
8. **Agent-native design system** from Open Design — 72 design systems, 131 composable skills
9. **MCP-as-tool infrastructure** from MCP Security Hub — Dockerized security tools as agent tools
10. **Pattern control** from OpenAgentsControl — Code patterns that agents learn and reuse

---

## TOP REPOS TO WATCH (by unique innovation, not just stars)

| Repo | Stars | Innovation Density | Best For |
|------|-------|-------------------|----------|
| ECC | 186K | ⭐⭐⭐⭐⭐ | Everything — the gold standard |
| Oh-My-Pi | 4.9K | ⭐⭐⭐⭐⭐ | Subagents, hash-verified edits, tool optimization |
| Open Design | 46K | ⭐⭐⭐⭐⭐ | Visual/design skills (completely missing from your pack) |
| Apra Fleet | 39 | ⭐⭐⭐⭐ | Cross-model agent teams, SSH fleet |
| Multica | 29K | ⭐⭐⭐⭐ | Managed agent workforce platform |
| Anthropic Cybersecurity | 6.4K | ⭐⭐⭐⭐ | 754 framework-mapped security skills |
| Auto-Maintainer | 49 | ⭐⭐⭐⭐ | Autonomous repo maintenance |
| OpenAgentsControl | 4K | ⭐⭐⭐⭐ | Pattern control + approval gates |
| PraisonAI | 7.8K | ⭐⭐⭐ | 24/7 AI workforce |
| Open Mercato | 1.3K | ⭐⭐⭐ | Architecture-aware foundation framework |
| Harness Craft | 86 | ⭐⭐⭐ | Repo memory, multi-agent coordination |

---

## FILES CREATED

This research report was written to:
/Users/halitozger/Desktop/megaskills/senior-dev-squad-skills/github-research-report.md

(alongside the existing gap-analysis-project-architect.md)

---

## METHODOLOGY

Searched using GitHub REST API (via curl with authentication) for 10+ query strings:
- "claude code skill", "MCP server collection", "ai coding agent framework"
- "agent skill pack OR claude-code-plugin"
- "subagent orchestration OR autonomous coding agent"
- "cursor rules OR .cursorrules"
- "AI code review automation"
- "multi-agent coding workflow"
- "ai documentation generator agent skill"

Analyzed 100+ repository READMEs. Extracted unique features not present in the user's existing skill pack. Verified against the gap-analysis document to avoid duplication of effort (the 13 project-architect gaps are already documented separately).
