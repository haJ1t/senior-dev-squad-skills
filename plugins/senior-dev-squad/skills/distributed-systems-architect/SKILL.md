---
name: distributed-systems-architect
description: "Distributed systems: microservices, event-driven design, data consistency, fault tolerance, multi-region, observability. Use when designing or reviewing distributed architecture."
version: 1.0.0
platforms: [linux, macos]
---

# Distributed Systems Architect

## Overview

Distributed Systems Architect is the skill of designing high-scale, high-availability, geographically distributed system architectures. While the `architecture-planner` handles foundational full-stack architectures, this skill addresses the unique complexities of distributed environments: partial failures, network unreliability, consistency-availability trade-offs (CAP/PACELC), eventual consistency, distributed transactions, and multi-region operations.

**Core Principle:** IN A DISTRIBUTED SYSTEM, EVERYTHING RUNS SIMULTANEOUSLY AND EVERYTHING BREAKS SIMULTANEOUSLY. THE ARCHITECT DESIGNS BY ACCEPTING THIS REALITY, NOT BY DENYING IT.

Key differences from the `architecture-planner`:
- **Starts with the Fallacies of Distributed Computing** — systematically refutes assumptions that the network is reliable, latency is zero, or bandwidth is infinite.
- **CAP/PACELC Theorem** — treats every storage decision as a deliberate consistency-availability trade-off that must be documented.
- **Partial Failure** — ensures that if a service crashes, the rest of the system continues to function gracefully.
- **Eventual Consistency** — defines clear eventual consistency strategies where instant strong consistency is impossible or costly.
- **Multi-region** — extends beyond a single data center to geographical distribution and disaster recovery.

## Iron Laws (NEVER Violate)

1. **The network is unreliable — every call can fail** — Do not write code without defining a timeout, retry strategy, and circuit breaker for every inter-service call.
2. **Every write operation must be idempotent** — If the same request is received twice, it must produce the same result. This is the only way retries are safe.
3. **Know the CAP/PACELC trade-off and document it** — For every datastore selection: CP or AP? Why? What is the behavior under each failure mode?
4. **Never start with distributed transactions (2PC)** — Attempt Saga, Outbox, and eventual consistency first. Two-Phase Commit (2PC) is a last resort.
5. **Each service owns its own database** — NO direct access to another service's database. Access must occur exclusively through APIs or event streams.
6. **Observability is not retrofitted; it is part of the design** — Distributed tracing, structured logging, and metrics aggregation are designed alongside the architecture.
7. **A single point of failure can crash the entire system** — Every component must have redundancy, a failover strategy, and a recovery plan.

## When To Use

**USE WHEN:**
- The system will be divided into 3+ independent services.
- The system expects 1000+ concurrent users or 10K+ RPS.
- Geographical distribution is required (multi-region, multi-AZ).
- Zero-downtime deployment is a hard requirement.
- Data consistency vs. availability trade-offs are critical (e.g., finance, e-commerce, healthcare).
- Different services require different database technologies (polyglot persistence).
- Parts of the system are developed by separate teams.

**DO NOT USE (use `architecture-planner` instead):**
- A monolith is sufficient and scale is not an issue.
- There are fewer than 3 services.
- The team has fewer than 5 people (microservices coordination overhead > benefit).
- The domain is simple (basic CRUD).
- There is no requirement for zero-downtime or multi-region deployment.

## The Fallacies of Distributed Computing

Every distributed system design begins by systematically refuting these 8 fallacies:

| # | Fallacy | Reality | Architectural Countermeasure |
|---|---------|--------|------------------------------|
| 1 | The network is reliable | Packets get lost, switches fail, cables break | Retry + timeout on EVERY call |
| 2 | Latency is zero | The speed of light imposes physical limits: NY↔London ~70ms min | Async communication, caching, CDN |
| 3 | Bandwidth is infinite | Network congestion and throttling are real | Backpressure, rate limiting, pagination |
| 4 | The network is secure | MITM, DNS spoofing, BGP hijacking are real threats | mTLS, service mesh, zero trust |
| 5 | Topology doesn't change | Services scale up/down, IPs change dynamically | Service discovery, health checking |
| 6 | There is one administrator | Each team has its own deployment and configuration | Federation, API gateway, contract testing |
| 7 | Transport cost is zero | Serialization/deserialization consumes significant CPU | Binary protocols (Protobuf, Avro), schema evolution |
| 8 | The network is homogeneous | Nodes and links have varying speeds and reliabilities | Adaptive timeout, latency-aware routing |

