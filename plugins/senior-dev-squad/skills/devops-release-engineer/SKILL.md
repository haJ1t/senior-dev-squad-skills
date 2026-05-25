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

## Red Flags — STOP

Friday deployment = weekend incident. "We'll add monitoring later" = users will tell you it's down. "Skip the rollback plan, it's a small change" = you'll need it.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "We'll add monitoring after deployment" | You'll notice it's down when users complain. |
| "Friday deploy is fine" | Friday deploy is how weekend incidents start. |
| "Rollback is just reverting the commit" | Schema migrations make rollbacks hard. Test them. |
| "Staging is close enough to production" | If staging isn't identical, it's not staging. |

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

## Related Skills

- **ship-readiness-checklist** — use as the final gate immediately before deploying; devops-release-engineer sets up the infrastructure this checklist verifies
- **security-reviewer** — use for Gate 3 when secrets management or container hardening needs a deeper audit
- **backend-senior-engineer** — use to ensure application-level health check endpoints and structured logging are implemented correctly
- **test-engineer** — use to confirm integration and smoke tests are in place for the CI pipeline's deploy stage
- **edge-case-hunter** — use to verify the rollback plan covers failure scenarios in the migration and deployment sequence
