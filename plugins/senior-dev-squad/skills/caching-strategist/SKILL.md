---
name: caching-strategist
description: "Designs deliberate, invalidation-first caching across browser, CDN, app, and DB layers. Use when adding a cache, choosing TTL, preventing stampede, or auditing staleness risk."
---

# Caching Strategist

## Overview

Caching is not a performance knob you turn up — it is a consistency contract you sign. Every cache entry is a promise that the data it holds is fresh enough for its consumers. Break that promise silently and you ship a latency-wrapped bug. This skill forces the right questions before a single key is written: which layer owns this data, how will it be invalidated, and what happens when it goes stale?

**Core principle:** Name the invalidation strategy before you add the cache. A cache without a named invalidation strategy is a bug with latency.

## The Iron Law

```
DEFINE THE INVALIDATION STRATEGY BEFORE YOU WRITE THE FIRST CACHE KEY.
NOT AFTER. NOT DURING CODE REVIEW. BEFORE.
```

## When to Use

**Use this when:**
- Adding any cache layer: Redis, Memcached, CDN edge, browser HTTP cache, in-process LRU, DB query cache
- Choosing or changing a TTL value
- Adding a `Cache-Control` or `ETag` header
- Designing a read-heavy endpoint that hits a database
- Migrating from per-request DB calls to a shared cache

**Use this ESPECIALLY when:**
- Someone says "just throw Redis in front of it" — unconstrained caching causes silent stale reads
- The data is user-specific, permission-gated, or mutable — cardinality and correctness collide
- Traffic spikes are expected — stampede hits exactly when you need the cache most
- The feature is "simple read caching" — simple caches have complex invalidation

**Never skip when:**
- Changing a TTL on an existing cache — you are changing the consistency contract, not just a number
- Adding a new cache key pattern — cardinality explosions happen quietly
- Upstream data can be mutated by users other than the reader — invalidation is non-local

## Phase 1: Layer Selection

Place the data in the correct cache tier before choosing a pattern. Full layer reference with latency, scope, and invalidation mechanism is in [`REFERENCE.md`](./REFERENCE.md).

**Tiers (closest-to-consumer first):**

1. **Browser HTTP cache** — single user, single device; `Cache-Control` + `ETag`; hardest to remotely invalidate
2. **CDN / edge cache** — all users globally; surrogate-key/tag-based purge; ideal for public read endpoints
3. **App-level in-process LRU** — single process; TTL + explicit eviction; best for low-cardinality reference data
4. **Distributed cache (Redis/Memcached)** — all app instances; `DEL`, TTL, pub/sub; session, aggregates, rate limits
5. **DB query cache** — engine-level; automatic but invisible; use with caution in OLTP
6. **Read replica** — eventual consistency via replication lag; reporting and heavy read queries

**Decision rule:** pick the layer closest to the consumer that can still be invalidated correctly.

## Phase 2: Pattern Selection

Pick one pattern per cache scope. Do not mix patterns in the same key namespace without documenting why.

| Pattern | When to use | Write latency | Invalidation |
|---------|------------|--------------|-------------|
| **Cache-aside** (lazy) | Most read-heavy workloads | None | Explicit `DEL` on write |
| **Read-through** | Client library supports it; keeps app code simple | None | Explicit `DEL` on write |
| **Write-through** | Data read immediately after write (e.g., order confirmation) | 2× (DB + cache) | Key always warm |
| **Write-behind** | Extremely write-heavy; counters, leaderboards | Async | Durability risk; requires durable queue |

See [`REFERENCE.md`](./REFERENCE.md) for cache-aside and write-through code examples.

## Phase 3: Invalidation Strategy

The strategy must be named and documented at the cache write site — in a comment or ADR — before implementation. Full strategy comparison table is in [`REFERENCE.md`](./REFERENCE.md).

**Strategies (choose one):**

- **TTL-only expiry** — eventual, bounded staleness; low complexity; right for product catalogs, public pages
- **Explicit delete on write** — strong, co-located with mutations; right for user-owned mutable data
- **Tag-based / surrogate-key purge** — strong for CDN; purge all pages embedding a changed entity
- **Event-driven pub/sub** — near-real-time for cross-service invalidation; highest complexity
- **Version/generation key** — bump a counter to orphan an entire namespace; right for config, feature flags
- **Cache-busting (fingerprinted URLs)** — perfect for static assets; content hash in filename

**TTL rules (add jitter to every TTL to prevent synchronized expiry storms):**

```python
# Always apply jitter — prevents synchronized expiry stampedes
effective_ttl = base_ttl + random.randint(0, int(base_ttl * 0.1))
redis.setex(cache_key, effective_ttl, value)
```

Never set `TTL=0` in production Redis — it means "never expires." See [`REFERENCE.md`](./REFERENCE.md) for HTTP `Cache-Control` header patterns and TTL selection by staleness tolerance.

## Phase 4: Stampede Prevention

Cache stampede (thundering herd) = many concurrent misses all hitting the DB simultaneously. This is when your cache causes the outage. Apply one of these for any high-traffic key.

**Options (choose one):**

