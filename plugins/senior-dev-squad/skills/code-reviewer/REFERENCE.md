# Code Reviewer — Reference Checklists

## API Design Review Checklist

### Iron Laws
1. **Consistency over cleverness** — Every endpoint must follow the same conventions. One clever exception breaks the mental model for all consumers.
2. **Backward compatibility** — Never break existing consumers. Additive changes only. Breaking changes require a new major version.
3. **Error messages are API** — Error responses must be actionable. "400 Bad Request" without details is a broken API.
4. **Pagination from day one** — Every list endpoint must support pagination. "We'll add it later" = data migration nightmare.

### Red Flags (STOP immediately)
- **Breaking change in minor version** — Field removed, type changed, or endpoint deprecated without major version bump
- **N+1 by design** — API structure forces consumers to make N+1 requests → add expansion/includes or GraphQL
- **Auth in URL** — API keys or tokens in query parameters → move to headers; URLs are logged everywhere
- **Inconsistent error shape** — Different endpoints return different error formats → consumers can't write generic error handlers

### Review Pipeline
1. **Discover** — inventory existing endpoints, document current state, identify consumers
2. **Audit** — review naming, resource modeling, HTTP methods, status codes, error format, pagination
3. **Score** — evaluate against REST/GraphQL/gRPC maturity model with concrete scores
4. **Report** — generate prioritized list: critical (breaking), major (DX friction), minor (style)
5. **Standardize** — propose conventions and design guidelines based on audit findings
6. **Validate** — test proposed design against real consumer use cases before implementation

### Verification Checklist
- [ ] All endpoints follow consistent naming convention
- [ ] Error responses have consistent shape with actionable messages
- [ ] Pagination supported on all list endpoints
- [ ] Backward compatibility verified — no field removals or type changes in current version
- [ ] Authentication tokens never appear in URLs or query parameters
- [ ] API documentation matches implementation (not outdated)
- [ ] Rate limiting implemented with clear headers (X-RateLimit-*)

### Human Escalation Triggers
- **Versioning strategy** — URL vs header versioning is an architectural commitment
- **Breaking change approval** — unavoidable breaking change requires a stakeholder communication plan
- **Rate limit policy** — setting rate limits impacts business model (free vs paid tiers)
- **API deprecation** — sunsetting a version with active consumers requires a migration support plan

---

## Document / Spec Quality Checklists

**Core principle:** EVERY DOCUMENT IS A CONTRACT. NEVER HAND OFF A DOCUMENT THAT HASN'T PASSED ITS QUALITY CHECKLIST.

### After SPECIFICATION.md
- [ ] Every user story has at least one acceptance criterion
- [ ] Every criterion is in Given/When/Then format
- [ ] All four states documented (loading, empty, error, success)
- [ ] Edge cases documented (empty, error, boundary, concurrent)
- [ ] Non-goals explicitly listed
- [ ] Data model changes identified
- [ ] Security implications assessed

### After Architecture Doc
- [ ] Every bounded context has clear responsibility
- [ ] API contract documented before implementation
- [ ] Database schema has additive migration plan
- [ ] Auth model covers authN + authZ
- [ ] Deployment model covers dev/staging/prod
- [ ] Risk register has mitigations for High/Critical
- [ ] Every decision has documented tradeoffs

### After TASKS.md
- [ ] Every task completable in one session
- [ ] Tasks ordered by strict dependency
- [ ] Each task specifies exact files (Create/Modify/Test)
- [ ] No "implement all" or similar vagueness
- [ ] Phases have clear milestones
- [ ] Test step exists for every implementation task

### After PROMPT.md
- [ ] Agent can execute without asking questions
- [ ] All dependencies have specific versions
- [ ] All file paths are exact
- [ ] All code patterns are complete (not placeholders)
- [ ] Verification method after every step
- [ ] No "TBD" or "TODO" remain

### Document Review Self-Check (Before Marking Complete)
- [ ] Selected the correct checklist for the document type
- [ ] Every checklist item verified against the actual text, not assumed
- [ ] Each failed item recorded with the specific gap (section + what is missing)
- [ ] Verdict is PASS only if zero items failed (partial compliance = fail)
- [ ] Gaps handed back to the generating skill before any downstream handoff
