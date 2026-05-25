# Architecture Planner — Worked Example

Concrete walk-through of the method applied to a **notifications service**. All eight output sections are produced below. Read this before your first real session.

---

## System: Notifications Service

**Context:** An e-commerce platform adds a notifications service to decouple transactional messaging (order confirmations, payment receipts, shipping updates) from the order, payment, and fulfillment services that currently send emails inline via SMTP.

---

## 1. Service Decomposition

| Service | Responsibility | Owns Data | Depends On | Scale Profile |
|---------|---------------|-----------|------------|---------------|
| notification-service | Template rendering, delivery dispatch, status tracking | notifications, delivery_attempts, templates | order-svc (events), payment-svc (events), fulfillment-svc (events) | 200K sends/day, spiky (order bursts) |
| template-service | Manage notification templates (email/SMS/push), versioning, A/B variants | templates, template_versions | — | Low write, high read |
| preference-service | User channel preferences, opt-out/unsubscribe, frequency caps | user_preferences, suppression_lists | — | 50K reads/min at peak |
| delivery-adapter-service | Vendor fan-out (SendGrid, Twilio, FCM), retry, bounce/complaint webhooks | delivery_logs, vendor_events | SendGrid, Twilio, FCM (external) | Matches notification-service volume + bounce traffic |

**Boundary rule applied:** `notification-service` does not write to `templates` (owned by template-service); it reads templates at render time. `preference-service` is the single writer for suppression lists — other services call it; none bypass it.

---

## 2. Architecture Decision Records

### ADR-001: Kafka over direct HTTP for inbound order/payment/fulfillment events

**Context:**
Order, payment, and fulfillment services currently send notification triggers via synchronous HTTP calls to the mailer. This creates tight coupling: if the mailer is slow or down, the caller blocks or fails. At 200K sends/day with spiky order traffic, the inline send path adds 80–200ms to checkout response time.

**Options Considered:**

| Option | Latency to caller | Delivery guarantee | Coupling | Ops overhead |
|--------|-------------------|-------------------|----------|-------------|
| Sync HTTP (current) | +80–200ms (inline) | At-most-once (caller retries are manual) | Tight | None |
| RabbitMQ queue | Near-zero | At-least-once (ack) | Loose | Medium |
| Kafka topic | Near-zero | At-least-once + replay | Loose | Higher (cluster, Schema Registry) |

**Decision:** Kafka.

**Tradeoffs:**
- Gain: producers are fully decoupled; notification-service can fall behind and catch up without data loss; replay enables re-sending if a vendor is down for hours; event log is the audit trail for "did we attempt to notify user X?".
- Sacrifice: Kafka cluster adds operational overhead (broker management, consumer group offsets, Schema Registry for schema evolution). Minimum latency floor ~5ms vs ~1ms for RabbitMQ. Requires Avro schema discipline from day one.

**Consequences:**
- order-svc, payment-svc, fulfillment-svc produce to topic `notification.triggers.v1` (Avro schema, backward-compatible evolution).
- notification-service is the sole consumer group (`notification-consumer`), 6 partitions (expected peak: ~2K events/min; 6 partitions gives headroom to 12K/min with consumer scaling).
- Schema Registry required in staging and production before launch.
- Dead-letter topic `notification.triggers.v1.dlq` for events that fail processing after 3 attempts; alerting on DLQ depth > 0.

---

### ADR-002: Transactional Outbox for delivery dispatch to vendor adapters

**Context:**
notification-service consumes a Kafka event, renders the template, persists a `notifications` row, then must dispatch to delivery-adapter-service. The dispatch must not be lost if notification-service crashes after writing to its DB but before the HTTP call to the adapter. Direct HTTP after `INSERT` creates a window where the notification row exists but the vendor never receives the send request.

**Options Considered:**

| Option | Atomicity | Complexity | Latency |
|--------|-----------|-----------|---------|
| HTTP dispatch inside DB transaction | None (HTTP is not transactional) | Low | Low |
| Two-phase commit (XA) | Full | Very high (requires XA-capable driver + adapter support) | +30–100ms |
| Saga (choreography via events) | Eventual | Medium | Medium |
| Transactional Outbox | Effective atomicity (same DB, relay picks up) | Medium | Low (+relay polling ~100ms) |