## Pipeline (Architectural Design — 10 Phases)

### Phase 1: Domain Analysis and Service Decomposition

Use Domain-Driven Design (DDD) to divide the system into bounded contexts.

1. **Domain Discovery** — Understand the domain via Event Storming, Domain Storytelling, or Big Picture.
2. **Define Bounded Contexts** — Each context has its own ubiquitous language, model, and database.
3. **Map Context Relationships** — Draw the context map showing relationships: upstream/downstream, shared kernel, customer/supplier, conformist, anti-corruption layer.
4. **Draw Service Boundaries** — Determine service boundaries based on transaction boundaries, deployment independence, and team structure.

```yaml
bounded_contexts:
  - name: "Order Management"
    ubiquitous_language: [order, line_item, fulfillment_status, shipping_address]
    owns_data: [orders, order_items]
    event_storming_commands: [PlaceOrder, CancelOrder, UpdateShippingAddress]
    event_storming_events: [OrderPlaced, OrderCancelled, ShippingAddressUpdated]
    
  - name: "Payment Processing"
    ubiquitous_language: [payment_intent, charge, refund, payment_method]
    owns_data: [payments, payment_methods, refunds]
    relationship_to_order: "customer/supplier (Payment publishes PaymentProcessed event to Order)"
    
  - name: "Inventory"
    ubiquitous_language: [stock_level, reservation, warehouse, sku]
    owns_data: [inventory_items, reservations, warehouses]
    anti_corruption_layer: "Normalizes data coming from legacy ERP"

service_boundaries:
  - service: "order-service"
    contexts: [Order Management]
    reason: "High transaction volume, independent scaling needs"
    
  - service: "payment-service"  
    contexts: [Payment Processing]
    reason: "PCI-DSS compliance isolation, distinct security domain"
    
  - service: "inventory-service"
    contexts: [Inventory]
    reason: "Isolate legacy ERP dependencies"
```

### Phase 2: Communication Architecture

Select the inter-service communication patterns.

**Decision Tree:**
```
Does the caller need the response IMMEDIATELY?
├── YES → Synchronous (Request-Response)
│   ├── Internal service → gRPC (Protobuf + HTTP/2, low latency)
│   ├── External API → REST (OpenAPI, HTTP/1.1, broad ecosystem)
│   └── Frontend → GraphQL Federation (for fetching data from multiple services)
│
└── NO → Asynchronous (Message/Event)
    ├── Guaranteed delivery needed → Message Broker (RabbitMQ, SQS)
    ├── High throughput needed → Event Streaming (Kafka, Pulsar)
    └── Simple notification → Webhook / WebSocket
```

```yaml
communication_matrix:
  frontend-to-backend:
    pattern: "GraphQL Federation"
    gateway: "Apollo Router"
    rationale: "Order page needs to fetch order + payment + inventory data in a single query"

  order-to-payment:
    pattern: "Async Event (OrderPlaced → Payment Service)"
    broker: "Kafka"
    topic: "orders.events"
    schema_registry: true
    exactly_once: true  # Enforced via idempotency key
    rationale: "Waiting synchronously for payments triggers timeouts; return 'Order received, processing payment' to user"

  payment-to-order:
    pattern: "Async Event (PaymentProcessed → Order Service)"
    rationale: "Payment result updates order status asynchronously; order service does not block waiting for payment"

  inventory-check:
    pattern: "Sync gRPC"
    timeout: "500ms"
    retry: "3x exponential backoff"
    circuit_breaker:
      failure_threshold: 5
      cooldown: "30s"
    fallback: "accept_order_defer_inventory_check"
    rationale: "Inventory check must be fast (500ms); if the inventory service fails, defer the check instead of rejecting the order"
```

### Phase 3: Data Consistency Strategy

There are no distributed transactions in a healthy distributed system. Design your consistency model.

```
STRONG CONSISTENCY
├── Within a single service → ACID transaction (sufficient)
├── Across multiple services, same DB → DO NOT DO THIS! Anti-pattern.
└── Across multiple services, different DBs → 2PC (last resort, performance bottleneck)

EVENTUAL CONSISTENCY
├── Saga (Orchestrated) → Orchestrator service manages all steps, triggers compensating transactions
├── Saga (Choreographed) → Services listen to events, execute actions, publish compensating events
├── Outbox Pattern → Atomic write to database AND publish event (via Change Data Capture / CDC)
├── CQRS → Separate read and write models, updated via eventual consistency
└── Event Sourcing → Rebuild state from event log, providing a complete audit trail
```

