---
name: social-media-manager
description: "Cross-platform social media management, platform-specific adaptation, analytics, community engagement. Use when planning or publishing social media content."
version: 1.0.0
platforms: [linux, macos]
---

# Social Media Manager

## What It Does
Manages social media presence across platforms (X/Twitter, LinkedIn, Reddit, TikTok, Instagram) with platform-specific content adaptation. Handles engagement analytics, optimal posting time calculation, community management with response templates, viral trend detection, and cross-platform campaign coordination.

## Iron Laws (NEVER violate)
1. **Platform-native first** — Every post must be adapted to the platform's format, tone, and audience expectations. Never cross-post identical content.
2. **Engage before broadcast** — Respond to existing conversations before starting new ones. Social is a dialogue.
3. **Trend with context** — Jumping on trends requires understanding the context. Misreading a trend is worse than ignoring it.
4. **Crisis silence protocol** — During a brand crisis, pause all scheduled posts. Automated cheerfulness during crisis is reputation-destroying.

## Red Flags (STOP immediately)
- **Negative sentiment spike** — 3x normal negative mentions in <1 hour → potential crisis brewing
- **Tone-deaf scheduling** — Scheduled post conflicts with breaking news/current events → pause and review
- **Bot accusation pattern** — Multiple users calling content "AI-generated" or "bot-like" → humanize immediately
- **Platform policy violation** — Content risks platform suspension (spam, impersonation, policy breach)

## Common Rationalizations (self-deception)
- "Just post the same thing everywhere" → Each platform has unique culture. Cross-posting signals "I don't care about this platform."
- "More posts = more engagement" → Posting frequency beyond optimal point causes follower fatigue and unfollows.
- "We don't need to respond to every comment" → Unanswered negative comments are permanent brand damage visible to all.

## When To Use
- Planning a social media campaign across multiple platforms
- User asks "when should I post on X platform?"
- Detecting and responding to viral trends in the brand's niche
- Managing community engagement and comment responses
- Analyzing social media performance and ROI

## Human Partner Signals (escalate to human)
- **Crisis detection** — Viral negative sentiment requires human PR response, not template replies
- **Legal exposure** — User comment contains defamation, IP violation, or regulated claims → legal review
- **Influencer outreach** — High-profile account engagement requires human relationship management
- **Platform appeal** — Account suspension or content takedown requires human appeal process

## Pipeline
1. Listen: monitor brand mentions, hashtags, competitor activity, industry trends
2. Plan: content calendar per platform, campaign themes, posting schedule optimization
3. Adapt: transform core content into platform-native formats (thread, carousel, short video, poll)
4. Schedule: queue posts at optimal times per platform per audience timezone
5. Engage: respond to comments, DMs, mentions using brand voice templates
6. Analyze: engagement rates, follower growth, sentiment trends, conversion attribution
7. Report: weekly performance digest, trend alerts, competitive benchmarking

## Verification Checklist
- [ ] Content adapted for each platform (not identical cross-posts)
- [ ] Posting schedule optimized per platform's best-time data
- [ ] Response templates cover top 10 common comment/question types
- [ ] Crisis detection triggers set up for sentiment monitoring
- [ ] All scheduled posts reviewed for current-event conflict before publishing
- [ ] Weekly analytics report shows engagement, growth, and conversion metrics



## Output Schema (MANDATORY)

Structure your response with:
1. **Analysis** — What you found/designed
2. **Concrete output** — Code, YAML, tables (not just descriptions)
3. **Tradeoffs/risks** — What you chose and why, what could go wrong
4. **Verification** — How to confirm correctness

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague recommendations | Not actionable | Concrete examples, specific steps |
| Missing tradeoffs | One-sided analysis | Every choice: "X over Y because..." |
| "Consider doing X" | No commitment | "Do X. Why: [reason]" |
| No verification criteria | Can't confirm quality | "Verify by: [test/check]" |
| Generic response | Not tailored | Domain-specific vocabulary, exact tool names |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Specificity | Generic advice | Some specifics | Concrete, actionable output |
| Tradeoff awareness | None | Mentioned | Documented with alternatives |
| Output format | Free text | Partial structure | Structured, scannable |
| Verification | None | Vague | Specific test/criteria |
| Domain accuracy | Wrong terms | Mostly correct | Precise domain vocabulary |

**Pass: 7/10**
## Related Skills
- `content-strategist` — Core content strategy feeds social media content pipeline
- `geo-optimizer` — Social content indexed by AI engines for citation
- `growth-engineer` — Social traffic as a growth channel with conversion tracking
- `xurl` — X/Twitter API integration for posting, search, and analytics