**Decision:** Transactional Outbox.

**Tradeoffs:**
- Gain: `notification` row and `outbox_events` row are written in one DB transaction — if the process crashes, the relay replays the outbox event on restart; no send is silently dropped. At-least-once delivery to the adapter with idempotency key on every dispatch prevents double-send.
- Sacrifice: relay process is an additional component to operate (can be co-located in the same service binary). Polling interval adds ~100ms latency vs inline dispatch. Adapter must be idempotent on `notification_id` (documented in the communication matrix as a contract).

**Consequences:**
- `outbox_events` table in notification-service's Postgres: `(id, notification_id, payload, created_at, dispatched_at, attempts)`.
- Relay polls every 100ms; marks `dispatched_at` on success; retries with exponential backoff (max 3 attempts before DLQ insert).
- delivery-adapter-service uses `notification_id` as idempotency key on all vendor API calls.

---

## 3. Communication Matrix (abbreviated)

| From | To | Pattern | Protocol | Timeout | Retry | Circuit Breaker |
|------|----|---------|----------|---------|-------|-----------------|
| order-svc | notification-service | Async event | Kafka topic | n/a | Kafka consumer retry (3×, exponential) | n/a (async) |
| notification-service | template-service | Sync read | gRPC | 200ms | 2× linear | Yes (fail-open: cached template version) |
| notification-service | preference-service | Sync read | gRPC | 150ms | 2× linear | Yes (fail-open: send anyway, log suppression miss) |
| notification-service | delivery-adapter-service | Async (outbox relay) | HTTP/2 | 2s | 3× exponential | Yes (fail to DLQ) |
| delivery-adapter-service | SendGrid / Twilio / FCM | Sync | HTTPS | 5s | 3× exponential | Yes (vendor-specific breaker) |

**Fail-open rationale for preference-service:** suppression misses are auditable post-hoc and recoverable (re-suppress + apology flow); blocking the entire send pipeline on a preference lookup outage is worse for users than an occasional non-suppressed send.

---

## 4. Data Consistency Strategy

**Cross-service write: user unsubscribes → preference-service → must suppress in-flight notifications**

Strategy: **Eventual consistency via event**.

1. User calls `POST /preferences/unsubscribe` on preference-service.
2. preference-service writes suppression row + publishes `user.preference.updated` Kafka event (transactional outbox on its own DB).
3. notification-service consumes event, updates local `suppression_cache` table (read-through cache for the 150ms preference lookup).
4. In-flight notifications that already passed preference check continue to send (acceptable: user unsubscribed while notification was being processed).
5. SLA: suppression propagates within 30 seconds (Kafka lag bound + cache TTL).

No compensation path needed: unsubscribe is additive-only (a new suppression row). The only "wrong" state is a send that escaped the window; this is disclosed in the privacy policy and standard for transactional email systems.

---

## 5. CAP Tradeoffs

| Data Store | Type | CP/AP | Partition Behavior | Justification |
|-----------|------|-------|-------------------|---------------|
| notifications (PostgreSQL primary) | RDBMS | CP | Refuses writes; relay queues in outbox | Delivery records must be consistent — duplicate sends are a user-trust issue |
| outbox_events (same PostgreSQL) | RDBMS | CP | Same as above | Outbox correctness requires same DB as notifications row |
| suppression_cache (PostgreSQL read replica) | Read replica | AP | May serve stale data (up to 30s replication lag) | Stale suppression → occasional extra send; acceptable vs blocking sends on replica lag |
| template_cache (Redis, TTL 5min) | Cache | AP | Returns cached template; notification-service falls back to gRPC call to template-service on miss | Menu-style data; 5-minute stale acceptable; degraded path is slower, not wrong |
| vendor delivery logs (PostgreSQL in delivery-adapter-service) | RDBMS | CP | Refuses writes; vendor calls still proceed (fire-and-forget log failure is acceptable) | Logs are observability; delivery is more important than logging |

