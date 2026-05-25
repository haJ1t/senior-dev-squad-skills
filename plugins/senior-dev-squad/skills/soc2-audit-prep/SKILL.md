---
name: soc2-audit-prep
description: "SOC 2 audit prep, trust services criteria mapping, control documentation, evidence collection. Use when preparing for a SOC 2 audit or compliance review."
version: 1.0.0
platforms: [linux, macos]
---

# SOC 2 Audit Prep

## What It Does
Prepares organizations for SOC 2 Type I and Type II audits by mapping existing controls to Trust Services Criteria (Security, Availability, Confidentiality, Processing Integrity, Privacy), identifying control gaps, generating control documentation, and automating evidence collection. Reduces audit preparation time from months to weeks.

## Iron Laws (NEVER violate)
1. **Evidence is timestamped** — Every control must have timestamped evidence proving it was operating during the audit period. Screenshots without timestamps are worthless.
2. **Controls must be operational, not aspirational** — "We plan to implement this" counts for nothing in an audit. Controls must be running.
3. **Segregation of duties** — No single person can both perform an action and approve it. Developer who deploys can't be the one who approves the deployment.
4. **Vendor risk is your risk** — Third-party vendors processing your data are in-scope. Their SOC 2 report covers your subservice organizations.

## Red Flags (STOP immediately)
- **Control gap** — Required TSC criterion has no corresponding control → must implement before audit
- **Evidence gap** — Control exists but no evidence it operated during audit period → observation window may need extension
- **Segregation violation** — Same person approved and executed a critical change → control design failure
- **Vendor without SOC 2** — Critical vendor processing sensitive data has no SOC 2 report → risk acceptance or vendor change

## Common Rationalizations (self-deception)
- "We're too small for SOC 2" → SOC 2 is often a sales requirement. No SOC 2 = no enterprise customers.
- "Our controls are good enough, we don't need documentation" → Undocumented controls don't exist in an auditor's eyes.
- "SOC 2 is just paperwork" → SOC 2 operationalizes security. Poor controls = real security gaps.

## When To Use
- Preparing for first SOC 2 Type I or Type II audit
- Annual SOC 2 audit preparation and evidence collection
- Gap analysis between current controls and TSC requirements
- Setting up continuous controls monitoring for SOC 2
- Vendor risk assessment using their SOC 2 reports

## Human Partner Signals (escalate to human)
- **Scope decision** — Which TSC criteria to include in audit scope → executive decision
- **Auditor selection** — Choosing between CPA firms → procurement and budget decision
- **Exception approval** — Control failure needs formal exception with compensating control → management sign-off
- **Report distribution** — Who receives the SOC 2 report → legal and sales decision

## Pipeline
1. Scope: define audit scope — which trust services criteria, which systems, which period
2. Map: inventory existing controls and map to TSC criteria (CC1-CC9 + supplemental criteria)
3. Gap: identify missing controls and insufficient evidence for each criterion
4. Remediate: implement missing controls, establish evidence collection automation
5. Document: create control descriptions, system description, and management assertion
6. Evidence: collect and organize evidence for the audit period
7. Review: internal readiness assessment before auditor engagement

## Verification Checklist
- [ ] All in-scope TSC criteria mapped to operational controls
- [ ] Evidence collected for entire audit period (no gaps)
- [ ] Segregation of duties verified for all critical change processes
- [ ] Vendor SOC 2 reports collected for all critical subservice organizations
- [ ] Control descriptions documented with control owner, frequency, and evidence type
- [ ] Management assertion drafted and reviewed by leadership
- [ ] Readiness assessment completed with no critical findings

## Related Skills
- `gdpr-compliance-scanner` — GDPR and SOC 2 share data protection and access control requirements
- `policy-as-code` — Automated policy enforcement reduces SOC 2 evidence collection burden
- `data-retention-manager` — Data lifecycle management for availability and confidentiality criteria
- `cloud-security-auditor` — Cloud control mapping to SOC 2 criteria
