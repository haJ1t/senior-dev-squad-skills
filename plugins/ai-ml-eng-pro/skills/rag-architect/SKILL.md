---
name: rag-architect
description: "End-to-end RAG system design — chunking strategies, embedding selection, retrieval optimization, reranking. Use when building or tuning a RAG pipeline."
version: 1.0.0
platforms: [linux, macos]
---

# RAG Architect

## What It Does
Designs and optimizes Retrieval-Augmented Generation (RAG) systems end-to-end. Covers chunking strategies (fixed, semantic, recursive, agentic), embedding model selection, vector database architecture, retrieval optimization (hybrid search, multi-stage retrieval), reranking, context window management, and hallucination reduction techniques.

## Iron Laws (NEVER violate)
1. **Retrieval before generation** — Never let the LLM answer from its parametric knowledge when relevant documents exist. RAG without retrieval is just generation.
2. **Chunk for the task** — Chunking strategy must match the query pattern. Q&A needs small chunks; summarization needs large chunks. Wrong chunk size = irrelevant retrieval.
3. **Source attribution required** — Every generated claim that came from a retrieved document must cite its source. Unattributed claims are indistinguishable from hallucination.
4. **Evaluate retrieval separately** — Retrieval quality (precision@k, recall@k, MRR) must be measured independently from generation quality. Bad retrieval → bad RAG, regardless of LLM quality.

## Red Flags (STOP immediately)
- **Retrieval irrelevance** — Top-k retrieved documents are unrelated to query → chunking or embedding strategy broken
- **Context overflow** — Retrieved documents exceed model context window → need reranking, summarization, or chunk reduction
- **Hallucination from retrieval** — LLM generates claims not present in retrieved documents → source attribution failure
- **Latency spiral** — Retrieval + reranking + generation exceeds latency SLA → pipeline optimization needed

## Common Rationalizations (self-deception)
- "Just use the default chunk size (1000 tokens)" → Chunk size is task-dependent. Default is rarely optimal.
- "Vector search is enough" → Keyword search catches exact matches that embeddings miss. Hybrid search is almost always better.
- "More retrieved documents = better answers" → Beyond optimal k, irrelevant documents dilute context and increase hallucination.

## When To Use
- Building a RAG system for document Q&A
- Optimizing an existing RAG pipeline that produces poor answers
- Selecting embedding models and vector databases
- Designing multi-stage retrieval with reranking
- Reducing hallucination in LLM applications with grounding

## Human Partner Signals (escalate to human)
- **Data sensitivity** — Documents contain confidential/proprietary information → access control review
- **Compliance requirement** — RAG system handles regulated data (health, finance, legal) → compliance review
- **Scale decision** — Vector database choice has significant cost implications → architecture decision
- **Quality threshold** — RAG accuracy below business requirement after optimization → human review of feasibility

## Pipeline
1. Analyze: understand query patterns, document types, latency requirements, accuracy targets
2. Chunk: select and tune chunking strategy — size, overlap, metadata preservation
3. Embed: choose embedding model based on domain, dimensionality, cost, and benchmark performance
4. Store: configure vector database with appropriate indexing (HNSW, IVF) and metadata filtering
5. Retrieve: implement retrieval — hybrid search (dense + sparse), multi-stage (candidate → rerank)
6. Generate: design LLM prompt with retrieved context, source attribution, and anti-hallucination guards
7. Evaluate: measure retrieval quality and end-to-end answer accuracy separately
8. Iterate: tune chunk size, retrieval k, reranking threshold based on eval results

## Verification Checklist
- [ ] Chunking strategy tested with real query patterns (not synthetic)
- [ ] Retrieval evaluated independently (precision@k, recall@k, MRR)
- [ ] Hybrid search implemented (dense + sparse) for retrieval
- [ ] Source attribution verified — every generated claim traceable to a document
- [ ] Context window budget honored (no overflow)
- [ ] Latency measured end-to-end and within SLA
- [ ] Hallucination rate measured on held-out test set

## Related Skills
- `embedding-manager` — Embedding generation and optimization for RAG retrieval
- `prompt-engineer` — RAG generation prompts require specialized design
- `model-evaluator` — Evaluate RAG system quality end-to-end
- `dataset-curator` — Curate document collections for RAG indexing