---

## 6. Fault Tolerance (top risks)

| Failure Mode | Probability | Impact | Mitigation | Fallback |
|-------------|-------------|--------|-----------|---------|
| SendGrid outage | Medium | High | Vendor circuit breaker; retry queue in delivery-adapter | Route to secondary vendor (Postmark) for transactional email |
| preference-service down | Low | Medium | Circuit breaker on gRPC call; fail-open (send anyway) | Log suppression miss; re-suppress post-recovery |
| Kafka consumer lag spike | Medium | Medium | HPA on notification-service consumers (CPU + lag metric) | DLQ prevents data loss; user sees delayed notification |
| notification-service crash mid-outbox | Low | Low | Relay replays unprocessed outbox rows on restart | Idempotency key prevents double-send |
| Template-service down | Low | High | Redis cache (5-min TTL) absorbs reads; gRPC breaker | Cached template served; stale template is better than no send for transactional types |

---

## 7. Deployment Topology

```
                          [CloudFront CDN — static assets only]
                                        |
                          [ALB — api.example.com — us-east-1]
                           /                          \
              [preference-service]          [template-service]
              (2 replicas, az-1a/1b)        (2 replicas, az-1a/1b)
                    |                              |
              [RDS preference-db              [RDS template-db
               Primary az-1a                  Primary az-1a
               Standby az-1b]                 Standby az-1b]

[MSK Kafka — 3 brokers, az-1a/1b/1c, topic: notification.triggers.v1, 6 partitions]
                    |
       [notification-service consumers]
       (3 replicas, HPA 2–8, az-1a/1b/1c)
                    |
       [RDS notification-db              [Redis template-cache
        Primary az-1a                    Cluster mode, 2 shards
        Standby az-1b                    az-1a/1b]
        Read Replica az-1c]
                    |
       [outbox relay — co-located in notification-service pod]
                    |
       [delivery-adapter-service]
       (3 replicas, HPA 2–10, az-1a/1b/1c)
       /             |             \
[SendGrid]      [Twilio]         [FCM]
(primary)    (SMS channel)   (push channel)
[Postmark]   (circuit-break
(failover)    + secondary)

DR: eu-west-1 active-passive, async Kafka MirrorMaker 2, RDS async replication
    RPO: 5 min  RTO: 20 min
```

---

## 8. Risk Register

| Risk | Likelihood | Impact | Mitigation | Owner | Review Date |
|------|-----------|--------|-----------|-------|-------------|
| Kafka Schema Registry migration breaks consumers | Medium | High | Avro backward-compat enforced in CI; schema review on every producer change | Platform team | Before launch |
| Vendor spend spike (SendGrid volume) | Low | Medium | Daily spend alert at 80% of monthly cap; auto-pause non-critical notification types | Eng + Finance | Monthly |
| Suppression propagation lag causes GDPR breach | Low | Critical | Propagation SLA 30s documented; unsubscribe confirmation email sent immediately by preference-service independent of notification pipeline | Legal + Eng | Quarterly |
| Outbox relay falls behind under peak load | Medium | Medium | Relay throughput tested at 3× peak in load test; alert on outbox_events age > 5min | Eng | Before launch |
| delivery-adapter-service vendor key rotation | Low | High | Secrets rotated via Vault; zero-downtime rotation runbook documented and tested | Sec + Eng | Bi-annual |

---

## Architecture Verdict

- Decisions made: 2 (ADR-001, ADR-002) + 3 implicit (CP/AP per store, fail-open preference, eventual suppression)
- Tradeoffs documented: every ADR has gain/sacrifice table
- Known risks: 5 (1 Critical, 2 High, 2 Medium)
- Critical unknowns: Schema Registry operational runbook not yet written; Postmark failover SLA not confirmed with vendor
- Overall: **NEEDS CLARIFICATION** — resolve Schema Registry runbook + Postmark SLA before READY FOR IMPLEMENTATION

---

*This example is intentionally complete. Real sessions start from a spec (see `spec-first-development`); the architecture document is the output of Phase 1–7 applied to that spec.*
