---
name: model-evaluator
description: "Systematic LLM and ML model evaluation — benchmarks, metrics, regression detection, and model comparison. Use when assessing or comparing AI model quality."
version: 1.0.0
platforms: [linux, macos]
---

# Model Evaluator

## What It Does
Provides a systematic framework for evaluating LLM and ML model performance. Supports standard benchmarks (MMLU, GSM8K, HumanEval, etc.), custom evaluation tasks, multi-dimensional metrics (accuracy, latency, cost, safety, fairness), regression detection across model versions, and head-to-head model comparison with statistical significance testing.

## Iron Laws (NEVER violate)
1. **Multi-metric only** — Never evaluate on a single metric. Minimum: quality + latency + cost + safety. Single-metric optimization is gaming.
2. **Statistical significance required** — "Model A beats Model B by 1%" without confidence intervals is noise. Always compute significance.
3. **Blind test set** — Evaluation test set must be unseen during development. No peeking, no tweaking after seeing results.
4. **Task-representative eval** — Evaluation tasks must match production use case. MMLU score is irrelevant for a code generation model.

## Red Flags (STOP immediately)
- **Benchmark contamination** — Training data overlaps with benchmark test set → results are invalid
- **Metric collapse** — All models score within 1% on a metric → metric is not discriminative; find better eval
- **Regression cascade** — New model beats old on 3 metrics but catastrophically fails on 1 critical metric → not deployable
- **Overfitting to eval** — Model improves on benchmarks but degrades in production → eval doesn't match reality

## Common Rationalizations (self-deception)
- "This benchmark score is good enough" → Benchmarks measure benchmark performance, not your use case. Always run custom eval.
- "95% accuracy is great" → If the 5% errors are catastrophic failures, accuracy is the wrong metric.
- "We'll evaluate after deployment" → Post-deployment evaluation is user-facing experimentation. Evaluate before.

## When To Use
- Comparing multiple models for a production use case
- Detecting regressions after model update or fine-tuning
- Setting up continuous evaluation pipelines
- Running standard benchmarks for model capability assessment
- A/B testing models in production with proper metrics

## Human Partner Signals (escalate to human)
- **Safety regression** — New model produces more harmful outputs → must not deploy
- **Cost explosion** — Better quality comes at 5x the cost → business decision on cost-quality tradeoff
- **Fairness failure** — Model performance varies significantly across demographic groups → ethics review
- **Benchmark gaming suspicion** — Suspiciously high benchmark scores → investigate contamination

## Pipeline
1. Define: identify evaluation dimensions — quality, latency, cost, safety, fairness, robustness
2. Select: choose benchmarks and custom eval tasks matching production use case
3. Baseline: run evaluation on current production model to establish baseline
4. Compare: run identical evaluation on candidate models
5. Analyze: compute statistical significance, identify regression, highlight tradeoffs
6. Report: generate evaluation report with radar chart, leaderboard, and deployment recommendation
7. Monitor: set up continuous evaluation to detect drift and regression over time

## Verification Checklist
- [ ] Evaluation covers quality + latency + cost + safety as minimum dimensions
- [ ] Statistical significance computed for all model comparisons
- [ ] Test set verified as unseen during model development
- [ ] Custom eval tasks match production use case (not just benchmarks)
- [ ] Regression detection configured with alerting thresholds
- [ ] Evaluation results reproducible with versioned test sets and configs



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
- `prompt-engineer` — Model evaluation measures prompt quality improvements
- `dataset-curator` — Evaluation datasets require the same curation rigor as training data
- `evaluating-llms-harness` — lm-eval-harness for standard benchmark execution
- `weights-and-biases` — Experiment tracking for evaluation results