```yaml
consistency_patterns:
  place_order_saga:
    type: "orchestrated"
    steps:
      - service: "order-service"
        action: "CREATE_ORDER (status=PENDING)"
        compensation: "CANCEL_ORDER"
      - service: "payment-service"
        action: "AUTHORIZE_PAYMENT"
        compensation: "VOID_PAYMENT"
      - service: "inventory-service"
        action: "RESERVE_INVENTORY"
        compensation: "RELEASE_INVENTORY"
      - service: "order-service"
        action: "CONFIRM_ORDER (status=CONFIRMED)"
        compensation: null  # Last step, no compensation
    orchestrator: "order-service"
    timeout_per_step: "30s"
    on_saga_failure: "Execute all compensations in reverse order"

  outbox_pattern:
    service: "order-service"
    implementation: "Debezium CDC"
    flow:
      - "INSERT INTO orders + INSERT INTO outbox (atomic, same transaction)"
      - "Debezium reads outbox → publishes to Kafka"
      - "Guaranteed: every order creation → at least once event publication"
    idempotency:
      key: "order_id + event_type"
      consumer_check: "SELECT 1 FROM processed_events WHERE key = ?"
      deduplication: "At-most-once processing"
```

### Phase 4: Resilience and Fault Tolerance

Every component must be designed to fail gracefully in isolation.

```yaml
resilience_stack:
  service_level:
    timeout: "Mandatory on every external call"
    retry:
      strategy: "exponential_backoff"
      max_attempts: 3
      initial_delay: "100ms"
      max_delay: "10s"
      jitter: true  # Prevents thundering herd
      retry_on: [timeout, 429, 5xx]
      dont_retry_on: [400, 401, 403, 404]  # Deterministic errors
    
    circuit_breaker:
      library: "resilience4j / polly / gobreaker"
      sliding_window: "10s"
      failure_threshold: 5
      cooldown: "30s"
      half_open_probe: true
      probe_count: 3
    
    bulkhead:
      type: "semaphore"
      max_concurrent_calls: 20
      max_queue_wait: "100"
      on_reject: "return 429 + Retry-After header"
    
    rate_limiter:
      algorithm: "token_bucket"
      limit: 100  # requests/second
      burst: 20

  infrastructure_level:
    load_balancer:
      type: "L7 (application)"
      health_check: "/health"
      unhealthy_threshold: 3
      draining_timeout: "30s"
    
    service_mesh:
      tool: "Istio / Linkerd / Consul Connect"
      features: [mTLS, traffic_split, circuit_breaking, retry, timeout]
      
    multi_az:
      min_instances_per_az: 2
      total_azs: 3
      failover: "automatic (load balancer health check)"
    
    multi_region:
      primary: "us-east-1"
      secondary: "eu-west-1"
      replication: "async (event stream)"
      rpo: "5 minutes"
      rto: "15 minutes"
      failover: "DNS (Route53 latency-based + health check)"
```

### Phase 5: Data Architecture

Each service owns its own database. No shared databases.

```yaml
data_architecture:
  order_service_db:
    type: "PostgreSQL (RDBMS)"
    rationale: "ACID transaction support, complex joins, foreign keys"
    partitioning:
      strategy: "range (created_at, monthly)"
      shards: 12
    read_replicas: 2
    connection_pooling: "PgBouncer (transaction mode)"
    
  payment_service_db:
    type: "PostgreSQL"
    rationale: "ACID compliance, PCI-DSS compliant audit logging"
    encryption:
      at_rest: "AWS KMS"
      in_transit: "TLS 1.3"
      column_level: "pgcrypto (card_number, cvv)"
    retention: "7 years (legal requirement)"
    
  inventory_service_db:
    type: "PostgreSQL + Redis"
    rationale: "PostgreSQL for persistent stock, Redis for real-time counters"
    cache_strategy: "write-through (write to DB first, then update cache)"
    cache_invalidation: "event-driven (InventoryUpdated event → Redis delete)"
    
  product_search:
    type: "Elasticsearch"
    rationale: "Full-text search, faceted filtering"
    sync_strategy: "CDC (Kafka Connect → Elasticsearch sink)"
    consistency: "eventual (< 1 second latency)"
```

### Phase 6: Event Architecture

The central event bus is the common language of all services.

