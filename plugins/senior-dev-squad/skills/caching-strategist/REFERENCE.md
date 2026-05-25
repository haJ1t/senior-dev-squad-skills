# Caching Strategist — Reference

Deep tables and code patterns extracted from `SKILL.md` to keep the main file concise.

---

## Cache Layer Reference

| Layer | Scope | Latency saved | Invalidation mechanism | Best for |
|-------|-------|--------------|----------------------|---------|
| Browser HTTP cache | Single user, single device | Network round-trip | `Cache-Control max-age`, `ETag`/`If-None-Match`, `stale-while-revalidate` | Static assets, public API responses |
| CDN / edge cache | All users, global | Origin round-trip | Surrogate-Key purge, `Cache-Control s-maxage`, tag-based purge API | Public pages, images, API read endpoints |
| App-level in-process | Single process instance | DB/API call | TTL expiry, explicit key delete, local LRU eviction | Hot lookup tables, config, low-cardinality reference data |
| Distributed cache (Redis/Memcached) | All app instances | DB/API call | TTL expiry, `DEL`/`UNLINK`, pub/sub invalidation, Lua scripts | Session data, computed aggregates, rate-limit counters |
| DB query cache | Within DB engine | Query execution | Automatic on write to underlying tables (use with caution) | Repeated identical read queries; avoid for OLTP writes |
| Read replica | All app instances | Write-path latency | Replication lag (eventual) | Heavy read load, reporting queries |

**Decision rule:** pick the layer closest to the consumer that can still be invalidated correctly. Browser cache is cheapest but hardest to invalidate remotely. DB query cache is automatic but invisible and unreliable.

---

## Invalidation Strategy Comparison

| Strategy | Consistency | Complexity | Best for |
|----------|------------|-----------|---------|
| TTL-only expiry | Eventual (bounded by TTL) | Low | Data where stale reads are acceptable (e.g., product catalog) |
| Explicit delete on write | Strong (for the writer's data) | Medium | User-owned mutable data (profile, settings) |
| Tag-based / surrogate-key purge | Strong (for all tagged keys) | High | CDN: purge all pages containing a product on price change |
| Event-driven (pub/sub) | Near-real-time | High | Cross-service caches: service A invalidates service B's cache via event |
| Version/generation key | Strong (key never collides) | Low–Medium | Global config, feature flags — bump a version counter to invalidate all |
| Cache-busting (fingerprinted URLs) | Perfect | Low (static only) | CSS/JS/image assets with content hash in filename |

---

## Pattern Code: Cache-Aside

```python
def get_user_profile(user_id: str) -> dict:
    cache_key = f"user:profile:{user_id}"

    # 1. Check cache
    cached = redis.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. Cache miss — load from DB
    profile = db.query("SELECT * FROM users WHERE id = %s", user_id)
    if profile is None:
        return None

    # 3. Populate cache with explicit TTL
    redis.setex(cache_key, ttl=300, value=json.dumps(profile))
    return profile

def update_user_profile(user_id: str, data: dict) -> None:
    db.execute("UPDATE users SET ... WHERE id = %s", user_id, data)
    # INVALIDATION: delete the key immediately after write
    redis.delete(f"user:profile:{user_id}")
```

---

## Pattern Code: Write-Through

```python
def save_order(order: dict) -> None:
    db.execute("INSERT INTO orders ...", order)
    cache_key = f"order:{order['id']}"
    redis.setex(cache_key, ttl=3600, value=json.dumps(order))
    # Cache is populated on write — reads will always hit
```

---

## Stampede Prevention: Probabilistic Early Recomputation (PER)

Recompute the cache slightly before it expires, while still serving the cached value to most requests.

```python
import math, random, time

def get_with_per(key: str, ttl: int, fetch_fn) -> dict:
    result = redis.get(key)
    if result:
        data, computed_at, beta = json.loads(result)
        remaining_ttl = redis.ttl(key)
        # Recompute early if probabilistically past the recompute window
        if remaining_ttl - beta * math.log(random.random()) < 0:
            data = fetch_fn()
            redis.setex(key, ttl, json.dumps([data, time.time(), beta]))
        return data

    # Full miss — fetch and populate
    data = fetch_fn()
    redis.setex(key, ttl, json.dumps([data, time.time(), 1.0]))
    return data
```

---

## Stampede Prevention: Distributed Lock (Mutex)

Only one worker recomputes; others wait briefly or serve stale.

```python
import uuid

def get_with_lock(key: str, ttl: int, lock_ttl: int, fetch_fn) -> dict:
    cached = redis.get(key)
    if cached:
        return json.loads(cached)

    lock_key = f"{key}:lock"
    lock_value = str(uuid.uuid4())

    acquired = redis.set(lock_key, lock_value, nx=True, ex=lock_ttl)
    if acquired:
        try:
            data = fetch_fn()
            redis.setex(key, ttl, json.dumps(data))
            return data
        finally:
            # Only release our own lock
            lua = "if redis.call('get',KEYS[1])==ARGV[1] then return redis.call('del',KEYS[1]) else return 0 end"
            redis.eval(lua, 1, lock_key, lock_value)
    else:
        time.sleep(0.05)
        return get_with_lock(key, ttl, lock_ttl, fetch_fn)
```

---

## Version/Generation Key Pattern

Invalidate ALL keys in a namespace without iterating them.

```python
def get_cache_key(user_id: str) -> str:
    generation = redis.get("user:profile:generation") or "1"
    return f"user:profile:v{generation}:{user_id}"

def invalidate_all_profiles() -> None:
    redis.incr("user:profile:generation")  # All old keys become orphans
```

---

## HTTP Cache Headers Reference

```http
# Public CDN-cacheable, 10 min, stale-while-revalidate for smoothness
Cache-Control: public, max-age=600, stale-while-revalidate=60

# Private (per-user), must not be stored at CDN
Cache-Control: private, max-age=300

# Never cache (admin actions, payment pages)
Cache-Control: no-store

# Conditional: client sends ETag back; 304 if unchanged
ETag: "abc123"
Cache-Control: public, max-age=0, must-revalidate
```

---

## TTL Selection Rules

| Staleness tolerance | TTL range | Example data |
|--------------------|-----------|-------------|
| Very low (seconds) | 1–60 s | Stock price, seat availability, rate-limit counters |
| Low (minutes) | 5–60 min | User profile, search results, rendered pages |
| Medium (hours) | 1–24 h | Reference data, category tree, feature flags |
| High (days+) | Days or cache-busted | Static assets, country list, compiled templates |

**Jitter formula:** `effective_ttl = base_ttl + random.randint(0, int(base_ttl * 0.1))`

Never set `TTL=0` in production Redis — it means "never expires." Use explicit `DEL` to remove a key immediately.
