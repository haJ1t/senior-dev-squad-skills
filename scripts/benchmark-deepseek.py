#!/usr/bin/env python3
"""Skill Benchmark - DeepSeek Multi-Model + Skill ON/OFF Comparison"""
import json, os, time, subprocess
from datetime import datetime

# --- LOAD API KEY ---
DEEPSEEK_KEY = ""
env_file = os.path.expanduser("~/.hermes/.env")
if os.path.exists(env_file):
    for line in open(env_file):
        if line.startswith("DEEPSEEK_API_KEY="):
            DEEPSEEK_KEY = line.split("=", 1)[1].strip().strip('"').strip("'")
            break
if not DEEPSEEK_KEY:
    DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not DEEPSEEK_KEY:
    print("DEEPSEEK_API_KEY not found!")
    exit(1)

MODELS = {"deepseek-v3": "deepseek-chat", "deepseek-r1": "deepseek-reasoner"}
API_URL = "https://api.deepseek.com/v1/chat/completions"

# --- BENCHMARK TASKS ---
TASKS = []

# Task 1: Architecture
TASKS.append({
    "id": "arch-01",
    "category": "Architecture",
    "skill": "You are a senior distributed systems architect. Follow these rules:
1. EVERY architecture decision MUST document its tradeoffs
2. The network is unreliable - every call must have timeout, retry, circuit breaker
3. Every service owns its own database
4. Idempotency is mandatory for all mutations

Respond with a numbered architecture plan with concrete YAML examples.",
    "noskill": "You are a helpful AI assistant. Design a system architecture as requested.",
    "prompt": "Design architecture for a food delivery platform: 50K concurrent orders, real-time driver tracking (location every 5s), PCI-DSS payments, restaurant inventory, 99.95% uptime SLA, multi-region (US East + EU). Provide: 1) Service decomposition 2) Communication patterns 3) Data consistency strategy 4) Fault tolerance design 5) Deployment architecture. Be specific with concrete examples.",
    "criteria": ["service_decomposition", "tradeoffs_documented", "fault_tolerance", "concrete_examples"],
})

# Task 2: Security
TASKS.append({
    "id": "sec-01",
    "category": "Security",
    "skill": "You are a senior application security engineer. Follow these rules:
1. NO production deployment without a passing security review
2. OWASP Top 10 scan is mandatory
3. Validate EVERY input at EVERY boundary
4. Rate limiting is not optional

Respond with a structured security review. Categorize findings: CRITICAL, HIGH, MEDIUM, LOW. Provide fixes for each.",
    "noskill": "You are a helpful AI assistant. Review this code for security issues.",
    "prompt": "Find ALL security issues in this code. Rate each by severity. Provide fixes:

@app.post('/api/v1/users/search')
def search_users(request):
    query = request.json.get('q')
    sql = f"SELECT id, name, email, role FROM users WHERE name ILIKE '%{query}%'"
    return {'users': [dict(r) for r in db.execute(sql)]}

@app.get('/api/v1/admin/users')
def admin_list_users():
    return {'users': [dict(u) for u in db.execute('SELECT * FROM users')]}",
    "criteria": ["sqli_detected", "auth_missing", "severity_levels", "fix_provided"],
})

# Task 3: Backend Code
TASKS.append({
    "id": "code-01",
    "category": "Backend Code",
    "skill": "You are a senior backend engineer. Follow these rules:
1. NEVER trust the client - validate EVERY input at EVERY boundary
2. Multi-step operations MUST use transactions
3. Consistent error format: {error: {code, message, details, requestId}}
4. Structured logging for every request
5. Rate limit all endpoints

Write production-grade code with proper error handling, logging, and validation.",
    "noskill": "You are a helpful AI assistant. Write the code as requested.",
    "prompt": "Implement POST /api/v1/orders endpoint in Python/FastAPI. Accept: user_id, items[{product_id, quantity}], shipping_address, payment_method_id. Validate all fields (quantity > 0). Check inventory, calculate total, create order with DB transaction. Rate limit: 10 orders per user per minute. Return: {order_id, status, total}. Include proper error handling and structured logging.",
    "criteria": ["input_validation", "error_handling", "transaction_usage", "rate_limiting", "structured_logging"],
})

