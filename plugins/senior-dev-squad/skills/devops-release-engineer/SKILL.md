---
name: devops-release-engineer
description: "Docker, CI/CD, secrets, deployment checklist, rollback, health checks. Use when deploying, releasing, or troubleshooting CI/CD pipelines."
---

# DevOps Release Engineer

## Overview

Make the application production-ready. Every service must be containerized, deployable, monitorable, and recoverable. No manual steps. No "works on my machine."

**Core principle:** IF IT'S NOT AUTOMATED, IT WON'T BE DONE. IF IT CAN'T BE ROLLED BACK, IT CAN'T BE DEPLOYED.

## The Iron Law

```
EVERY DEPLOYMENT MUST HAVE A TESTED ROLLBACK PLAN
```

Deploying without a rollback plan is not deploying — it's gambling.

## When to Use

**Use this when:**
- Before the first deployment
- When adding a new service or dependency
- When debugging deployment issues
- Before a production release

**Use this ESPECIALLY when:**
- Someone says "let's just merge and deploy, it's a small change"
- The deployment involves a database migration
- You're deploying on a Friday afternoon
- Someone says "we'll fix it in prod"

**Don't skip when:**
- "It's a simple change" (simple changes can break production too)
- "We've done this a hundred times" (complacency causes incidents)
- "The rollback is easy, just revert" (schema migrations are hard to revert)

## Production Readiness (7 Gates)

### Gate 1: Containerization

```
☐ Multi-stage Dockerfile (dev deps never in production image)
☐ Non-root user (never run as root)
☐ Specific base image tags (never :latest)
☐ Health check in Dockerfile
☐ .dockerignore (excludes node_modules, .git, tests)
```

### Gate 2: CI/CD Pipeline

```
☐ Quality stage: lint + type-check + unit tests + security scan
☐ Build stage: production build + Docker image
☐ Deploy stage: staging → integration tests → production
☐ All stages must pass before merge
```

### Gate 3: Secrets Management

```
☐ No secrets in .env files committed to git
☐ .env.example committed with placeholder values
☐ Secrets stored in secret manager (not env vars)
☐ Access to secrets logged and audited
```

### Gate 4: Rollback Plan

```yaml
Rollback Trigger:
  - Error rate increase > 5%
  - P50 latency increase > 100ms
  - 5xx rate > 1%
  - Any P1 alert fires

Steps:
  1. git revert <deploy-commit>
  2. Re-run CI/CD pipeline
  3. Or: swap load balancer to previous version
  4. Run rollback migration (if schema changed)
  5. Verify health checks pass
  6. Monitor error rates for 15 minutes
```

### Gate 5: Monitoring

```
☐ Structured JSON logging on every service
☐ Health check endpoint: /health, /health/ready, /health/live
☐ Metrics: latency, error rate, request rate, saturation
☐ Alerts configured for error rate, latency, and downtime
```

### Gate 6: Deployment Checklist

```
☐ Tests pass (CI green)
☐ Lint + type-check pass
☐ Build succeeds
☐ No known CVEs in dependencies
☐ Database migrations are additive + reversible
☐ Migration tested against staging data
☐ Env vars documented in .env.example
☐ Rollback plan documented
```

### Gate 7: Release

```
☐ Release notes written
☐ Version bumped (semver)
☐ Changelog updated
☐ Stakeholders notified
☐ Post-release monitoring plan in place
```

## Decision Tree

Use this before every release to resolve the four recurring judgment calls.

```
1. WHICH DEPLOY STRATEGY?
   │
   ├─ Can I run two versions in parallel (DB schema is backward-compatible)?
   │    ├─ Yes, and traffic split is valuable → CANARY
   │    │     (start at 1–5 %, watch error rate for 15 min, ramp to 100 %)
   │    └─ Yes, but instant cutover is fine → BLUE-GREEN
   │          (keep old stack warm for ≥ 30 min, swap LB, tear down only after monitors green)
   │
   └─ Cannot run two versions in parallel (breaking schema, single DB writer)?
        ├─ Downtime is acceptable → RECREATE
        │     (schedule maintenance window, announce to stakeholders)
        └─ Downtime is NOT acceptable → ROLLING (with expand-contract migration)
              (each pod replaced one-by-one; requires old + new code to coexist)

2. ROLL BACK or FORWARD-FIX?
   │
   ├─ Error rate > threshold AND root cause is unknown → ROLL BACK immediately
   ├─ Error rate > threshold AND fix is a one-line config change → FORWARD-FIX
   │     (only if fix can be deployed in < 10 min and is lower risk than rollback)
   └─ Error rate is acceptable but UX is degraded → FORWARD-FIX with feature flag disable

3. MIGRATION BEFORE or AFTER DEPLOY?
   │
   ├─ Additive (ADD COLUMN, CREATE TABLE, ADD INDEX CONCURRENTLY) → BEFORE deploy
   │     (old binary ignores new column; new binary uses it — safe overlap)
   ├─ Destructive (DROP COLUMN, DROP TABLE, RENAME COLUMN) → AFTER deploy + after rollback window closes
   │     (old binary must be gone before the column it reads disappears)
   └─ Data backfill on large table → ASYNC background job, never in a blocking migration

4. WHAT GATES PROMOTION TO PROD?
   │
   ├─ CI green (all tests + lint + security scan) → required
   ├─ Staging smoke tests pass → required
   ├─ /health/ready returns 200 on new pods → required (readiness gate)
   ├─ Error rate stable for ≥ 5 min post-deploy (canary) → required
   └─ Rollback tested against staging in this release cycle → required
```

