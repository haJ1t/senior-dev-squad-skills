#!/usr/bin/env python3
"""
Skill Benchmark Harness — Multi-Model via OpenRouter
Tests senior-dev-squad-skills across 4 frontier models with 5 benchmark tasks.
"""
import json, os, time, sys
from datetime import datetime
import subprocess

# ─── CONFIG ───────────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
if not OPENROUTER_API_KEY:
    print("❌ OPENROUTER_API_KEY not set!")
    sys.exit(1)

MODELS = {
    "claude-sonnet-4": "anthropic/claude-sonnet-4-20250514",
    "gpt-4o": "openai/gpt-4o-2024-11-20", 
    "gemini-2.5-pro": "google/gemini-2.5-pro-preview-05-06",
    "deepseek-v3": "deepseek/deepseek-chat",
}

API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ─── BENCHMARK TASKS ──────────────────────────────────────────

BENCHMARK_TASKS = [
    {
        "id": "arch-01",
        "category": "Architecture / Distributed Systems",
        "skill": "architecture-planner + distributed-systems-architect",
        "system_prompt": """You are a senior distributed systems architect. Follow these Iron Laws:
1. EVERY architecture decision MUST document its tradeoffs.
2. The network is unreliable — every call must have timeout, retry, circuit breaker.
3. CAP theorem awareness: document your consistency-availability tradeoff.
4. Every service owns its own database. Shared database = anti-pattern.
5. Idempotency is mandatory for all mutations.

Respond with a clear, numbered architecture plan. Document tradeoffs for every decision. Include concrete YAML examples.""",
        "user_prompt": """Design the architecture for a food delivery platform (like Uber Eats) that must handle:
- 50,000 concurrent orders during peak hours
- Real-time driver tracking (location every 5 seconds)
- Payment processing with PCI-DSS compliance
- Restaurant inventory management
- 99.95% uptime SLA
- Multi-region deployment (US East + EU)

Provide:
1. Service decomposition (bounded contexts)
2. Communication patterns between services (sync vs async)
3. Data consistency strategy (Saga, Outbox, Event Sourcing?)
4. Fault tolerance design (circuit breakers, fallbacks)
5. CAP tradeoffs for each data store
6. Deployment architecture""",
        "eval_criteria": ["service_decomposition", "communication_patterns", "consistency_strategy", "fault_tolerance", "cap_awareness", "deployment_plan", "tradeoffs_documented", "concrete_examples"],
    },
    {
        "id": "sec-01",
        "category": "Security Review",
        "skill": "security-reviewer",
        "system_prompt": """You are a senior application security engineer. Follow these Iron Laws:
1. NO production deployment without a passing security review.
2. Validate EVERY input at EVERY boundary. Never trust the client.
3. OWASP Top 10 scan is mandatory for every PR.
4. Three-layer defense for LLM apps: pre-filter → PII redaction → post-filter.
5. Rate limiting is not optional, it's infrastructure.

Respond with a structured security review. Categorize findings as CRITICAL, HIGH, MEDIUM, LOW.""",
        "user_prompt": """Review this API endpoint for security vulnerabilities:

```python
@app.post("/api/v1/users/search")
def search_users(request):
    query = request.json.get("q")
    sql = f"SELECT id, name, email, role FROM users WHERE name ILIKE '%{query}%' OR email ILIKE '%{query}%'"
    results = db.execute(sql).fetchall()
    return {"users": [dict(r) for r in results]}

@app.get("/api/v1/admin/users")
def admin_list_users():
    # TODO: Add auth later
    users = db.execute("SELECT * FROM users").fetchall()
    return {"users": [dict(u) for u in users], "total": len(users)}
```

Find ALL security issues. Rate each by severity. Provide fixes.""",
        "eval_criteria": ["sqli_detection", "auth_missing", "pii_exposure", "input_validation", "rate_limiting", "severity_accuracy", "fix_quality", "owasp_mapping"],
    },
    {
        "id": "code-01",
        "category": "Backend Implementation",
        "skill": "backend-senior-engineer",
        "system_prompt": """You are a senior backend engineer. Follow these Iron Laws:
1. NEVER trust the client. Validate EVERY input at EVERY boundary.
2. EVERY endpoint must handle: auth, validation, error formatting, logging.
3. Multi-step operations MUST use transactions.
4. Migrations MUST be additive with rollback plan.
5. Consistent error format: {error: {code, message, details, requestId}}.

Write production-grade code with proper error handling, logging, and validation.""",
        "user_prompt": """Implement a POST /api/v1/orders endpoint for an e-commerce platform with these requirements:

- Accept: user_id, items[{product_id, quantity}], shipping_address, payment_method_id
- Validate: all fields, quantity > 0, product exists, address valid
- Business logic: check inventory, calculate total, create order, reserve inventory, charge payment
- All steps in a single transaction (or Saga if multi-service)
- Return: order_id, status, total, estimated_delivery
- Rate limit: 10 orders per user per minute
- Structured logging for every request

Write the complete implementation in TypeScript/Express or Python/FastAPI.""",
        "eval_criteria": ["input_validation", "error_handling", "transaction_safety", "rate_limiting", "structured_logging", "idempotency", "inventory_check", "response_format"],
    },
    {
        "id": "edge-01", 
        "category": "Edge Case Analysis",
        "skill": "edge-case-hunter",
        "system_prompt": """You are an edge case hunter. Your job is to find EVERYTHING that can break. Follow this matrix:
1. Input extremes (empty, null, max length, unicode, SQL injection in text)
2. Concurrency (race conditions, double-submit, simultaneous cancel+process)
3. Network (timeout, partial response, connection drop mid-request)
4. Time (timezone, DST transitions, leap seconds, clock skew)
5. State (retry of already-succeeded operation, out-of-order events)
6. Scale (0 items, 1 item, 10K items, empty database, full disk)
7. Integration (upstream down, downstream slow, webhook replay, duplicate events)
8. Human (copy-paste errors, wrong currency, fat-finger quantities)

Document each edge case with: Scenario → Expected Behavior → What Actually Happens.""",
        "user_prompt": """Analyze this order cancellation flow for edge cases:

```
1. User clicks "Cancel Order" button
2. Frontend calls POST /api/v1/orders/{order_id}/cancel
3. Backend checks if order status is "CONFIRMED" or "PREPARING"
4. If yes: sets status to "CANCELLED", triggers refund
5. Refund service: reverses payment via Stripe
6. Inventory service: releases reserved items
7. Notification service: sends email + push notification
8. Returns 200 OK with new status
```

Find ALL edge cases. Consider timing, concurrency, failures at each step.""",
        "eval_criteria": ["concurrency_issues", "failure_states", "time_edge_cases", "idempotency_concerns", "state_machine_gaps", "network_failures", "integration_failures", "human_error_cases"],
    },
    {
        "id": "orch-01",
        "category": "Epic Orchestration",
        "skill": "epic-orchestrator",
        "system_prompt": """You are an epic orchestrator managing large-scale AI agent projects. Follow these Iron Laws:
1. NEVER start without epic decomposition. Break project→epics→stories→atomic tasks.
2. Every squad gets ONLY the context it needs. Cross-squad context leak = wasted tokens.
3. Every squad must be independently executable. If Squad A blocks Squad B for >1hr, decomposition is wrong.
4. Failure is a data point, not an endpoint. Retry → fallback → escalate → circuit breaker.
5. Every epic produces a learning artifact. Post-mortem, pattern extraction, skill update.

Plan with concrete YAML examples, dependency DAGs, token budgets, and monitoring rules.""",
        "user_prompt": """You need to orchestrate a 5-day project: "Migrate a 250K-line Rails monolith to microservices."

The project involves:
- Extracting 4 bounded contexts: User/Auth, Orders, Payments, Notifications
- Zero-downtime migration (users can't notice)
- 8 developers across 3 squads
- PCI-DSS compliance for payment context
- Must maintain existing API contracts during migration

Plan the full orchestration:
1. Epic decomposition (project → epics → stories → atomic tasks)
2. Squad design (roles, token budgets, handoff contracts)
3. Dependency DAG (which squad waits for which)
4. Timeline with milestones
5. Failure recovery strategy for each epic
6. Monitoring rules (alert conditions, escalation paths)
7. Post-mortem learning extraction plan""",
        "eval_criteria": ["decomposition_quality", "squad_design", "dependency_dag", "timeline_realism", "failure_recovery", "monitoring_rules", "learning_loop", "token_budgeting"],
    },
]

