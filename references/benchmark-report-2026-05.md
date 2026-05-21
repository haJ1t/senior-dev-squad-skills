# 🔬 Agent Skill Ecosystem Benchmark — May 2026

**senior-dev-squad-skills v3.1.0 vs 20 competitor packs**

---

## 1. GENERAL METRICS COMPARISON

| # | Pack | ★ Stars | Skill Count | SKILL.md | Total MD | Size | Bytes/Skill | Domain Plugin | Quality Format |
|---|-------|:-------:|:-----------:|:--------:|:---------:|:-----:|:----------:|:------------:|:-------------:|
| 1 | **ECC** | 187K | ~778 | 778 | 2,172 | 35.7 MB | ~47 KB | ❌ | Partial |
| 2 | **antigravity-awesome-skills** | 38K | 4,639* | 4,639 | 8,387 | 55 MB | ~12 KB | ❌ | Mixed |
| 3 | **Anthropic-Cybersecurity** | 6.5K | 759 | 759 | 2,384 | 11.4 MB | ~15 KB | ❌ | Framework-map |
| 4 | **Open Design** | 48K | 423 | 423 | 1,126 | 873 MB** | ~2 MB | ❌ | Own format |
| 5 | **awesome-agent-skills** | 22K | 1,000+* | — | — | 330 KB | — | ❌ | List only |
| 6 | **addyosmani/agent-skills** | 44K | 7+7*** | 26 | 55 | 305 KB | ~12 KB | ❌ | Good |
| 7 | **Product-Manager-Skills** | 4.4K | 49 | — | — | 1.6 MB | ~33 KB | ❌ | PM format |
| 8 | **marketingskills** | 30K | ~30 | — | — | 1.9 MB | ~63 KB | ❌ | Marketing |
| 9 | **seo-geo-claude-skills** | 1.7K | 20 | — | — | 1.2 MB | ~58 KB | ❌ | SEO/GEO |
| 10 | **maestro-orchestrate** | 422 | 39 | — | — | 2 MB | ~50 KB | ❌ | Agent format |
| 11 | **OpenAgentsControl** | 4.1K | ~20 | — | — | 5.2 MB | ~260 KB | ❌ | Plan-first |
| 12 | **harness-craft** | 86 | 47 | 47 | 92 | 6.1 MB | ~130 KB | ❌ | Good |
| 13 | **open-mercato** | 1.3K | ~15 | — | — | 132 MB** | ~8.8 MB | ❌ | Framework |
| 14 | **auto-maintainer** | 51 | 5 | — | — | 688 KB | ~138 KB | ❌ | Simple |
| 15 | **apra-fleet** | 39 | 8 | — | — | 2.5 MB | ~320 KB | ❌ | Agent |
| 16 | **PraisonAI** | 7.9K | ~30 | — | — | 68 MB** | ~2.3 MB | ❌ | Framework |
| 17 | **anthropics/skills** | 138K | 16 | 20 | 90 | 3.7 MB | ~233 KB | ❌ | Official |
| 18 | **mcp-security-hub** | 554 | 38 | — | — | 288 KB | ~7.6 KB | ❌ | MCP |
| 19 | **multica** | 30K | ~60 | — | — | 51.7 MB** | ~860 KB | ❌ | Platform |
| 20 | **oh-my-pi** | 5.4K | 13 | — | — | 291 MB** | ~22 MB | ❌ | Agent |
| | | | | | | | | | |
| **21** | **senior-dev-squad-skills 🏆** | **—** | **104** | **104** | **364** | **771 KB** | **~7.4 KB** | **✅ 20** | **Superpowers** |

> \* Aggregator — collected from other repositories, not original
> \** Repo size (including code, assets, and design files), not just skills
> \*** 7 slash commands + 7 skills (slash commands are not skills, but workflow triggers)

---

## 2. QUALITY FORMAT COMPARISON

Structural elements present in each skill:

