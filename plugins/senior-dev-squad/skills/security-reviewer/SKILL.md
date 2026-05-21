---
name: security-reviewer
description: "OWASP Top 10, injection, XSS, IDOR, secrets, SSRF, prompt injection, concrete fixes, LLM anti-pattern detection. Use when auditing code for security vulnerabilities."
version: 2.0.0
---

# Security Reviewer v2

## Overview

Find security vulnerabilities before they find you. Security is not a final audit — it's an integrated gate at every development stage. **Benchmark-proven: without structured guidance, models miss 57% of critical findings (tested across Claude, GPT, Gemini, DeepSeek).**

**Core principle:** SECURITY IS EVERYONE'S RESPONSIBILITY AND EVERY STAGE'S GATE.

## The Iron Law

```
NO PRODUCTION DEPLOYMENT WITHOUT A PASSING SECURITY REVIEW.
EVERY FINDING MUST INCLUDE: OWASP mapping + concrete fix code + exploit scenario.
```

## MANDATORY Output Schema

**YOU MUST produce output in this EXACT structure. No exceptions.**

```markdown
# Security Review: [Endpoint/Feature Name]

## CRITICAL Findings (Block Deployment)

### C1: [Title] | OWASP: [A01-A10]
**Location:** [file:line]
**Exploit Scenario:** [Step-by-step how attacker exploits this]
**Impact:** [What happens if exploited — data breach, RCE, financial loss]
**Fix:**
```[language]
[Complete, compilable fix code — not pseudocode, not "consider using"]
```

## HIGH Findings (Fix Before Merge)

### H1: [Title] | OWASP: [A01-A10]
[Same format as CRITICAL]

## MEDIUM Findings (Fix This Sprint)

### M1: [Title] | OWASP: [A01-A10]
[Same format]

## LOW / Informational
[Brief bullet list]

## Security Posture Summary
- Endpoints reviewed: [count]
- CRITICAL: [count] — MUST fix before deployment
- HIGH: [count] — MUST fix before merge
- MEDIUM: [count] — Fix this sprint
- LOW: [count] — Document and track
- Overall: [PASS / FAIL — FAIL if any CRITICAL]
```

## LLM Anti-Patterns (BENCHMARK FINDINGS)

**These are mistakes models CONSISTENTLY make. Guard against them:**

| Anti-Pattern | Example | Why Wrong | Correct Approach |
|-------------|---------|-----------|-----------------|
| **Vague fixes** | "Use parameterized queries" | No code, model assumes dev knows how | Show exact code: `cursor.execute("SELECT ... WHERE id = ?", (user_id,))` |
| **Missing severity** | "There's an SQL injection" | No prioritization | Always tag: `CRITICAL \| OWASP A03: Injection` |
| **Forgotten auth check** | Only flags SQLi, misses missing auth | Single-focus blindness | Run A01 (Access Control) SEPARATELY before A03 (Injection) |
| **Rate limiting ignored** | "Add rate limiting" as afterthought | OWASP A05 + DoS vector | Always check: is there a rate limiter? If not → HIGH finding |
| **No exploit scenario** | "SQL injection possible" | Not actionable | Show: `curl -X POST ... -d '{"q":"'\'' OR 1=1--"}'` |
| **PII exposure missed** | Returns all user fields including email/role | Privacy violation | Flag: `SELECT *` returning `email, role` → HIGH (PII + privilege info leak) |
| **Over-flagging** | "Missing Content-Security-Policy header" as CRITICAL | Severity inflation | CSP is MEDIUM unless there's inline scripts (then HIGH) |

## When to Use

