---
name: postgres-pro
description: "Advanced PostgreSQL: indexing, CTEs, window functions, partitioning, full-text search. Use when optimizing or reviewing PostgreSQL schemas and queries."
model: any
user-invocable: true
always: false
---

# PostgreSQL Pro

## Purpose

Use PostgreSQL at a senior DBA level. Covers advanced indexing strategies, query optimization, window functions, CTEs, full-text search, partitioning, and migration safety.

## When to Use

**Use this when:**
- Writing or reviewing complex SQL queries involving CTEs, window functions, or subqueries
- Designing or auditing indexes for tables with performance-sensitive read paths
- Planning schema migrations that must not lock tables in production

**Use this ESPECIALLY when:**
- EXPLAIN ANALYZE shows sequential scans on tables with more than 10K rows
- Query latency has regressed after a data-volume increase and the bottleneck is unclear
- A migration involves renaming columns, dropping defaults, or adding constraints to a live table

**Don't skip when:**
- Implementing full-text search — LIKE '%term%' at scale is a common performance trap
- Setting up partitioning on a high-volume append-only table (audit logs, events, metrics)
- Configuring connection pooling or statement timeouts for a new production environment

## Core Patterns

### 1. Index Strategy

```sql
-- B-tree (default) — equality + range queries
CREATE INDEX idx_projects_owner_id ON projects(owner_id);

-- Composite B-tree — multi-column filters
CREATE INDEX idx_projects_owner_status_created
ON projects(owner_id, status, created_at DESC);

-- Partial index — filtered subset
CREATE INDEX idx_active_projects
ON projects(owner_id, created_at DESC)
WHERE status = 'active';

-- Covering index — avoid heap lookups
CREATE INDEX idx_projects_list
ON projects(owner_id, status, created_at DESC)
INCLUDE (name, description);

-- GIN — full-text search, JSONB, arrays
CREATE INDEX idx_projects_search
ON projects USING GIN(to_tsvector('english', name || ' ' || description));

-- BRIN — large, sequential tables (logs, time-series)
CREATE INDEX idx_audit_logs_created
ON audit_logs USING BRIN(created_at)
WITH (pages_per_range = 32);

-- Hash — equality only (rarely needed)
CREATE INDEX idx_users_email_hash
ON users USING HASH(email);
```

### 2. Query Optimization

```sql
-- Check query plan
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
SELECT * FROM projects WHERE owner_id = 'uuid-here';

-- Common anti-patterns:
-- ❌ Sequential scan on large table
-- ✅ Add appropriate index

-- ❌ N+1 queries in app code
-- ✅ JOIN + prefetch

-- ❌ SELECT * when only id needed
-- ✅ SELECT specific columns

-- ❌ COUNT(*) on every page load
-- ✅ Approximate count or cached count

-- ❌ Filtering on function(column)
-- ✅ Index on expression or generated column
```

### 3. CTEs (Common Table Expressions)

```sql
-- Recursive CTE — hierarchy traversal
WITH RECURSIVE project_tree AS (
  -- Anchor: top-level tasks
  SELECT id, parent_id, title, 1 AS depth
  FROM tasks
  WHERE project_id = 'uuid' AND parent_id IS NULL

  UNION ALL

  -- Recursive: child tasks
  SELECT t.id, t.parent_id, t.title, pt.depth + 1
  FROM tasks t
  JOIN project_tree pt ON t.parent_id = pt.id
)
SELECT * FROM project_tree ORDER BY depth, title;

-- Multi-step CTE — clear data pipeline
WITH
  project_stats AS (
    SELECT project_id, COUNT(*) AS task_count
    FROM tasks GROUP BY project_id
  ),
  top_projects AS (
    SELECT p.*, ps.task_count
    FROM projects p
    JOIN project_stats ps ON p.id = ps.project_id
    ORDER BY ps.task_count DESC
    LIMIT 10
  )
SELECT * FROM top_projects;
```

### 4. Window Functions

```sql
-- Running total
SELECT
  created_at,
  amount,
  SUM(amount) OVER (ORDER BY created_at) AS running_total
FROM transactions
WHERE project_id = 'uuid';

-- Rank within group
SELECT
  id, name, status, created_at,
  ROW_NUMBER() OVER (
    PARTITION BY status
    ORDER BY created_at DESC
  ) AS status_rank
FROM projects
WHERE owner_id = 'uuid';

-- Moving average
SELECT
  created_at,
  value,
  AVG(value) OVER (
    ORDER BY created_at
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS moving_avg_7d
FROM metrics
WHERE project_id = 'uuid';
```

