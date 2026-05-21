---
name: geo-optimizer
description: "Generative Engine Optimization for AI search — optimize content for ChatGPT, Perplexity, Gemini. Use when optimizing content for AI-powered search visibility."
version: 1.0.0
platforms: [linux, macos]
---

# GEO Optimizer (Generative Engine Optimization)

## What It Does
Optimizes content for AI-powered search engines (ChatGPT, Perplexity, Gemini, Copilot) — the emerging "answer engine" paradigm. Goes beyond traditional SEO by optimizing for LLM consumption: structured data markup, entity optimization, citation-worthiness scoring, and AI search ranking monitoring. The goal is to be the source that AI engines cite in their answers.

## Iron Laws (NEVER violate)
1. **Citeable structure** — Every claim must be backed by data in an easily extractable format. AI engines cite what they can parse.
2. **Entity clarity** — Entities (people, products, companies, concepts) must be unambiguously defined with schema markup.
3. **Freshness signal** — Content must show last-updated timestamps. AI engines heavily weight recency.
4. **No cloaking** — Content served to AI crawlers must match what humans see. Cloaking = black hat = delisting.

## Red Flags (STOP immediately)
- **Hallucination bait** — Vague or contradictory statements that LLMs might misinterpret → rewrite for precision
- **Unstructured data** — Key facts buried in prose without schema markup → invisible to AI extractors
- **Duplicate entity confusion** — Same entity referenced with different names across pages → normalize
- **Citation drift** — AI engine cites your content but misrepresents the claim → file correction

## Common Rationalizations (self-deception)
- "Good SEO is enough for AI search" → AI engines don't use PageRank. They use entity understanding and citation graphs.
- "AI crawlers will figure it out" → Without structured data, your content is invisible to LLM extractors.
- "GEO is just a buzzword" → ChatGPT alone drives 100M+ weekly queries. Ignoring it is ignoring a search engine.

## When To Use
- Content that should appear in AI-generated answers (how-to, definitions, comparisons)
- User wants to track AI search visibility for their brand/topics
- Optimizing existing content for LLM consumption
- Checking if competitors are being cited by AI engines more than you
- Setting up structured data (schema.org) for entity optimization

## Human Partner Signals (escalate to human)
- **Black-hat temptation** — User suggests keyword stuffing or cloaking for AI → educate on risks
- **Brand misrepresentation** — AI engine consistently misattributes claims to your brand → PR issue
- **Competitive vulnerability** — Competitor dominates AI citations in your category → strategic threat
- **Technical implementation** — Schema markup requires CMS/dev changes → coordinate with engineering

## Pipeline
1. Audit: check current AI search visibility (what do ChatGPT/Perplexity say about your topics?)
2. Analyze: identify citation gaps — where should you be cited but aren't?
3. Structure: add schema.org markup (Article, FAQ, HowTo, Product, Organization)
4. Optimize: rewrite content for extractability — clear claims, data-backed, unambiguous entities
5. Monitor: track AI citation rates, entity recognition accuracy, ranking changes
6. Iterate: A/B test content structures, double down on cited formats

## Verification Checklist
- [ ] All key pages have schema.org structured data (Article, FAQ, or HowTo)
- [ ] Entity references are consistent across all pages (same name, same schema)
- [ ] Every factual claim has an inline citation or data source
- [ ] Last-updated timestamps present and accurate on all content pages
- [ ] AI citation monitoring set up for top 10 target keywords
- [ ] Competitor AI citation analysis completed for main competitors

## Related Skills
- `content-strategist` — GEO builds on SEO content strategy foundations
- `growth-engineer` — AI search traffic is a growth channel to measure and optimize
- `social-media-manager` — AI engines increasingly index social content for citations
- `competitive-agent-research` — Monitor competitors' AI search presence
