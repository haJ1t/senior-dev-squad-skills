---
name: api-design-reviewer
description: "REST, GraphQL, gRPC API review, naming, versioning, error handling, DX optimization. Use when reviewing or critiquing an API design."
version: 1.0.0
platforms: [linux, macos]
---

# API Design Reviewer

## What It Does
Reviews API designs for consistency, developer experience, and adherence to best practices across REST, GraphQL, and gRPC. Evaluates naming conventions, resource modeling, error handling patterns, versioning strategy, pagination, authentication, rate limiting, and documentation quality. Flags anti-patterns that cause downstream developer friction.

## Iron Laws (NEVER violate)
1. **Consistency over cleverness** — Every endpoint must follow the same conventions. One clever exception breaks the mental model for all consumers.
2. **Backward compatibility** — Never break existing consumers. Additive changes only. Breaking changes require a new major version.
3. **Error messages are API** — Error responses must be actionable. "400 Bad Request" without details is a broken API.
4. **Pagination from day one** — Every list endpoint must support pagination. "We'll add it later" = data migration nightmare.

## Red Flags (STOP immediately)
- **Breaking change in minor version** — Field removed, type changed, or endpoint deprecated without major version bump
- **N+1 by design** — API structure forces consumers to make N+1 requests → add expansion/includes or GraphQL
- **Auth in URL** — API keys or tokens in query parameters → move to headers; URLs are logged everywhere
- **Inconsistent error shape** — Different endpoints return different error formats → consumers can't write generic error handlers

## Common Rationalizations (self-deception)
- "We'll document it later" → Undocumented APIs are unusable. Documentation is part of the API contract.
- "Just return the database model" → Internal models leak implementation details. API models should be stable contracts.
- "REST is always the answer" → GraphQL for complex nested data, gRPC for service-to-service. Choose the right paradigm.

## When To Use
- Designing a new API or adding endpoints to an existing one
- Reviewing an API before public launch
- Migrating between API paradigms (REST → GraphQL, REST → gRPC)
- Auditing API consistency and developer experience
- Establishing API design standards for a team

## Human Partner Signals (escalate to human)
- **Versioning strategy** — Decision between URL versioning, header versioning, or no versioning → architectural commitment
- **Breaking change approval** — Unavoidable breaking change requires stakeholder communication plan
- **Rate limit policy** — Setting rate limits impacts business model (free vs paid tiers) → product decision
- **API deprecation** — Sunsetting an API version with active consumers → migration support plan needed

## Pipeline
1. Discover: inventory existing endpoints, document current state, identify consumers
2. Audit: review naming, resource modeling, HTTP methods, status codes, error format, pagination
3. Score: evaluate against REST/GraphQL/gRPC maturity model with concrete scores
4. Report: generate prioritized list of issues — critical (breaking), major (DX friction), minor (style)
5. Standardize: propose conventions and design guidelines based on audit findings
6. Validate: test proposed design against real consumer use cases before implementation

## Verification Checklist
- [ ] All endpoints follow consistent naming convention (checked programmatically)
- [ ] Error responses have consistent shape with actionable messages
- [ ] Pagination supported on all list endpoints
- [ ] Backward compatibility verified — no field removals or type changes in current version
- [ ] Authentication tokens never appear in URLs or query parameters
- [ ] API documentation matches implementation (not outdated)
- [ ] Rate limiting implemented with clear headers (X-RateLimit-*)

## Related Skills
- `backend-senior-engineer` — API implementation follows the design reviewed here
- `spec-first-development` — API specs written before implementation
- `contract-testing` — API contracts validated against consumer expectations
- `documentation-generator` — Auto-generate API reference docs from design
