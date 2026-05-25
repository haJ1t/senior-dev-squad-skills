---
name: contract-testing
description: "Pact, consumer-driven contracts, API contract testing, integration breakage prevention. Use when setting up or running contract tests between services."
version: 1.0.0
platforms: [linux, macos]
---

# Contract Testing

## What It Does
Implements consumer-driven contract testing to prevent integration breakage between services. Each API consumer defines its expectations (contract) — specific requests and expected responses. The provider verifies it satisfies all consumer contracts. Contracts are versioned and validated in CI/CD, catching breaking API changes before deployment. Uses Pact framework for HTTP and message-based contracts.

## Iron Laws (NEVER violate)
1. **Consumer defines the contract** — The service that depends on the API specifies what it needs. Provider-centric testing misses what consumers actually use.
2. **Contract ≠ functional test** — Contracts verify API shape (endpoint, method, headers, response schema), not business logic. Functional tests verify behavior.
3. **Provider must verify all consumer contracts** — A provider satisfied N-1 consumers is still broken. All contracts must pass.
4. **Breaking contract = breaking change** — Changing a field that any consumer contract depends on IS a breaking change, regardless of versioning strategy.

## Red Flags (STOP immediately)
- **Contract verification failure** — Provider no longer satisfies a consumer's contract → breaking change detected
- **Stale contract** — Consumer contract hasn't been verified in 30+ days → consumer may be abandoned
- **Over-specified contract** — Consumer specifies fields it doesn't use → provider unnecessarily constrained
- **Missing contract** — Consumer integration exists but no contract defined → invisible dependency

## Common Rationalizations (self-deception)
- "We use the same monorepo, we don't need contract tests" → Monorepo doesn't prevent breaking changes. Contracts catch what code review misses.
- "End-to-end tests cover integration" → E2E tests are slow, flaky, and don't tell you WHO broke the contract. Contract tests are fast and precise.
- "Our API is versioned, breaking changes are fine" → Versioning doesn't help if you don't know you're making a breaking change.

## When To Use
- Microservices architecture with multiple service-to-service API consumers
- Public API with external consumers who can't coordinate releases
- Monorepo where teams independently deploy services
- Event-driven systems with message schemas (Kafka, RabbitMQ)
- Mobile app + backend API where app updates lag behind server updates

## Human Partner Signals (escalate to human)
- **Breaking change impact** — Proposed change breaks 3+ consumer contracts → stakeholder communication needed
- **Consumer deprecation** — Consumer contract appears abandoned → decision to remove or contact owner
- **Contract negotiation** — Consumer needs new field; provider team disagrees on implementation → cross-team alignment
- **Pact broker access** — External consumer needs contract broker access → security and access control review

## Pipeline
1. Consumer: define expected interactions — "Given X state, when I GET /users/1, I expect {id, name, email}"
2. Consumer: generate contract file (Pact) and publish to Pact Broker
3. Provider: fetch all consumer contracts from broker
4. Provider: replay each contract against provider — verify responses match expectations
5. CI: contract verification runs on every provider change; fails if any contract is broken
6. Evolve: consumers update contracts when adding new expectations; provider teams review
7. Deprecate: remove contracts for deprecated API versions; archive in broker

## Verification Checklist
- [ ] Every API consumer has at least one contract defined
- [ ] Provider CI verifies all consumer contracts on every change
- [ ] Contract verification includes HTTP status, headers, and response body shape
- [ ] Breaking contract detection alerts the provider team before merge
- [ ] Pact Broker accessible to all consumer and provider teams
- [ ] Contract compatibility verified before provider deployment
- [ ] Stale contracts flagged for review (no verification in 30 days)

## Related Skills
- `api-design-reviewer` — Contract testing validates API design decisions
- `spec-first-development` — API specs become the basis for consumer contracts
- `test-engineer` — Contract tests are part of the integration testing layer
- `backend-senior-engineer` — Provider implementation must satisfy consumer contracts