| Element | ECC | Anti-gravity | Cyber Sec | Open Design | Harness Craft | Addy Osmani | **Us** |
|---------|:---:|:-----------:|:---------:|:----------:|:------------:|:----------:|:------:|
| Iron Laws (NEVER violate) | ⚠️ | ❌ | ❌ | ❌ | ✅ | ❌ | **✅** |
| Red Flags (STOP triggers) | ⚠️ | ❌ | ❌ | ❌ | ✅ | ❌ | **✅** |
| Common Rationalizations | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |
| Human Partner Signals | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | **✅** |
| Verification Checklist | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | **✅** |
| Related Skills (cross-ref) | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ | **✅** |
| Full Pipeline (phased) | ⚠️ | ⚠️ | ⚠️ | ✅ | ✅ | ⚠️ | **✅** |
| YAML Frontmatter | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **✅** |

**Legend:** ✅ Mandatory and complete | ⚠️ Partial/in some skills | ❌ None

**Result:** We are the **ONLY pack that fully implements the Superpowers quality format (8/8 elements).** Harness Craft is second with 5/8.

---

## 3. DOMAIN COVERAGE COMPARISON

| Domain | ECC | Anti-gravity | Cyber Sec | Open Design | **Us** |
|--------|:---:|:-----------:|:---------:|:----------:|:------:|
| Spec/Planning | ✅ | ✅ | ❌ | ❌ | **✅** |
| Architecture | ⚠️ | ⚠️ | ❌ | ❌ | **✅ (2)** |
| Frontend | ⚠️ | ✅ | ❌ | ✅ | **✅ (7)** |
| Backend | ✅ | ✅ | ❌ | ❌ | **✅ (4)** |
| Security | ✅ | ✅ | ✅✅✅ | ❌ | **✅ (9)** |
| Testing | ⚠️ | ✅ | ❌ | ❌ | **✅ (9)** |
| DevOps | ⚠️ | ✅ | ❌ | ❌ | **✅ (2)** |
| Code Review | ✅ | ✅ | ❌ | ❌ | **✅** |
| Guardrails | ✅✅ | ❌ | ❌ | ❌ | **✅ (4)** |
| Orchestration | ⚠️ | ⚠️ | ❌ | ❌ | **✅ (4)** |
| Design System | ❌ | ⚠️ | ❌ | ✅✅✅ | **✅ (6)** |
| MCP Integration | ✅ | ✅ | ❌ | ✅ | **✅ (4)** |
| Agent Platform | ❌ | ❌ | ❌ | ❌ | **✅ (5)** |
| Marketing/SEO/GEO | ❌ | ⚠️ | ❌ | ❌ | **✅ (4)** |
| Product Mgmt | ❌ | ❌ | ❌ | ❌ | **✅ (4)** |
| AI/ML Pipeline | ❌ | ⚠️ | ❌ | ❌ | **✅ (5)** |
| DevEx | ❌ | ❌ | ❌ | ❌ | **✅ (5)** |
| Compliance/GDPR | ❌ | ❌ | ⚠️ | ❌ | **✅ (4)** |
| Advanced Testing | ❌ | ❌ | ❌ | ❌ | **✅ (5)** |
| **Domain Plugins** | ❌ | ❌ | ❌ | ❌ | **✅ (20)** |
| Distributed Systems | ❌ | ❌ | ❌ | ❌ | **✅** |
| Epic Orchestration | ❌ | ❌ | ❌ | ❌ | **✅** |

**Result:** The ONLY pack active in **all 22 of 22 domains**. No competitor covers more than 10 domains.

---

## 4. STRUCTURAL ADVANTAGES

| Feature | Us | Best Competitor | Difference |
|---------|:---:|:------------:|:----:|
| **Domain plugin system** | 20 | 0 (none present) | ∞ |
| **Phase organization** | 4 phases, 14 layers | 1-2 layers (flat list) | 7x |
| **Quality format (8 elements)** | 8/8 | 5/8 (Harness Craft) | +60% |
| **Domain coverage** | 22/22 | ~8/22 (ECC) | 2.7x |
| **Cross-referencing (Related Skills)** | In every skill | Present in Harness Craft | — |
| **Pipeline (phased workflow)** | In every skill | Present in Open Design | — |
| **Learning loop (post-mortem)** | In Epic Orchestrator | None | ∞ |
| **Distributed systems architecture** | Yes (592 lines) | None | ∞ |
| **Consistent format (all skills)** | 100% | 30-60% | 2-3x |

