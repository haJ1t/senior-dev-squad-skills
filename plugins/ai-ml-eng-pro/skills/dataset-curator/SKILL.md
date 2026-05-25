---
name: dataset-curator
description: "Dataset creation, cleaning, augmentation, versioning, QA for ML/AI pipelines. Use when preparing or improving a training or evaluation dataset."
version: 1.0.0
platforms: [linux, macos]
---

# Dataset Curator

## What It Does
Manages the full dataset lifecycle for ML/AI projects — from raw data collection through cleaning, labeling, augmentation, splitting, versioning, and quality assurance. Ensures datasets are reproducible, documented (datasheets), balanced across classes/demographics, and free from common pitfalls like data leakage, label noise, and unintended bias.

## Iron Laws (NEVER violate)
1. **Split before touch** — Separate train/val/test before ANY processing. Data leakage through preprocessing is the #1 ML bug.
2. **Data card required** — Every dataset must have a datasheet documenting source, collection method, demographics, known biases, and usage restrictions.
3. **Version everything** — Datasets, labels, and preprocessing code must be versioned together. Reproducibility demands it.
4. **Class balance awareness** — Know your class distribution. Imbalanced datasets need explicit handling (oversampling, weighting, stratified splitting).

## Red Flags (STOP immediately)
- **Data leakage** — Training data contains information from test set (time-based, group-based, or preprocessing leakage) → must fix before training
- **Label noise > 10%** — Too many mislabeled examples → cleaning required; model will learn noise
- **Demographic skew** — Dataset represents only one demographic → model will fail on others; document or fix
- **PII in dataset** — Personally identifiable information found in training data → must anonymize or remove

## Common Rationalizations (self-deception)
- "More data is always better" → Noisy, biased, or leaked data is worse than less clean data. Quality > quantity.
- "We'll clean it later" → Data quality issues compound through the pipeline. Clean early, clean often.
- "The dataset is representative enough" → Without demographic analysis, "representative" is an assumption. Verify.

## When To Use
- Creating a new dataset for ML training or evaluation
- Cleaning and preparing existing data for model consumption
- Augmenting data to address class imbalance or increase diversity
- Versioning datasets for reproducible ML pipelines
- Auditing datasets for bias, leakage, and quality issues

## Human Partner Signals (escalate to human)
- **Sensitive data** — Dataset contains health, financial, or biometric data → compliance review
- **Copyright concern** — Data scraped from web may violate copyright → legal review
- **Bias discovered** — Systematic demographic exclusion found → ethics and product decision
- **Labeling ambiguity** — Human labelers disagree >20% on task → task definition needs refinement

## Pipeline
1. Collect: gather raw data from sources, document provenance and collection methodology
2. Profile: analyze distributions, identify missing values, detect outliers, check class balance
3. Clean: handle missing values, remove duplicates, correct label errors, filter outliers
4. Augment: apply transformations to balance classes, increase diversity, improve robustness
5. Split: create stratified train/val/test splits with temporal awareness for time-series data
6. Document: generate datasheet with all metadata — source, demographics, biases, usage
7. Version: commit dataset + preprocessing code + datasheet to versioned storage (DVC, HF datasets)

## Verification Checklist
- [ ] Train/val/test split performed before any preprocessing
- [ ] Data card/datasheet completed for every dataset
- [ ] Class distribution analyzed and imbalance addressed
- [ ] PII scan completed with zero findings
- [ ] Data leakage check passed (no test info in training data)
- [ ] Dataset versioned with reproducible preprocessing pipeline
- [ ] Demographic analysis documents representation across key groups

## Related Skills
- `model-evaluator` — Curated datasets are the foundation of reliable model evaluation
- `prompt-engineer` — Test sets for prompt evaluation are curated datasets
- `embedding-manager` — Embedding quality depends on dataset quality
- `huggingface-hub` — Dataset storage, versioning, and sharing infrastructure