1. **Probabilistic Early Recomputation (PER)** — recomputes the value slightly before expiry while serving cached data to the rest; no coordination overhead
2. **Distributed lock / mutex** — one worker recomputes, others wait briefly; use a Lua-scripted atomic release to avoid lock leaks
3. **Request coalescing (single-flight)** — at the app layer, one in-flight fetch per key; duplicate callers wait for the same result; libraries: `singleflight` (Go), `p-memoize` (Node), `asyncio-singleflight` (Python)

Full code for PER, distributed lock, and version/generation pattern is in [`REFERENCE.md`](./REFERENCE.md).

## Phase 5: Cache Key Design

Bad keys cause cardinality explosions, cross-tenant data leaks, and incidents that cannot be reproduced in staging.

**Convention:** `{service}:{entity}:{id}:{variant}`

```
user:profile:u_1234
product:detail:p_5678:currency=USD:locale=en
search:results:q=shoes:page=1:sort=relevance
```

**Key design checklist:**
- Is the ID cardinality bounded? If unbounded, set a memory alert.
- Does the key include user-controlled input? Normalize (lowercase, trim) before hashing.
- Is user-scoped data isolated? Include `user_id` in the Redis key; use `Cache-Control: private` at HTTP layer.
- Are query parameters in canonical order? `?a=1&b=2` and `?b=2&a=1` must hash to the same key.

**What NOT to cache:**
- Mutable aggregates with no invalidation bus to the write service
- PII — unless the cache is encrypted and strictly user-scoped
- Results of non-deterministic operations (`NOW()`, `UUID()`, `random()`)
- Errors — unless negative caching is intentional with a very short TTL
- Anything that changes faster than your shortest meaningful TTL

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "I'll add the invalidation logic later, let's get caching working first"
- "The TTL is short enough that staleness doesn't really matter"
- "We'll just flush the whole cache when we deploy"
- "This data never changes" (without auditing the write path)
- "Redis is fast, so more caching is always better"
- "The key includes the full user query string" (cardinality bomb incoming)
- Writing a cache key with no `DEL` and no TTL anywhere in the codebase

**ALL of these mean: STOP. Return to Phase 2 (pattern) or Phase 3 (invalidation).**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "TTL will handle it eventually" | Eventual ≠ acceptable. Define the staleness window your users can tolerate, then set that TTL explicitly. |
| "We'll add invalidation after launch" | After launch the write paths are harder to audit. You will ship stale bugs instead of fixing them. |
| "It's read-only data, no invalidation needed" | "Read-only" describes today's write paths. Reference data changes at deploy, via admin panel, or migration. Name the strategy anyway. |
| "More cache layers = more performance" | More cache layers = more invalidation surfaces = more consistency bugs. Add layers only when profiling justifies it. |
| "Flushing the whole cache on deploy is fine" | Stampede. All traffic hits the origin simultaneously. Warm the cache before cutover or use rolling invalidation. |
| "Cache keys are an implementation detail" | Bad key design causes cross-tenant data leaks, cardinality explosions, and production incidents with no staging reproduction. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Users are seeing stale data after we updated X" — invalidation does not cover all write paths; return to Phase 3
- "The database melted right after deploy" — cache flushed without stampede protection; return to Phase 4
- "Redis memory keeps growing" — unbounded cardinality or missing TTLs; return to Phase 5
- "Why are some users seeing other users' data?" — user-scoped data in a shared key; return to Phase 5
- "Caching made things slower" — wrong layer or TTL so short recomputation cost dominates; return to Phase 1

**When you see these:** STOP. Return to the named phase and document the decision change.

## Related Skills

- **performance-engineer** — profile and confirm the upstream bottleneck before adding a cache layer
- **data-modeling-designer** — cache key design must match the entity model; schema changes break key contracts
- **backend-senior-engineer** — audit all mutation write paths that must trigger invalidation
- **sre-slo-engineer** — define cache hit rate, origin error rate, and staleness SLOs; alert when effectiveness degrades
- **distributed-systems-architect** — cache consistency tradeoffs in multi-region and multi-service topologies

## Verification

- [ ] Invalidation strategy is named and documented at every cache write site (comment or ADR)
- [ ] TTL is set explicitly on every key; no key has infinite TTL unless intentional and documented
- [ ] TTL values have jitter applied to prevent synchronized expiry
- [ ] Stampede protection is in place for every high-traffic cache key (PER, lock, or coalescing)
- [ ] Cache key naming follows the `{service}:{entity}:{id}:{variant}` convention
- [ ] User-scoped data includes `user_id` in the key and is not served from a shared CDN cache
- [ ] All write paths that mutate cached data have been audited and trigger invalidation
- [ ] Cardinality of each key space is bounded or monitored with a memory alert
- [ ] What NOT to cache is documented (PII, non-deterministic results, high-churn aggregates)
- [ ] HTTP `Cache-Control` headers are set correctly for public vs. private data
- [ ] Cache layer choice is justified against the layer reference table (Phase 1 / `REFERENCE.md`)
- [ ] Negative caching is intentional and TTL is appropriately short
- [ ] Deploy runbook addresses cache warm-up if a full flush is required at cutover