```yaml
event_design:
  schema_registry: "Confluent / Apicurio"
  schema_evolution: "FULL (backward + forward compatible)"
  
  topics:
    orders.events:
      schema: "OrderEvent.avsc"
      partitions: 12
      replication_factor: 3
      retention: "7 days"
      key: "order_id"
      
    payments.events:
      schema: "PaymentEvent.avsc"
      partitions: 12
      replication_factor: 3
      retention: "90 days (financial audit)"
      key: "payment_id"
      
    inventory.events:
      schema: "InventoryEvent.avsc"
      partitions: 6
      retention: "3 days"
      key: "sku_id"

  event_schema_example:
    OrderPlaced:
      type: "record"
      fields:
        - name: "event_id"      # UUID v7 (time-sortable)
          type: "string"
        - name: "event_type"    # "OrderPlaced"
          type: "string"
        - name: "timestamp"     # ISO 8601, producer timestamp
          type: "string"
        - name: "source"        # "order-service/v2.3.1"
          type: "string"
        - name: "correlation_id"  # Trace ID (cross-service)
          type: "string"
        - name: "payload":
          type: "record"
          fields:
            - name: "order_id"    # Business key
            - name: "customer_id"
            - name: "items"
            - name: "total_amount"
```

### Phase 7: API Gateway and Service Discovery

```yaml
api_gateway:
  tool: "Kong / Envoy / AWS API Gateway"
  
  routes:
    /api/v1/orders/*: "order-service"
    /api/v1/payments/*: "payment-service (internal only, not exposed)"
    /api/v1/products/*: "product-service"
    /graphql: "Apollo Router (federated)"
  
  cross_cutting:
    authentication: "Gateway-level JWT validation"
    rate_limiting: "Gateway-level (Redis-backed)"
    request_logging: "Gateway-level structured logging"
    cors: "Enforced at gateway"
    request_size_limit: "10MB"

service_discovery:
  tool: "Consul / Kubernetes DNS / Eureka"
  health_check:
    interval: "10s"
    timeout: "2s"
    unhealthy_threshold: 3
    endpoint: "/health (liveness) + /health/ready (readiness)"
  
  load_balancing:
    algorithm: "least_connections"
    sticky_sessions: false  # Stateless preferred
```

### Phase 8: Observability

Three pillars: Metrics, Logging, Tracing.

```yaml
observability:
  distributed_tracing:
    tool: "OpenTelemetry + Jaeger / Honeycomb"
    propagation: "W3C Trace Context (traceparent header)"
    sampling:
      production: "1% (tail sampling: all errors + latency > p95)"
      staging: "100%"
    
  metrics:
    tool: "Prometheus + Grafana"
    golden_signals:
      - latency: "p50, p90, p99 (histogram)"
      - traffic: "requests/sec, events/sec"
      - errors: "error rate (5xx / total)"
      - saturation: "CPU, memory, connection pool, goroutine count"
    slo_dashboard:
      availability: "99.95% (monthly)"
      latency_p95: "< 200ms"
      error_rate: "< 0.1%"
      burn_rate_alerts:
        - "2% error budget consumed in 1h → page on-call"
        - "5% error budget consumed in 6h → ticket"

  logging:
    tool: "Loki / ELK / Datadog"
    format: "structured JSON"
    required_fields:
      - timestamp: "ISO 8601"
      - level: "DEBUG|INFO|WARN|ERROR|FATAL"
      - service: "order-service"
      - trace_id: "W3C trace ID"
      - span_id: "OpenTelemetry span ID"
      - message: "Human readable"
      - context: "Request-specific (user_id, order_id, etc.)"
    pii_redaction: "Automatic (credit card, email, phone → [REDACTED])"
```

### Phase 9: Security Architecture

```yaml
security:
  defense_in_depth:
    layer_1_network: "WAF (AWS WAF / Cloudflare), DDoS protection"
    layer_2_transport: "mTLS everywhere (service mesh), TLS 1.3 minimum"
    layer_3_application: "JWT (RS256), RBAC + ABAC, input validation at every boundary"
    layer_4_data: "Encryption at rest (KMS), column-level encryption (PII), key rotation (90 days)"
    
  zero_trust:
    principle: "Never trust, always verify"
    implementation:
      - "Every service call is authenticated (mTLS + JWT)"
      - "Every service performs its own authorization (no blind trust)"
      - "Least privilege: each service accesses only the data it requires"
    
  secrets_management:
    tool: "HashiCorp Vault / AWS Secrets Manager"
    rotation: "Automatic (every 90 days)"
    audit: "Every secret access is logged"
    
  threat_model:
    methodology: "STRIDE per service boundary"
    critical_assets:
      - "payment-service: PCI-DSS scope"
      - "user-service: PII (GDPR scope)"
```