# Task 4: Edge Cases
TASKS.append({
    "id": "edge-01",
    "category": "Edge Cases",
    "skill": "You are an edge case hunter. Find EVERYTHING that can break. Check:
- Input extremes (empty, null, max)
- Concurrency/race conditions
- Network failures
- Timezone/DST issues
- State corruption
- Scale (0/1/10K items)
- Integration failures
- Human errors

Document each: Scenario -> Expected Behavior -> What Actually Happens.",
    "noskill": "You are a helpful AI assistant. Find potential issues in this flow.",
    "prompt": "Analyze this order cancellation flow for edge cases:
1. User clicks Cancel Order
2. Backend checks if order status is CONFIRMED
3. Sets status to CANCELLED, triggers refund
4. Refund service reverses payment via Stripe
5. Inventory service releases reserved items
6. Notification service sends email + push
7. Returns 200 OK

Find ALL edge cases. Consider timing, concurrency, failures at each step.",
    "criteria": ["concurrency_issues", "failure_states", "idempotency", "state_machine_gaps"],
})

# Task 5: Orchestration
TASKS.append({
    "id": "orch-01",
    "category": "Orchestration",
    "skill": "You are an epic orchestrator managing large-scale projects. Follow these rules:
1. NEVER start without decomposition: project -> epics -> stories -> atomic tasks
2. Every squad gets ONLY the context it needs
3. Squads must be independently executable
4. Failure is a data point: retry -> fallback -> escalate -> circuit breaker
5. Every epic produces a learning artifact

Plan with concrete YAML examples, dependency DAGs, token budgets, monitoring rules.",
    "noskill": "You are a helpful AI assistant. Help plan this project.",
    "prompt": "Plan a 5-day project: Migrate a 250K-line Rails monolith to microservices. Extracting 4 bounded contexts: User/Auth, Orders, Payments, Notifications. Requirements: zero-downtime migration, 8 developers in 3 squads, PCI-DSS for payments, maintain existing API contracts. Provide: 1) Epic decomposition 2) Squad design with roles 3) Dependency DAG 4) Timeline with milestones 5) Failure recovery strategy 6) Monitoring/alert rules.",
    "criteria": ["decomposition", "squad_design", "dependency_dag", "failure_recovery", "token_budgeting"],
})

# --- API CALL ---
def call_model(model_id, system_prompt, user_prompt):
    payload = json.dumps({
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 1500,
        "temperature": 0.2,
    })
    
    try:
        r = subprocess.run(
            ["curl", "-s", "-w", "HTTP_CODE:%{http_code}", "--max-time", "120",
             "-H", f"Authorization: Bearer {DEEPSEEK_KEY}",
             "-H", "Content-Type: application/json",
             "-d", payload, API_URL],
            capture_output=True, text=True, timeout=130
        )
        out = r.stdout.strip()
        
        # Split response and HTTP code
        if "HTTP_CODE:" in out:
            body, code = out.rsplit("HTTP_CODE:", 1)
            code = code.strip()
        else:
            body, code = out, "0"
        
        if code != "200":
            return {"error": f"HTTP {code}", "raw": body[:300]}
        
        d = json.loads(body)
        content = d["choices"][0]["message"]["content"]
        usage = d.get("usage", {})
        return {
            "content": content,
            "tokens": usage.get("total_tokens", 0),
            "prompt_tokens": usage.get("prompt_tokens", 0),
            "completion_tokens": usage.get("completion_tokens", 0),
            "model": d.get("model", model_id),
        }
    except Exception as e:
        return {"error": str(e)[:200]}

# --- SCORING ---
def score(content, criteria):
    c = content.lower()
    scores = {}
    for crit in criteria:
        s = 0.0
        cl = crit.lower()
        # Check for criterion mentioned
        if cl.replace("_", " ") in c or cl in c:
            s += 1.5
        # Quality signals
        if "```" in content:
            s += 0.5
        if len(content) > 800:
            s += 0.5
        if any(w in c for w in ["example", "concrete", "specific", "scenario"]):
            s += 0.5
        scores[crit] = min(s, 3.0)
    return scores