**Use this ESPECIALLY when:**
- Someone says "we'll add auth later" (you won't — add it now)
- The PR adds a file upload feature, payment processing, or AI/LLM integration
- New dependencies are introduced

**Don't skip when:**
- "It's an internal tool" (internal compromise is still a breach)
- "We're using an ORM so SQL injection isn't possible" (it is in raw queries)

## Security by Stage

### Stage 1: Threat Model (During Spec & Architecture)

Before ANY code, answer STRIDE:

| Threat | Question | Mitigation |
|--------|----------|-----------|
| **Spoofing** | Can identity be faked? | Strong auth, MFA |
| **Tampering** | Can data be modified in transit? | HTTPS, signed payloads |
| **Repudiation** | Can user deny action? | Immutable audit logs |
| **Information Disclosure** | Can data leak? | Encryption, access control |
| **Denial of Service** | Can system be overwhelmed? | Rate limiting, quotas |
| **Elevation of Privilege** | Can user escalate access? | RBAC, RLS, least privilege |

### Stage 2: Code Review (OWASP Top 10 Scan)

**A01: Broken Access Control**
```
☐ IDOR: Can User A access User B's data? (TEST THIS)
☐ Role escalation: Can user perform admin actions?
☐ Mass assignment: Can user set fields they shouldn't?
☐ Missing auth: Is EVERY endpoint behind authentication?
```

**A03: Injection**
```
☐ SQL: Parameterized queries ONLY. String interpolation = INSTANT CRITICAL
☐ NoSQL: $where, $gt operator bypasses
☐ Command: User input in exec()/spawn() = CRITICAL
☐ Template: User input in templates = RCE risk
```

**A05: Security Misconfiguration**
```
☐ CORS: NOT Access-Control-Allow-Origin: *
☐ Debug mode disabled in production
☐ Security headers: CSP, X-Frame-Options, X-Content-Type-Options
☐ Rate limiting on ALL endpoints (not just "important" ones)
```

**A06: Vulnerable Components**
```
☐ npm audit / pip audit passing (0 critical, 0 high)
☐ Dependencies pinned (not ^ ranges in production)
☐ SBOM generated
```

### Stage 3: LLM/Prompt Injection (If AI App)

```typescript
// THREE-LAYER DEFENSE FOR LLM
// 1. Pre-filter: Detect + block injection attempts
if (await detectInjection(userInput)) return block('Injection detected')
// 2. PII redaction: Strip sensitive data before LLM call
const { redacted, replaced } = redactor.redact(userInput)
// 3. Post-filter: Validate LLM output before showing user
const { passed, sanitized } = await guardrails.validate(llmOutput)
```

### Stage 4: Infrastructure & Secrets

```
☐ Docker: non-root user, no :latest, regular scans
☐ Secrets: NEVER in env files committed to git
☐ Network: Internal services not exposed publicly
☐ Backup: Encrypted, tested restore
```

## Severity Guide (MANDATORY reference)

| Severity | Definition | Examples | Action |
|----------|-----------|----------|--------|
| 🔴 CRITICAL | Direct path to data breach, RCE, or system compromise | SQL injection, auth bypass, hardcoded secrets, RCE | **Block deployment. Fix immediately.** |
| 🟠 HIGH | Significant security weakness, likely exploitable | Missing auth on sensitive endpoint, PII exposure, IDOR | **Block merge. Fix before merge.** |
| 🟡 MEDIUM | Security best practice violation, harder to exploit | Missing rate limiting, CORS misconfiguration, verbose errors | **Fix within sprint.** |
| 🔵 LOW | Defense-in-depth improvement, informational | Missing security header, debug log in production | **Document, fix when convenient.** |

## Red Flags — STOP and Follow Process

- "We'll add auth later" — You won't. Add it now.
- "No one will find this unauthenticated endpoint" — Security through obscurity is not security.
- "The ORM prevents all injection" — Raw queries, ORDER BY injection, dynamic table names exist.
- "We don't need rate limiting, we trust our users" — DDoS doesn't need authentication.
- "I'll just flag it and move on" — Every finding needs OWASP mapping + concrete fix code.

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "You marked that as MEDIUM but it's clearly a blocker" — You under-classified a severity; re-read the Severity Guide and reclassify
- "Where's the fix code? You just said 'sanitize inputs'" — You produced a vague fix without concrete, runnable code
- "You didn't check the auth on this endpoint at all" — You focused on injection or other OWASP categories and skipped A01 entirely
- "That's not how this exploit would actually work" — Your exploit scenario was theoretical; write a concrete curl or payload example
- "You're flagging too many things as CRITICAL" — You inflated severity; cross-check each finding against the Severity Guide definition before assigning CRITICAL

**When you see these:** STOP. Return to the MANDATORY Output Schema, re-score the affected finding against the Scoring Rubric, and reissue the corrected finding before continuing.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll do security review later" | There is no later. Schedule it now or it won't happen. |
| "The ORM prevents SQL injection" | Raw queries, ORDER BY injection, and dynamic table names don't use the ORM. |
| "It's internal, no one will attack" | Insider threats are responsible for 30% of breaches. |
| "Rate limiting adds complexity" | A DDoS attack adds more. |
| "The fix is obvious, I don't need to write code" | Obvious to you is not obvious to the junior dev fixing it at 2 AM. Write the code. |

## Few-Shot Examples (MANDATORY Reference)

### ❌ BAD Output (Vague — most common error in benchmarks)

```markdown
## SQL Injection
The search endpoint has SQL injection. Use parameterized queries instead.
```
**Why it is bad:** No OWASP mapping, no severity, no exploit scenario, no fix code.

### ✅ GOOD Output (As it should be)

```markdown
### C1: SQL Injection in User Search | OWASP: A03 Injection
**Location:** search_users(), line 3
**Exploit Scenario:** Attacker sends `{"q": "' OR 1=1--"}` → query becomes 
  `SELECT id, name, email, role FROM users WHERE name ILIKE '%' OR 1=1--%'`
  → returns ALL users including emails and roles
**Impact:** Complete data breach — attacker extracts all user PII (email, role enumeration)
**Fix:**
```python
@app.post('/api/v1/users/search')
def search_users(request):
    query = request.json.get('q', '')
    if not query or len(query) > 100:
        raise HTTPException(status_code=400, detail="Invalid query")
    # PARAMETERIZED — no string interpolation
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, name FROM users WHERE name ILIKE %s LIMIT 50",
        (f"%{query}%",)
    )
    return {"users": [dict(r) for r in cursor.fetchall()]}
```
**Note:** Also removed email/role from SELECT — PII minimization (see H1 below)
```

### ❌ BAD: Missing auth flag omitted
```markdown
## Missing Authentication
The admin endpoint has no auth. Add authentication middleware.
```
**Why it is bad:** Absence of auth is CRITICAL, not HIGH or MEDIUM. No fix code.

### ✅ GOOD: Auth correctly flagged as CRITICAL
```markdown
### C2: Unauthenticated Admin Endpoint | OWASP: A01 Broken Access Control
**Location:** admin_list_users(), line 9
**Exploit Scenario:** Attacker sends `GET /api/v1/admin/users` with no auth header
  → receives full user list including emails, roles, internal IDs
**Impact:** Privilege escalation + full user enumeration. Attacker gains admin-level data access.
**Fix:**
```python
from fastapi import Depends
from .auth import get_current_admin

@app.get('/api/v1/admin/users')
def admin_list_users(current_user = Depends(get_current_admin)):
    # get_current_admin raises 401 if no auth, 403 if not admin
    users = db.execute("SELECT id, name FROM users LIMIT 100").fetchall()
    return {"users": [dict(u) for u in users]}
```
**Note:** `get_current_admin` checks JWT validity AND admin role. Two-layer auth.
```

## Model-Specific Calibration (BENCHMARK FINDINGS)

| Model | Tendency | Calibration |
|-------|---------|-------------|
| **Claude Sonnet 4** | Most detailed, automatically performs OWASP mapping, but sometimes over-flags | Do not force "Find minimum 3 CRITICAL/HIGH findings" — Claude tends to classify everything as CRITICAL |
| **GPT-4o** | Medium detail, good fix codes but tends to skip auth checks | "Check A01 (Access Control) SEPARATELY before A03 (Injection)" — GPT often skips auth checks |
| **Gemini 2.5 Pro** | Shortest response, consistent severity classification but weak exploit scenario | "For EVERY finding, write a curl command showing the exploit" — Gemini skips exploit scenarios |
| **DeepSeek V3** | Most economical, but 57% less detailed without skill. Good with skill but fix codes are short | "Write complete, runnable fix code — not one-liners" — DeepSeek keeps fixes short |

## Scoring Rubric (Self-Evaluation)

Score each security review output according to the following criteria:

| Criterion | 0 points | 1 point | 2 points |
|-----------|----------|---------|----------|
| **OWASP mapping** | No OWASP reference at all | Exists in some findings | A01-A10 mapping in EVERY finding |
| **Severity accuracy** | At the level of "there is a problem" | CRITICAL/HIGH/MEDIUM exist but incorrectly assigned | Correct severity + matches its definition |
| **Exploit scenario** | None | "SQL injection possible" | Step-by-step exploit with curl command |
| **Fix code** | "Use parameterized queries" | Code exists but incomplete | Complete, executable fix code |
| **PII awareness** | Endpoint returning SELECT * not noticed | Noticed but no fix | Noticed + SELECT restricted |
| **Auth check** | Missing auth not noticed | Noticed but low severity | Flagged as CRITICAL + fix |
| **Rate limiting** | Not checked at all | "Rate limiting should be added" | Concrete rate limiter code + 429 response |
| **Output format** | Free text | Partially structural | Full compliance with the MANDATORY schema |

**Passing score: 12/16** (At least 1 point in every critical area)

## Chaining (Auto-Trigger)

**Complete → auto-trigger:**
- `mitre-attack-mapper` — map findings to the MITRE ATT&CK framework
- `nist-csf-scanner` — NIST CSF compliance gap analysis
- `supply-chain-verifier` — dependency CVE scanning
- `cloud-security-auditor` — CIS benchmark if cloud deployment exists

## Related Skills

- **backend-senior-engineer** — implements auth, validation this skill reviews
- **ai-app-security-pro** — deep dive on LLM-specific threats
- **spec-first-development** — threat model during spec phase
- **devops-release-engineer** — infrastructure security review
- **supply-chain-verifier** — dependency CVE scanning
- **mitre-attack-mapper** — map findings to MITRE ATT&CK framework

## Verification Checklist (Before Signing Off)

- [ ] EVERY finding has: OWASP mapping + severity + exploit scenario + concrete fix code
- [ ] Output follows MANDATORY schema EXACTLY
- [ ] No vague fixes ("use parameterized queries" without code = FAIL)
- [ ] AuthN + AuthZ verified for EVERY protected endpoint
- [ ] Rate limiting checked on ALL endpoints (not skipped for "internal" ones)
- [ ] No secrets in code (verified by scanner)
- [ ] PII exposure checked (no SELECT * returning sensitive fields)
- [ ] LLM anti-patterns reviewed (did I make any of the 7 benchmark mistakes?)
- [ ] Security Posture Summary included with PASS/FAIL verdict
