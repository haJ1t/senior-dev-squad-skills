# Distributed Systems Architect — Reference

Full design pipeline with worked examples, YAML templates, and decision patterns.
All 10 phases are annotated and cross-referenced; use this alongside SKILL.md.

---

## Phase 1: Domain Analysis and Service Decomposition

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

---

## Phase 2: Communication Architecture

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

---

## Phase 3: Data Consistency Strategy

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

---

## Phase 4: Resilience and Fault Tolerance

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

---

## Phase 5: Data Architecture

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

---

## Phase 6: Event Architecture

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

---

## Phase 7: API Gateway and Service Discovery

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

---

## Phase 8: Observability

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

---

## Phase 9: Security Architecture

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

---

## Phase 10: Deployment and Operational Architecture

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

---

## Output Template

Use this structure for deliverables produced by this skill:

```
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
