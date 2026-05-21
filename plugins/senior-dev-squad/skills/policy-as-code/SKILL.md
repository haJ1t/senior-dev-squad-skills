---
name: policy-as-code
description: "Policy-as-code with Open Policy Agent (OPA) — compliance, security, and operational rules as versioned code. Use when encoding governance rules in OPA/Rego."
version: 1.0.0
platforms: [linux, macos]
---

# Policy as Code

## What It Does
Implements governance, security, and operational policies as version-controlled, testable, and automatically enforced code. Uses Open Policy Agent (OPA) and Rego language to encode rules covering infrastructure compliance (Terraform, Kubernetes), API authorization, data access control, and CI/CD pipeline gates. Policies are treated with the same rigor as application code — tested, reviewed, and deployed through CI/CD.

## Iron Laws (NEVER violate)
1. **Policy is code, code is tested** — Every policy must have unit tests covering allow, deny, and edge cases. Untested policies are trust theater.
2. **Default deny** — All policies default to deny. Explicit allow rules only. A missing policy = blocked action, not an open door.
3. **Policy decisions are auditable** — Every policy evaluation must log: policy name, input, decision (allow/deny), and reasoning. "Denied" without reason is unacceptable.
4. **Policy as guardrail, not gatekeeper** — Policies enforce non-negotiable rules. They are not a substitute for human judgment in ambiguous cases.

## Red Flags (STOP immediately)
- **Policy bypass** — Code path that circumvents policy evaluation → security vulnerability
- **Policy regression** — Policy change that accidentally allows previously denied actions → test coverage gap
- **Policy conflict** — Two policies produce contradictory decisions for the same input → policy architecture issue
- **Performance degradation** — Policy evaluation adds significant latency → optimization or caching needed

## Common Rationalizations (self-deception)
- "We'll add policies later" → Policies added after deployment are reactive. Security should be proactive.
- "The team knows not to do that" → Human knowledge doesn't scale. Policies scale automatically.
- "OPA is overkill for our size" → Even small teams benefit from automated guardrails. Manual review doesn't scale past 3 people.

## When To Use
- Enforcing infrastructure compliance (no open S3 buckets, minimum TLS version)
- Implementing fine-grained API authorization
- Setting up CI/CD pipeline gates (can't deploy without security scan)
- Managing Kubernetes admission control
- Automating compliance checks (GDPR, SOC 2, PCI)

## Human Partner Signals (escalate to human)
- **Policy exception** — Legitimate need to bypass a policy → exception process with approval and time limit
- **Policy dispute** — Team disagrees with policy → policy review and modification, not bypass
- **Novel scenario** — Policy can't evaluate a new type of input → policy gap; extend policy language
- **Regulatory change** — New regulation requires new policies → legal review of policy language

## Pipeline
1. Identify: determine what should be governed — infrastructure, API access, data, CI/CD
2. Design: write policies in Rego — define rules, inputs, and decision outputs
3. Test: create test suite covering allow, deny, and edge cases for each policy
4. Integrate: deploy OPA as sidecar, daemon, or library; integrate with enforcement points
5. Monitor: track policy decisions — allow rate, deny rate, decision latency, policy violations
6. Audit: review policy decisions periodically; identify patterns that suggest policy refinement
7. Evolve: update policies as requirements change, maintaining backward compatibility where possible

## Verification Checklist
- [ ] Every policy has unit tests covering allow, deny, and at least 3 edge cases
- [ ] Default deny enforced — unhandled inputs are denied, not allowed
- [ ] Policy decisions logged with full context (input, decision, policy name, timestamp)
- [ ] Policy evaluation latency within SLA (<10ms for API authorization)
- [ ] No code paths that bypass policy evaluation
- [ ] Policy change process includes code review and testing (same as application code)
- [ ] Exception process defined with approval workflow and automatic expiration



## Output Schema (MANDATORY)

```markdown
# [Review Type]: [Target]
## CRITICAL Findings
### C1: [Title] | [Framework]: [ID]
**Finding:** [What]
**Impact:** [Why matters]
**Fix:** [Concrete fix — code, not words]
## HIGH Findings
[Same format]
## MEDIUM / LOW
[Same format]
## Summary
- CRITICAL: N, HIGH: N, MEDIUM: N
- Verdict: PASS/FAIL
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| Vague fixes ("add validation") | Not actionable | Show exact code |
| Missing severity tag | No prioritization | Always CRITICAL/HIGH/MEDIUM/LOW |
| Single-focus blindness | Misses related issues | Scan ALL categories separately |
| No framework mapping | Can't track compliance | Map to OWASP/MITRE/NIST |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Finding completeness | Missed major issues | Found most | All issues found |
| Severity accuracy | None/random | Some correct | All correctly rated |
| Fix quality | "Fix it" | Partial code | Complete, runnable fix |
| Framework mapping | None | Some mapped | All mapped to framework |
| Output format | Free text | Partial structure | Schema-compliant |

**Pass: 8/10**
## Related Skills
- `gdpr-compliance-scanner` — GDPR rules encoded as OPA policies
- `soc2-audit-prep` — SOC 2 controls automated through policy-as-code
- `cloud-security-auditor` — Cloud compliance policies enforced via OPA
- `terraform-pro` — Terraform compliance policies (no open security groups, encrypted storage)
