# DevOps Release Engineer — Worked Example

A complete release from build to verified production, narrated step by step.
Scenario: Node.js API service, PostgreSQL, GitHub Actions CI, Kubernetes target, canary deploy strategy.

---

## 1. Build Stage (CI)

```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check
      - run: npm run test:unit -- --coverage
      - uses: aquasecurity/trivy-action@master
        with:
          scan-type: fs
          exit-code: '1'
          severity: CRITICAL,HIGH

  build:
    needs: quality
    runs-on: ubuntu-latest
    outputs:
      image: ${{ steps.meta.outputs.tags }}
      digest: ${{ steps.push.outputs.digest }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=sha,prefix=,format=short
      - id: push
        uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

**Why:** Quality gate runs first — no image built if lint, types, tests, or CVE scan fails. Image is tagged with the short commit SHA, not `latest`.

---

## 2. Migration — Expand-Contract Ordering

This release adds a `user_timezone` column. The old binary does not read it; the new binary writes and reads it.

```sql
-- migration/001_add_user_timezone.sql  (run BEFORE new binary deploys)
ALTER TABLE users ADD COLUMN timezone VARCHAR(64);
-- No NOT NULL constraint yet — old binary cannot supply it.
-- No DROP of old columns — old binary still reads them.
```

Deploy order:
1. Run migration → `timezone` column exists but is nullable. Old binary unaffected.
2. Deploy new binary → reads and writes `timezone`.
3. (Next release) Backfill nulls, add `NOT NULL`, then optionally drop the old column.

```yaml
  migrate:
    needs: build
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Run migration
        env:
          DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
        run: |
          npx db-migrate up
          echo "Migration complete — verifying row count"
          psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM schema_migrations;"
```

**Never run a destructive migration (DROP COLUMN, RENAME) before the old binary is fully retired and the rollback window has closed.**

---

## 3. Canary Deploy

```yaml
  deploy-staging:
    needs: migrate
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy to staging (100%)
        run: |
          kubectl set image deployment/api api=${{ needs.build.outputs.image }} \
            --namespace=staging
          kubectl rollout status deployment/api --namespace=staging --timeout=5m

  deploy-prod-canary:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Canary — route 5% of traffic to new pods
        run: |
          # Argo Rollouts example; adapt for Flagger / weighted Ingress / etc.
          kubectl argo rollouts set image rollout/api api=${{ needs.build.outputs.image }} \
            --namespace=production
          kubectl argo rollouts promote api --namespace=production --full=false
          echo "Canary at 5%. Waiting 10 min before promotion."

      - name: Wait and observe
        run: sleep 600   # 10 minutes at canary weight

      - name: Check error rate before promoting
        env:
          PROM_URL: ${{ secrets.PROMETHEUS_URL }}
        run: |
          ERROR_RATE=$(curl -s "$PROM_URL/api/v1/query" \
            --data-urlencode 'query=rate(http_requests_total{status=~"5..",version="canary"}[5m]) / rate(http_requests_total{version="canary"}[5m])' \
            | jq '.data.result[0].value[1]' -r)
          echo "Canary error rate: $ERROR_RATE"
          python3 -c "
          rate = float('$ERROR_RATE')
          if rate > 0.01:
              raise SystemExit('ERROR RATE > 1% — aborting promotion')
          print('Error rate acceptable — promoting canary to 100%')
          "

      - name: Promote to 100%
        run: |
          kubectl argo rollouts promote api --namespace=production --full
          kubectl argo rollouts status api --namespace=production --timeout=10m
```

---

## 4. Health Check — Readiness Gate

The readiness probe blocks Kubernetes from routing traffic to a pod that has not finished warming up (DB pool, caches, third-party handshakes).

```typescript
// src/health.ts
import { Router } from 'express';
import { db } from './db';

export const health = Router();

// Liveness — is the process alive?
health.get('/health/live', (_req, res) => res.status(200).json({ status: 'ok' }));

// Readiness — is the process ready to serve traffic?
health.get('/health/ready', async (_req, res) => {
  try {
    await db.raw('SELECT 1');          // DB connection warm
    res.status(200).json({ status: 'ready' });
  } catch (err) {
    res.status(503).json({ status: 'not ready', reason: String(err) });
  }
});
```

```yaml
# kubernetes/deployment.yaml (probe config)
readinessProbe:
  httpGet:
    path: /health/ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
  failureThreshold: 3    # 15 s of failure before pod is removed from LB
livenessProbe:
  httpGet:
    path: /health/live
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 10
  failureThreshold: 3
```

---

## 5. Automated Rollback on Failure

If the canary error-rate check (step 3) exits non-zero, GitHub Actions fails the job. Argo Rollouts automatically aborts to the previous stable image:

```yaml
      - name: Abort canary on failure
        if: failure()
        run: |
          kubectl argo rollouts abort api --namespace=production
          kubectl argo rollouts undo api --namespace=production
          echo "Rollback triggered. Verifying stable revision..."
          kubectl argo rollouts status api --namespace=production --timeout=5m
```

If you are not using Argo Rollouts, the equivalent for a standard Kubernetes Deployment:

```bash
# Record the stable image SHA before the deploy (done in pipeline setup)
STABLE_IMAGE=$(kubectl get deployment api -n production \
  -o jsonpath='{.spec.template.spec.containers[0].image}')

# On failure:
kubectl set image deployment/api api="$STABLE_IMAGE" --namespace=production
kubectl rollout status deployment/api --namespace=production --timeout=5m
```

After rollback:
1. Verify `/health/ready` returns 200 across all pods.
2. Watch error rate for 15 minutes.
3. Open a post-mortem ticket before the next deploy attempt.

---

## Full Pipeline Dependency Graph

```
quality → build → migrate (staging) → deploy-staging
                                             │
                                    integration-tests
                                             │
                                   deploy-prod-canary
                                    (5 %, 10 min wait)
                                   error-rate check
                                    pass → promote 100%
                                    fail → auto-rollback
```

Each arrow is a `needs:` dependency. No stage is skipped.