# --- MAIN ---
def main():
    print("=" * 70)
    print("SKILL BENCHMARK - DeepSeek v3 vs R1 (with skill vs without)")
    print(f"Models: deepseek-v3 (chat), deepseek-r1 (reasoner)")
    print(f"Tasks: {len(TASKS)} | Calls: {len(MODELS) * len(TASKS) * 2}")
    print("=" * 70)
    
    results = {}
    start = datetime.now()
    call_num = 0
    
    for task in TASKS:
        tid = task["id"]
        print(f"
[{tid}] {task['category']}")
        results[tid] = {}
        
        for mode, sys_prompt in [("WITH_SKILL", task["skill"]), ("NO_SKILL", task["noskill"])]:
            for model_name, model_id in MODELS.items():
                call_num += 1
                key = f"{model_name}_{mode}"
                print(f"  [{call_num}/20] {model_name} {mode}...", end=" ", flush=True)
                
                r = call_model(model_id, sys_prompt, task["prompt"])
                
                if "error" in r:
                    print(f"FAIL: {r['error']}")
                    results[tid][key] = r
                else:
                    print(f"OK ({r['tokens']} tok, {len(r['content'])} char)")
                    results[tid][key] = r
                
                time.sleep(0.3)  # Rate limit
    
    elapsed = (datetime.now() - start).total_seconds()
    
    # --- RESULTS TABLE ---
    print("
" + "=" * 70)
    print("RESULTS: WITH SKILL vs WITHOUT SKILL")
    print("=" * 70)
    
    for task in TASKS:
        tid = task["id"]
        print(f"
### {tid}: {task['category']}")
        print(f"    Criteria: {', '.join(task['criteria'])}")
        print(f"    {'Model/Mode':<30} {'Score':>7} {'Tokens':>8} {'Chars':>8}")
        print(f"    {'-'*30} {'-'*7} {'-'*8} {'-'*8}")
        
        for model_name in MODELS:
            for mode in ["WITH_SKILL", "NO_SKILL"]:
                key = f"{model_name}_{mode}"
                r = results[tid].get(key, {})
                if "error" in r:
                    print(f"    {key:<30} {'ERR':>7} {'-':>8} {'-':>8}")
                else:
                    scores = score(r["content"], task["criteria"])
                    avg = sum(scores.values()) / len(scores) if scores else 0
                    print(f"    {key:<30} {avg:>7.1f} {r['tokens']:>8} {len(r['content']):>8}")
    
    # --- SKILL IMPACT SUMMARY ---
    print(f"
### SKILL IMPACT (score improvement)")
    print(f"    {'Model':<15} {'Arch':>6} {'Sec':>6} {'Code':>6} {'Edge':>6} {'Orch':>6} {'Avg':>6}")
    print(f"    {'-'*15} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*6}")
    
    for model_name in MODELS:
        improvements = []
        row = f"    {model_name:<15}"
        for task in TASKS:
            tid = task["id"]
            skill_score = sum(score(results[tid].get(f"{model_name}_WITH_SKILL", {}).get("content", ""), task["criteria"]).values())
            noskill_score = sum(score(results[tid].get(f"{model_name}_NO_SKILL", {}).get("content", ""), task["criteria"]).values())
            delta = skill_score - noskill_score
            improvements.append(delta)
            row += f" {delta:>+6.1f}"
        avg_imp = sum(improvements) / len(improvements)
        row += f" {avg_imp:>+6.1f}"
        print(row)
    
    # --- TOKEN EFFICIENCY ---
    print(f"
### TOKEN EFFICIENCY")
    for model_name in MODELS:
        skill_tok = sum(results[t["id"]].get(f"{model_name}_WITH_SKILL", {}).get("tokens", 0) for t in TASKS)
        noskill_tok = sum(results[t["id"]].get(f"{model_name}_NO_SKILL", {}).get("tokens", 0) for t in TASKS)
        delta = skill_tok - noskill_tok
        pct = (delta / noskill_tok * 100) if noskill_tok else 0
        print(f"    {model_name}: with={skill_tok:,}  without={noskill_tok:,}  delta={delta:+} ({pct:+.1f}%)")
    
    print(f"
Total time: {elapsed:.1f}s")
    
    # Save results
    save = {"timestamp": datetime.now().isoformat(), "elapsed": elapsed, "models": list(MODELS.keys()), "results": {}}
    for tid in results:
        save["results"][tid] = {}
        for key, r in results[tid].items():
            if "content" in r:
                save["results"][tid][key] = {
                    "tokens": r["tokens"], "prompt_tokens": r["prompt_tokens"],
                    "completion_tokens": r["completion_tokens"], "model": r.get("model", ""),
                    "content_preview": r["content"][:300], "chars": len(r["content"])
                }
            else:
                save["results"][tid][key] = r
    
    with open("/tmp/skill-benchmark-deepseek.json", "w") as f:
        json.dump(save, f, indent=2)
    
    print(f"Saved: /tmp/skill-benchmark-deepseek.json")

if __name__ == "__main__":
    main()