## Red Flags — STOP

- **Deploy + destructive migration in the same pipeline step.** DROP COLUMN while the old binary is still serving traffic corrupts data. Use expand-contract: add column → deploy new binary → backfill → drop column in a follow-up release.
- **No rollback path documented before deploy begins.** "We'll revert the commit" is not a rollback plan when a schema migration has run.
- **No health check / readiness gate after deploy.** The load balancer routes traffic the moment a container starts, not when it is ready. Without `/health/ready`, you're sending real requests to a cold instance.
- **Secrets in env vars or committed to the repo.** `DATABASE_URL=postgres://...` in a `.env` file checked into git is a breach waiting to be found.
- **Friday-afternoon deploy with no monitoring watch.** If you can't stay for 30 minutes of post-deploy monitoring, the deploy waits until Monday.
- **"Small change" skips Gates 1–7.** The gate list exists because small changes have caused the largest incidents.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll add monitoring after deployment" | You'll notice it's down when users complain, not from a dashboard. |
| "Friday deploy is fine, it's a one-liner" | Friday deploys are how weekend incidents start. The size of the change is irrelevant. |
| "Rollback is just reverting the commit" | Schema migrations do not revert with `git revert`. Test the rollback migration against staging data. |
| "Staging is close enough to production" | If staging has a different DB version, different secret store, or synthetic data, it is not staging — it is theater. |
| "We'll run the migration after deploy, it's additive" | Additive columns can still lock tables on large datasets. Measure migration time against prod row counts before the release window. |
| "Health checks are handled by the platform" | Kubernetes/ECS liveness ≠ readiness. A container that has started but hasn't warmed connections is not ready. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "How do we roll this back if something goes wrong?" — Gate 4 was skipped or the rollback plan was not communicated
- "Why did production get a secret that wasn't in staging?" — secrets management is inconsistent between environments
- "The container is running as root" — Gate 1 non-root user requirement was missed
- "We don't have an alert for this" — Gate 5 monitoring was treated as optional
- "Can you walk me through what the pipeline does?" — CI/CD stages are not documented or not visible

**When you see these:** STOP. Return to the relevant gate, complete it fully, and verify it against staging before proceeding.

## Verification

- [ ] Dockerfile uses a multi-stage build and runs as a non-root user
- [ ] Base image uses a specific version tag, not `:latest`
- [ ] Dockerfile includes a `HEALTHCHECK` instruction
- [ ] `.dockerignore` excludes `node_modules`, `.git`, test directories, and local env files
- [ ] CI pipeline has quality, build, and deploy stages in that order — all must pass before merge
- [ ] No secrets committed to git; `.env.example` has placeholder values for all required vars
- [ ] All production secrets are in a secret manager with access logging enabled
- [ ] Rollback plan is written out step by step, including the migration rollback command if applicable
- [ ] Rollback trigger criteria are defined with numeric thresholds (error rate, latency, alert name)
- [ ] Rollback plan has been executed against staging at least once
- [ ] `/health`, `/health/ready`, and `/health/live` endpoints respond correctly post-deploy
- [ ] Alerts configured for error rate, p50/p99 latency, and downtime before production deployment
- [ ] Release notes written and stakeholders notified before the release window

## Worked Example

See [REFERENCE.md](./REFERENCE.md) for a complete end-to-end release walk-through: CI pipeline snippet, expand-contract migration ordering, canary deploy config, health-check readiness gate, and automated rollback trigger — all narrated step-by-step.

## Related Skills

- **ship-readiness-checklist** — use as the final gate immediately before deploying; devops-release-engineer sets up the infrastructure this checklist verifies
- **security-reviewer** — use for Gate 3 when secrets management or container hardening needs a deeper audit
- **backend-senior-engineer** — use to ensure application-level health check endpoints and structured logging are implemented correctly
- **test-engineer** — use to confirm integration and smoke tests are in place for the CI pipeline's deploy stage
- **edge-case-hunter** — use to verify the rollback plan covers failure scenarios in the migration and deployment sequence