# ─── API CALL FUNCTION ────────────────────────────────────────

def call_model(model_id, system_prompt, user_prompt, max_tokens=2000):
    """Call OpenRouter API for a single model."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/senior-dev-squad",
        "X-Title": "Skill Benchmark Harness",
    }
    payload = {
        "model": MODELS[model_id],
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2,  # Low temp for consistency
    }
    
    curl_cmd = ["curl", "-s", "-w", "\n%{http_code}", "--max-time", "120",
                "-H", f"Authorization: Bearer {OPENROUTER_API_KEY}",
                "-H", "Content-Type: application/json",
                "-H", "HTTP-Referer: https://github.com/senior-dev-squad",
                "-H", "X-Title: Skill Benchmark Harness",
                "-d", json.dumps(payload),
                API_URL]
    
    try:
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=130)
        output = result.stdout.strip()
        
        # Split response and status code
        if "\n" in output:
            *response_lines, status_code = output.rsplit("\n", 1)
            response_text = "\n".join(response_lines)
        else:
            response_text = output
            status_code = "0"
        
        if status_code != "200":
            return {"error": f"HTTP {status_code}", "raw": response_text[:500]}
        
        data = json.loads(response_text)
        
        # Extract metrics
        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {})
        model_used = data.get("model", model_id)
        
        return {
            "model": model_used,
            "content": content,
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "cost": data.get("usage", {}).get("cost", 0) if "cost" in data.get("usage", {}) else None,
        }
    except subprocess.TimeoutExpired:
        return {"error": "timeout (>120s)"}
    except json.JSONDecodeError as e:
        return {"error": f"JSON parse: {str(e)[:100]}", "raw": response_text[:500] if 'response_text' in dir() else "N/A"}
    except Exception as e:
        return {"error": str(e)[:200]}


# ─── MAIN ─────────────────────────────────────────────────────

def main():
    print("=" * 70)
    print("🧪 SKILL BENCHMARK HARNESS — Multi-Model via OpenRouter")
    print(f"   Models: {', '.join(MODELS.keys())}")
    print(f"   Tasks:  {len(BENCHMARK_TASKS)} benchmark tasks")
    print(f"   Total:  {len(MODELS) * len(BENCHMARK_TASKS)} API calls")
    print("=" * 70)
    
    all_results = {}
    start_time = datetime.now()
    
    for task in BENCHMARK_TASKS:
        task_id = task["id"]
        print(f"\n📋 [{task_id}] {task['category']}")
        print(f"   Skill: {task['skill']}")
        
        task_results = {}
        for model_key, model_id in MODELS.items():
            print(f"   ⏳ Calling {model_key}...", end=" ", flush=True)
            result = call_model(model_key, task["system_prompt"], task["user_prompt"])
            
            if "error" in result:
                print(f"❌ {result['error']}")
                task_results[model_key] = result
            else:
                tokens = result["total_tokens"]
                length = len(result["content"])
                print(f"✅ {tokens} tokens, {length} chars")
                task_results[model_key] = result
            
            time.sleep(1)  # Rate limit safety
        
        all_results[task_id] = task_results
    
    elapsed = (datetime.now() - start_time).total_seconds()
    
    # ─── SUMMARY ───────────────────────────────────────────
    print("\n" + "=" * 70)
    print("📊 BENCHMARK SUMMARY")
    print("=" * 70)
    
    # Per-task comparison table
    for task in BENCHMARK_TASKS:
        task_id = task["id"]
        print(f"\n### {task_id}: {task['category']}")
        print(f"   Eval criteria: {', '.join(task['eval_criteria'][:5])}...")
        print(f"   {'Model':<20} {'Tokens':>8} {'Chars':>8} {'Status':>10}")
        print(f"   {'-'*20} {'-'*8} {'-'*8} {'-'*10}")
        
        for model_key in MODELS:
            r = all_results[task_id].get(model_key, {})
            if "error" in r:
                print(f"   {model_key:<20} {'—':>8} {'—':>8} {'❌ ' + r['error']:>10}")
            else:
                print(f"   {model_key:<20} {r['total_tokens']:>8} {len(r['content']):>8} {'✅':>10}")
    
    # Overall token comparison
    print(f"\n### Overall Token Efficiency")
    print(f"   {'Model':<20} {'Total Tokens':>14} {'Avg/Task':>10}")
    print(f"   {'-'*20} {'-'*14} {'-'*10}")
    for model_key in MODELS:
        total = sum(
            all_results[t["id"]].get(model_key, {}).get("total_tokens", 0)
            for t in BENCHMARK_TASKS
        )
        avg = total / len(BENCHMARK_TASKS) if total > 0 else 0
        print(f"   {model_key:<20} {total:>14,} {avg:>10,.0f}")
    
    print(f"\n⏱️  Total benchmark time: {elapsed:.1f}s")
    print(f"📁 Results saved to: /tmp/skill-benchmark-results.json")
    
    # Save full results
    output = {
        "benchmark": "senior-dev-squad-skills v3.1.0",
        "timestamp": datetime.now().isoformat(),
        "models": list(MODELS.keys()),
        "tasks": [{"id": t["id"], "category": t["category"], "skill": t["skill"]} for t in BENCHMARK_TASKS],
        "elapsed_seconds": elapsed,
        "results": all_results,
    }
    
    # Save (content fields only for file size)
    for task_id in all_results:
        for model_key in all_results[task_id]:
            if "content" in all_results[task_id][model_key]:
                # Keep first 500 chars for preview
                all_results[task_id][model_key]["content_preview"] = all_results[task_id][model_key]["content"][:500]
    
    with open("/tmp/skill-benchmark-results.json", "w") as f:
        json.dump(output, f, indent=2, default=str)
    
    return all_results

if __name__ == "__main__":
    main()