### 5. Full-Text Search

```sql
-- Add tsvector column
ALTER TABLE projects ADD COLUMN search_vector tsvector;

-- Populate via trigger
CREATE FUNCTION projects_search_update() RETURNS trigger AS $$
BEGIN
  NEW.search_vector := to_tsvector('english',
    COALESCE(NEW.name, '') || ' ' || COALESCE(NEW.description, '')
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_projects_search
  BEFORE INSERT OR UPDATE ON projects
  FOR EACH ROW EXECUTE FUNCTION projects_search_update();

-- GIN index on tsvector
CREATE INDEX idx_projects_search ON projects USING GIN(search_vector);

-- Query
SELECT id, name,
  ts_rank(search_vector, query) AS rank
FROM projects, plainto_tsquery('english', 'project management') AS query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```

### 6. Table Partitioning

```sql
-- Range partitioning by date
CREATE TABLE audit_logs (
  id UUID NOT NULL,
  action TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE audit_logs_2025_q1
  PARTITION OF audit_logs
  FOR VALUES FROM ('2025-01-01') TO ('2025-04-01');

CREATE TABLE audit_logs_2025_q2
  PARTITION OF audit_logs
  FOR VALUES FROM ('2025-04-01') TO ('2025-07-01');

-- Partition pruning happens automatically
EXPLAIN SELECT * FROM audit_logs
WHERE created_at BETWEEN '2025-02-01' AND '2025-02-28';
-- Only scans audit_logs_2025_q1
```

### 7. Migration Safety

```sql
-- ✅ Additive: new column with default (no downtime)
ALTER TABLE projects ADD COLUMN priority INTEGER DEFAULT 0;

-- ✅ Expand-contract: rename column safely
-- Phase 1: Add new column + sync trigger
ALTER TABLE projects ADD COLUMN display_name TEXT;
UPDATE projects SET display_name = name WHERE display_name IS NULL;
CREATE FUNCTION sync_name() RETURNS trigger AS $$ ... $$;
-- Phase 2: Drop old column (separate deploy, after all code updated)
ALTER TABLE projects DROP COLUMN name;

-- ✅ NOT VALID: add constraint without table lock
ALTER TABLE projects ADD CONSTRAINT projects_status_check
  CHECK (status IN ('active', 'archived'))
  NOT VALID;
-- Later: VALIDATE CONSTRAINT (no lock)
ALTER TABLE projects VALIDATE CONSTRAINT projects_status_check;
```

### Checklist

- [ ] Every query with a WHERE clause has an index
- [ ] Composite indexes ordered by selectivity (most selective first)
- [ ] N+1 queries detected and eliminated
- [ ] No sequential scans on tables > 10K rows
- [ ] Full-text search uses tsvector + GIN (not LIKE '%...%')
- [ ] Migrations are additive (no ALTER COLUMN DROP DEFAULT)
- [ ] EXPLAIN ANALYZE run on all new queries
- [ ] Connection pooling (PgBouncer) configured
- [ ] statement_timeout set to prevent runaway queries
- [ ] Regular VACUUM schedule for high-turnover tables



## Related Skills

- **backend-senior-engineer** — ORM query patterns and connection management live in application code; coordinate when N+1 queries or missing indexes are introduced at the ORM layer
- **supabase-pro** — Supabase runs on PostgreSQL; this skill supplies the advanced index, partition, and migration knowledge that supabase-pro defers to when queries or schema complexity grows
- **performance-engineer** — slow query analysis and EXPLAIN ANALYZE interpretation overlap with application-level profiling; use together when the bottleneck spans DB and runtime
- **api-design-reviewer** — pagination, filtering, and sorting decisions at the API layer directly determine which indexes are useful; align both skills when designing list endpoints on large tables
- **devops-release-engineer** — zero-downtime migration techniques (expand-contract, NOT VALID constraints) must be coordinated with deploy strategy; involve this skill when a migration requires multi-phase deployment
- **observability-pro** — pg_stat_statements, slow query logs, and connection pool metrics feed into the observability stack; use together when instrumenting database health

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
