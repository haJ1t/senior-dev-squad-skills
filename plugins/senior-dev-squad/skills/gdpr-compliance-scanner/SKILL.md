---
name: gdpr-compliance-scanner
description: "Automated GDPR compliance scanning — data flows, consent management, right-to-access, and privacy by design. Use when auditing GDPR or privacy compliance."
version: 1.0.0
platforms: [linux, macos]
---

# GDPR Compliance Scanner

## What It Does
Automatically scans codebases, data flows, and infrastructure for GDPR compliance gaps. Identifies personal data processing, checks for consent management implementation, verifies data subject rights support (access, erasure, portability), audits data retention, and flags cross-border data transfer issues. Produces compliance reports with remediation recommendations.

## Iron Laws (NEVER violate)
1. **PII is toxic by default** — Treat all personal data as a liability. Collect minimum, store minimum, retain minimum.
2. **Consent must be explicit** — Pre-checked boxes, implied consent, and "by using this service" are not valid GDPR consent.
3. **Deletion means deletion** — "Soft delete" that keeps data is not GDPR-compliant erasure. Data must be irrecoverable.
4. **Data flow documentation required** — Every PII data flow must be documented: source, processor, storage, transfer, retention.

## Red Flags (STOP immediately)
- **Unmapped PII** — Personal data found in logs, backups, or analytics without documentation → data mapping failure
- **Missing legal basis** — Processing personal data without a documented lawful basis (consent, contract, legitimate interest)
- **Cross-border transfer without safeguards** — EU data sent to non-adequate country without SCCs or BCRs → violation
- **Data subject request not honored** — System can't fulfill access, erasure, or portability request within 30-day SLA

## Common Rationalizations (self-deception)
- "We don't have EU users" → If you're accessible from the EU, GDPR applies. Geography of server is irrelevant.
- "The data is anonymized" → True anonymization is extremely hard. Pseudonymization ≠ anonymization under GDPR.
- "We'll handle compliance later" → GDPR fines are up to 4% of global revenue. Compliance debt is existential risk.

## When To Use
- Auditing a codebase for GDPR compliance before launch
- Responding to a data subject access/erasure request
- Setting up privacy-by-design practices in development
- Preparing for a Data Protection Impact Assessment (DPIA)
- Reviewing third-party processor compliance

## Human Partner Signals (escalate to human)
- **Data breach** — PII exposed or potentially exposed → DPO and legal must be notified within 72 hours
- **DPIA trigger** — Large-scale processing of sensitive data → mandatory DPIA required
- **Regulatory uncertainty** — Grey area in GDPR interpretation → legal counsel needed
- **Processor non-compliance** — Third-party vendor not meeting GDPR requirements → contract review

## Pipeline
1. Discover: scan codebase for PII processing — identify data types, storage locations, processing purposes
2. Map: document data flows — collection → processing → storage → transfer → deletion for each PII type
3. Audit: check consent mechanisms, data subject rights implementation, retention policies, processor agreements
4. Score: rate compliance maturity per GDPR article — compliant, partially compliant, non-compliant, not applicable
5. Remediate: generate prioritized remediation plan with specific code/config changes
6. Report: produce compliance report suitable for DPO review and regulatory inspection

## Verification Checklist
- [ ] All PII data flows documented with lawful basis for processing
- [ ] Consent mechanism provides explicit opt-in (no pre-checked boxes)
- [ ] Data subject access request can be fulfilled within 30 days
- [ ] Data erasure removes data irrecoverably (no soft-delete)
- [ ] Cross-border transfers have appropriate safeguards (SCCs, BCRs, adequacy decision)
- [ ] Data retention periods defined and enforced automatically
- [ ] Third-party processors have signed Data Processing Agreements (DPAs)

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

## Related Skills
- `soc2-audit-prep` — SOC 2 and GDPR share data protection requirements
- `data-retention-manager` — Automated data retention enforcement
- `policy-as-code` — Compliance rules encoded as automated policies
- `cloud-security-auditor` — Cloud infrastructure compliance scanning