### Phase 10: Deployment and Operational Architecture

```yaml
deployment:
  strategy: "Blue/Green (critical) + Canary (non-critical)"
  
  ci_cd:
    pipeline:
      - "PR → lint + unit test + security scan"
      - "Merge → integration test + build image + push registry"
      - "Deploy staging → e2e test + chaos test"
      - "Canary production (5% → 25% → 100%)"
      - "Monitor for 15 min → promote or rollback"
    
  rollback:
    automated: true
    trigger: "error rate > 1% OR latency p95 > 2x baseline"
    duration: "< 5 minutes"

  kubernetes_manifests:
    replica_strategy:
      min: 3
      max: 20
      autoscaling: "HPA (CPU > 70% or custom metrics)"
    pod_disruption_budget: "minAvailable: 2"
    affinity: "podAntiAffinity (spread across different AZs)"
    resource_limits:
      cpu: "1-4 cores"
      memory: "512Mi-4Gi"
    
  capacity_planning:
    current_load: "5K RPS peak"
    growth_rate: "20% monthly"
    headroom: "3x (Black Friday / traffic spikes)"
    cost_model:
      compute: "$8K/month (K8s cluster)"
      databases: "$12K/month (RDS + ElastiCache + Elasticsearch)"
      networking: "$3K/month (NAT GW, Load Balancer, data transfer)"
      observability: "$5K/month (Datadog / Grafana Cloud)"
      total: "$28K/month"
```

## Red Flags (STOP and Rethink)

- **Considering a shared database** — You are building a distributed monolith, not microservices. Each service must own its DB.
- **Two-Phase Commit (2PC) is your first choice** — It is a massive performance bottleneck. Attempt Saga patterns instead.
- **No circuit breakers defined** — You are inviting cascading failures where one downed service crashes the entire system.
- **Events lack a schema registry** — You will struggle to parse event schemas 3 months from now. Enforce schema evolution.
- **Logging without Trace IDs** — You cannot trace errors across asynchronous boundaries in a distributed system.
- **"We will add scalability later"** — Scalability does not retroactively fit. Partitioning and sharding must be designed up front.
- **Deploying to a single region** — What happens when that region suffers an outage? Multi-AZ is the minimum; multi-region is preferred.
- **No idempotency keys** — Asynchronous retries will execute duplicate actions. Every state mutation must be idempotent.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The monolith is fine, we will split it later" | Splitting a monolith later is 10x harder than designing modular bounded contexts from day one. |
| "The network is reliable, we are in AWS" | AWS SLAs are typically 99.99%, meaning ~52 minutes of allowed downtime per year. Can your system handle that gracefully? |
| "Two services can share a database, it's the same team" | Teams split and change. Shared databases lead to tight coupling, schema conflicts, and migration logjams. |
| "Event sourcing is too complex, let's just do CRUD" | The audit trail, point-in-time recovery, and simplified debugging of event sourcing will far outweigh its initial complexity. |
| "We have a load balancer, so circuit breakers are optional" | Load balancers drop dead nodes, but if a node is alive and returning slow timeouts, only a circuit breaker prevents systemic exhaustion. |
| "We will add observability once we are in production" | When a production incident occurs, trying to debug without tracing and correlation IDs is practically impossible. |

## Human Partner Signals

**Requires Architectural Decision:**
- Cases where the CAP/PACELC trade-off is business-critical (strong consistency vs. high availability).
- Deciding to deviate from the ideal design due to severe budget constraints.
- Choosing between high multi-region infrastructure costs vs. acceptable downtime risks.

**Requires Domain Knowledge:**
- Bounded context boundaries are fuzzy due to lack of a domain expert.
- Navigating regulatory details (PCI-DSS, HIPAA, GDPR) that exceed technical expertise.
- Business decisions regarding integration protocols with legacy external systems.

## Verification Checklist

**Domain and Service Design:**
- [ ] Ubiquitous language is explicitly defined for all bounded contexts.
- [ ] Service boundaries are optimized around transaction volumes and team capacities.
- [ ] Each service owns its database (absolutely no shared databases).
- [ ] Anti-corruption layers are defined for external/legacy system integrations.