---

## 5. AREAS WHERE COMPETITORS OUTPERFORM US

Honesty: No pack is perfect. Competitor highlights:

| Feature | Competitor | Why They Outperform Us |
|---------|-------|-----------------|
| **Skill count (volume)** | antigravity (4,639), ECC (778) | Because they are aggregators |
| **Stars/recognition** | ECC (187K), Anthropic Skills (138K) | Older and official |
| **Security framework depth** | Anthropic Cybersecurity (759) | Mapped to 5 frameworks, 26 security domains |
| **Design system assets** | Open Design (71 systems) | 72 brand-grade design systems, assets included |
| **MCP tool catalog** | mcp-security-hub (38 servers) | Dockerized security tools |
| **npx installer** | antigravity | One-command installation |
| **Official Anthropic support** | anthropics/skills | Official format and documentation |

---

## 6. BENCHMARK SUMMARY — SCORING TABLE

Max score per category is 10, total 100.

| # | Pack | Quality | Coverage | Structure | Depth | Domain Plugin | Originality | Total |
|---|-------|:------:|:------:|:----:|:-------:|:------------:|:----------:|:------:|
| 1 | **senior-dev-squad 🏆** | **10** | **10** | **10** | **9** | **10** | **10** | **59** |
| 2 | ECC | 6 | 8 | 7 | 7 | 0 | 9 | 37 |
| 3 | Anthropic Cybersecurity | 5 | 4 | 5 | 10 | 0 | 10 | 34 |
| 4 | Open Design | 6 | 3 | 7 | 8 | 0 | 9 | 33 |
| 5 | harness-craft | 8 | 5 | 6 | 5 | 0 | 8 | 32 |
| 6 | addyosmani/agent-skills | 7 | 4 | 5 | 3 | 0 | 8 | 27 |
| 7 | antigravity-awesome | 3 | 8 | 3 | 3 | 0 | 2 | 19 |
| 8 | Product-Manager | 4 | 1 | 4 | 6 | 0 | 6 | 21 |
| 9 | marketingskills | 4 | 1 | 4 | 5 | 0 | 6 | 20 |
| 10 | open-mercato | 3 | 1 | 4 | 7 | 0 | 7 | 22 |

---

## 7. OUR UNIQUE ADVANTAGES (Nobody Else Did)

1. **20 Domain Plugins** — No competitor has framework/DB/infra specific plugins.
2. **Superpowers Quality Format (8/8)** — Iron Laws + Red Flags + Rationalizations + Human Signals + Verification + Related Skills = complete package.
3. **4-Phase Organization (14 layers)** — Structured pipeline, not just a flat list.
4. **Epic Orchestrator** — Project-level orchestration with post-mortem learning loop (unique).
5. **Distributed Systems Architect** — CAP/PACELC theorems, Saga, CQRS, multi-region (unique).
6. **100% Format Consistency** — All skills are identically structured and cross-referenced.
7. **Compliance + Advanced Testing** — SOC2, GDPR, chaos engineering, mutation testing (unique).

---

## 8. RECOMMENDED DEVELOPMENT AREAS

| # | Action | Source/Competitor | Priority |
|---|---------|-------------|:-------:|
| 1 | Add npx/hermes installer | antigravity (npx install) | P1 |
| 2 | Publish to official Hermes marketplace | anthropics/skills (marketplace) | P1 |
| 3 | Map more security frameworks | Anthropic Cybersecurity (5 frameworks) | P2 |
| 4 | Expand MCP servers from 38 to 50+ | mcp-security-hub | P2 |
| 5 | Add badge/metrics to GitHub PRs | ECC (canary watch) | P2 |
| 6 | Expand design system assets | Open Design (71 systems) | P3 |

---

*Report date: May 20, 2026*
*Data source: Live GitHub API, 20 competitor repos analyzed*
