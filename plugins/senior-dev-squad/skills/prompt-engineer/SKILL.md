---
name: prompt-engineer
description: "Systematic prompt design, optimization, and evaluation framework for LLM applications. Use when crafting or improving prompts for AI systems."
version: 1.0.0
platforms: [linux, macos]
---

# Prompt Engineer

## What It Does
Applies engineering rigor to prompt design — treating prompts as code that can be versioned, tested, optimized, and deployed. Provides a systematic framework for prompt iteration (draft → test → measure → refine), evaluation against defined quality metrics, and production prompt management with A/B testing and rollback capabilities.

## Iron Laws (NEVER violate)
1. **Prompt is code** — Treat prompts with the same rigor as production code: version control, code review, testing, and CI/CD.
2. **Measure before optimize** — Establish baseline metrics before attempting optimization. You can't improve what you don't measure.
3. **Test on diverse inputs** — Evaluate prompts against a curated test set covering happy path, edge cases, adversarial inputs, and diverse demographics.
4. **No prompt injection vectors** — Every prompt must be reviewed for injection vulnerabilities. User input and system instructions must have clear boundaries.

## Red Flags (STOP immediately)
- **Prompt regression** — Optimization improves one metric but degrades another critical metric → tradeoff decision needed
- **Overfitting to test set** — Prompt performs perfectly on test set but fails on new inputs → prompt is memorizing, not generalizing
- **Token bloat** — Prompt grows 50%+ during optimization without proportional quality improvement → refactor for conciseness
- **Injection surface expanded** — New prompt structure introduces new injection vectors → security regression

## Common Rationalizations (self-deception)
- "The prompt works, no need for testing" → Prompts break silently on edge cases. Test like any other code.
- "Longer prompts are better prompts" → Verbosity often degrades performance. Concise, well-structured prompts outperform bloated ones.
- "I'll just tweak it until it feels right" → Vibes-based optimization is slow and unreliable. Measure systematically.

## When To Use
- Designing prompts for production LLM applications
- Optimizing existing prompts for cost, latency, or quality
- Setting up prompt evaluation pipelines
- A/B testing prompt variations
- Migrating prompts between models (different models need different prompt structures)

## Human Partner Signals (escalate to human)
- **Ethical output concern** — Prompt produces biased, harmful, or misleading outputs → ethics review
- **Cost-quality tradeoff** — Optimal quality prompt is 3x more expensive → business decision
- **Model-specific lock-in** — Prompt only works on one provider → strategic decision on vendor lock-in
- **User-facing prompt** — End-users see and interact with this prompt → UX review needed

## Pipeline
1. Define: specify task, success criteria, quality metrics, and constraints (latency, cost, token budget)
2. Draft: create initial prompt with clear structure — role, context, instructions, format, examples
3. Test: evaluate against curated test set; measure accuracy, relevance, safety, consistency
4. Optimize: iterate using techniques — few-shot examples, chain-of-thought, structured output, self-consistency
5. Validate: security review for injection, bias audit, edge case coverage check
6. Deploy: version the prompt, set up monitoring, configure A/B test if comparing variants
7. Monitor: track quality metrics in production, detect drift, trigger re-optimization

## Verification Checklist
- [ ] Prompt versioned in source control with descriptive commit messages
- [ ] Test set covers happy path, edge cases, adversarial inputs, and diverse demographics
- [ ] Baseline metrics established before optimization begins
- [ ] Prompt injection review completed (user input boundaries clearly defined)
- [ ] A/B test configured for prompt variants with success criteria
- [ ] Production monitoring tracks quality drift and triggers alerts

## Related Skills
- `model-evaluator` — Prompt quality is measured by model evaluation frameworks
- `rag-architect` — RAG prompts require specialized structure for context injection
- `dataset-curator` — Test sets for prompt evaluation are curated datasets
- `dspy` — Programmatic prompt optimization framework