**Communication and Data:**
- [ ] Sync/async communication pattern is documented for every inter-service call.
- [ ] Timeout, retry, and circuit breaker policies are defined for every endpoint.
- [ ] CAP/PACELC trade-offs are documented per datastore.
- [ ] Saga, Outbox, or Event Sourcing consistency strategies are mapped.
- [ ] All state mutations are designed to be idempotent.

**Infrastructure:**
- [ ] Multi-AZ deployment is active (minimum 3 AZs).
- [ ] Multi-region strategy is detailed (active-passive or active-active).
- [ ] Service discovery and health checks are configured.
- [ ] API gateway handles JWT validation, global rate limiting, and structured routing.

**Observability:**
- [ ] Distributed tracing is active across all services.
- [ ] Structured logging is formatted in JSON containing valid trace correlation IDs.
- [ ] Golden signals dashboard is configured in Prometheus/Grafana.
- [ ] SLOs are defined and burn-rate alert rules are deployed.

**Security:**
- [ ] mTLS is enforced for all inter-service communications.
- [ ] Zero trust is implemented: each service validates its own incoming authentication and authorization.
- [ ] Automated secrets rotation is set up.
- [ ] STRIDE threat modeling is completed per service boundary.

**Operations:**
- [ ] CI/CD pipeline supports blue/green and canary deployments.
- [ ] Automated rollback triggers have been tested.
- [ ] Capacity planning and complete cost models are calculated.
- [ ] Chaos testing (e.g., node shutdown, network latency injection) is scheduled.

## Output Schema (MANDATORY)

```markdown
# [Architecture Name]
## 1. Components/Contexts
[Table: Name | Responsibility | Data | Dependencies]
## 2. Decisions (ADR format)
### ADR-001: [Title]
**Context:** [Why] **Options:** [2+ alternatives] **Decision:** [What] **Tradeoffs:** [+gain / -sacrifice]
## 3. Communication Matrix
[Table: From→To | Pattern | Protocol | Timeout | Retry]
## 4. Data & CAP Analysis
[Per store: Type | CP/AP | Partition behavior]
## 5. Deployment Topology
[ASCII diagram]
## Verdict: READY / NEEDS CLARIFICATION
```

## LLM Anti-Patterns

| Anti-Pattern | Why Wrong | Fix |
|-------------|-----------|-----|
| No tradeoffs | Decision without context | Every choice: "X over Y because..." |
| Vague tech ("use Kafka") | No justification | ADR format with 2+ alternatives |
| Missing CAP | Ignores partition reality | Every store: CP or AP? |
| No deployment diagram | Paper architecture | ASCII topology with AZs |
| Single option presented | No real analysis | Always compare 2+ choices |

## Scoring Rubric

| Criterion | 0 | 1 | 2 |
|-----------|---|---|---|
| Component decomposition | None | Listed | Bounded contexts with ownership |
| ADR tradeoffs | None | Some | Every decision: 2+ alternatives |
| CAP awareness | None | Mentioned | Per-store CP/AP + behavior |
| Communication matrix | None | Patterns only | Timeout+retry+circuit breaker |
| Deployment topology | None | "Deploy to cloud" | AZ diagram with counts |
| Risk register | None | 1-2 risks | 5+ with mitigation+owner |

**Pass: 8/12**

## Related Skills

- **architecture-planner** — Foundational full-stack architecture. Runs BEFORE or TOGETHER WITH Distributed Systems Architect.
- **epic-orchestrator** — Orchestration of large-scale distributed projects. Implements the architecture produced by this skill.
- **performance-engineer** — Core Web Vitals and N+1 optimizations. In distributed systems: network latency, serialization cost, connection pooling.
- **security-reviewer** — OWASP Top 10. In distributed systems: mTLS, service mesh security, zero trust.
- **devops-release-engineer** — CI/CD and deployment. In distributed systems: blue/green, canary, multi-region deploy.
- **chaos-engineer** — Chaos engineering. Mandatory for distributed systems: network partition, AZ failure, region failure testing.
- **cloud-security-auditor** — CIS Benchmarks. In distributed systems: IAM policy, security group, VPC audit.
- **observability-pro** — OpenTelemetry, Prometheus, structured logging. The observability backbone of distributed systems.
- **postgres-pro** — PostgreSQL optimization. In distributed systems: partitioning, sharding, read replicas, connection pooling.
- **docker-k8s-pro** — Kubernetes. The deployment platform for distributed systems.
- **terraform-pro** — Infrastructure as Code. Multi-AZ, multi-region environments.
