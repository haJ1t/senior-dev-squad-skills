# Backend Senior Engineer — Reference

Detailed output format, per-check code samples, worked examples, and model calibration. Linked from [SKILL.md](SKILL.md).

---

## MANDATORY Output Format

Every endpoint implementation MUST include:

```markdown
## Endpoint: [METHOD] [PATH]

### Request Schema
```json
{
  "field": "type (required/optional, constraints)",
  "idempotency_key": "uuid (required for POST/PUT/PATCH)"
}
```

### Success Response
```json
{
  "data": {},
  "meta": {"requestId": "uuid"}
}
```

### Error Responses
| Status | Code | When | Example |
|--------|------|------|---------|
| 400 | VALIDATION_ERROR | Invalid input | `{"error":{"code":"VALIDATION_ERROR","message":"...","details":[...],"requestId":"..."}}` |
| 401 | UNAUTHORIZED | Missing/invalid auth | |
| 403 | FORBIDDEN | Valid auth, insufficient permissions | |
| 404 | NOT_FOUND | Resource doesn't exist | |
| 409 | CONFLICT | Duplicate, stale version | |
| 429 | RATE_LIMITED | Too many requests | Include `Retry-After` header |

### Implementation
```[language]
// Complete, production-grade code with:
// - Input validation (Zod/Pydantic)
// - Auth check
// - Transaction (if multi-step)
// - Structured logging
// - Rate limiting
// - Idempotency key check
```

### Tests
```[language]
// At minimum:
// - Happy path
// - Invalid input (each field)
// - Missing auth
// - Rate limit exceeded
// - Idempotency: same key twice = same result
```
```

---

## Check 1: Input Validation (ALWAYS)

```typescript
// DO: Validate at API boundary, before any business logic
const schema = z.object({
  name: z.string().min(1).max(100).trim(),
  description: z.string().max(500).optional().default(''),
  idempotency_key: z.string().uuid(),
})
const parsed = schema.parse(req.body)

// DON'T: Pass raw input to database
db.projects.create(req.body)  // Mass assignment!
```

## Check 2: Authentication + Authorization

Three-layer check on EVERY protected endpoint:
1. **AuthN:** Is this a valid user? → 401 if not
2. **AuthZ:** Does this user have permission? → 403 if not
3. **Rate limit:** Is this user within quota? → 429 if not

## Check 3: Transaction Safety

Every multi-step operation in a transaction:
```typescript
await db.$transaction(async (tx) => {
  const order = await tx.order.create({ data: orderData })
  await tx.inventory.reserve({ orderId: order.id, items })
  await tx.auditLog.create({ action: 'ORDER_CREATED', orderId: order.id })
})
// If ANY step fails, ALL steps roll back
```

## Check 4: Structured Logging

```json
{"level":"info","requestId":"req_abc","method":"POST","path":"/api/v1/orders","userId":"user_456","statusCode":201,"duration":42,"error":null}
```
**NEVER log:** passwords, tokens, secrets, full request bodies with PII.

## Check 5: Consistent Error Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Project name is required",
    "details": [{"field": "name", "message": "String must contain at least 1 character"}],
    "requestId": "req_abc123"
  }
}
```

---

## Few-Shot Examples (MANDATORY Reference)

### BAD Output

```python
@app.post("/api/v1/orders")
def create_order(data):
    order = db.orders.create(data)
    payment.charge(order.total)
    return {"order_id": order.id}
```
**Why bad:** No input validation, no transactions, no error handling, no rate limiting, no idempotency, no logging.

### GOOD Output

```python
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
import structlog

router = APIRouter()
logger = structlog.get_logger()

class OrderItem(BaseModel):
    product_id: UUID
    quantity: int = Field(gt=0, le=100)

class CreateOrderRequest(BaseModel):
    user_id: UUID
    items: list[OrderItem] = Field(min_length=1, max_length=50)
    shipping_address: str = Field(min_length=10, max_length=500)
    payment_method_id: UUID
    idempotency_key: UUID

@router.post("/api/v1/orders", status_code=201)
async def create_order(
    req: CreateOrderRequest,
    request: Request,
    current_user = Depends(get_current_user),
):
    request_id = str(uuid4())
    logger.info("order_create_started", request_id=request_id, user_id=str(req.user_id))
    
    # Check idempotency
    existing = await db.orders.find_first(where={"idempotency_key": str(req.idempotency_key)})
    if existing:
        logger.info("order_idempotent_replay", request_id=request_id, order_id=str(existing.id))
        return {"order_id": str(existing.id), "status": existing.status, "total": str(existing.total)}
    
    # Validate + create in transaction
    try:
        async with db.transaction():
            # Validate products exist and check inventory
            products = await db.product.find_many(where={"id": {"in": [str(i.product_id) for i in req.items]}})
            if len(products) != len(req.items):
                raise HTTPException(400, detail={"code": "INVALID_PRODUCT", "message": "One or more products not found"})
            
            # Calculate total
            total = sum(p.price * i.quantity for p, i in zip(products, req.items))
            
            # Create order
            order = await db.orders.create(data={
                "id": str(uuid4()), "user_id": str(req.user_id),
                "status": "CONFIRMED", "total": str(total),
                "idempotency_key": str(req.idempotency_key),
            })
            
            # Reserve inventory (in same transaction)
            for item in req.items:
                await db.inventory.update(
                    where={"product_id": str(item.product_id)},
                    data={"reserved": {"increment": item.quantity}},
                )
            
            logger.info("order_created", request_id=request_id, order_id=order.id, total=str(total))
            return {"order_id": order.id, "status": "CONFIRMED", "total": str(total)}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("order_create_failed", request_id=request_id, error=str(e))
        raise HTTPException(500, detail={"code": "INTERNAL_ERROR", "message": "Order creation failed", "requestId": request_id})
```

---

## Model-Specific Calibration

| Model | Tendency | Calibration |
|-------|---------|-------------|
| **Claude Sonnet 4** | Produces the cleanest code, handles transactions and error handling naturally, but tends to forget rate limiting | "Add rate limiting BEFORE the business logic — it's the first check" |
| **GPT-4o** | Fast, performs great Pydantic validation, but tends to skip the idempotency check | "Check idempotency key FIRST, before any business logic — return cached result if exists" |
| **Gemini 2.5 Pro** | Concise and clean, but weak on transaction details | "Wrap ALL multi-step operations in a transaction — show explicit rollback behavior" |
| **DeepSeek V3** | Highly cost-effective, writes structured logs, but sometimes produces a malformed error format | "Use EXACT error format: {error: {code, message, details, requestId}} — no variations" |

---

## Worked Example

**Endpoint:** `POST /orders` (TypeScript · Express · Zod · Prisma)

Walk through every Iron Law decision in order. Each block is preceded by a
narration note explaining *why* that choice was made here.

### Step 1 — Input validation at the boundary

**Decision:** Zod parses and coerces the raw body before any other code runs.
If the schema rejects the input, we short-circuit immediately with a 400 and
never touch the database. `idempotency_key` is required (UUID) on every
mutating request — the schema enforces it, not a downstream check.

```typescript
import { z } from 'zod'

const OrderItemSchema = z.object({
  product_id: z.string().uuid(),
  quantity: z.number().int().min(1).max(100),
})

const CreateOrderSchema = z.object({
  idempotency_key: z.string().uuid(),           // Iron Law 6: required on every POST
  items: z.array(OrderItemSchema).min(1).max(50),
  shipping_address: z.string().min(10).max(500).trim(),
  payment_method_id: z.string().uuid(),
})

type CreateOrderInput = z.infer<typeof CreateOrderSchema>
```

### Step 2 — AuthN + AuthZ + rate limit (before business logic)

**Decision:** Auth runs after schema validation but before any DB read. Rate
limiting is the third sub-check — never deferred to "when we see abuse".
The user can only create orders for themselves; the `user_id` comes from the
verified JWT, not the request body (prevents mass-assignment of another user's
orders).

```typescript
router.post('/api/v1/orders', rateLimiter({ max: 20, window: '1m' }), async (req, res) => {
  // AuthN — 401 if token is missing or invalid
  const currentUser = await verifyJwt(req.headers.authorization)
  if (!currentUser) return res.status(401).json(errorBody('UNAUTHORIZED', 'Invalid token', req.id))

  // AuthZ — 403 if the user's role cannot place orders
  if (!currentUser.permissions.includes('orders:create'))
    return res.status(403).json(errorBody('FORBIDDEN', 'Insufficient permissions', req.id))

  // Input validation — 400 on schema failure
  const parsed = CreateOrderSchema.safeParse(req.body)
  if (!parsed.success)
    return res.status(400).json(errorBody('VALIDATION_ERROR', 'Invalid input', req.id, parsed.error.issues))

  const input: CreateOrderInput = parsed.data
```

### Step 3 — Idempotency key check

**Decision:** Query the idempotency store *before* any write. If the key was
already used, return the cached response immediately — the operation is
complete from the caller's perspective. This makes retries safe at the network
layer without duplicating records.

```typescript
  const cached = await db.idempotencyRecord.findUnique({
    where: { key: input.idempotency_key },
  })
  if (cached) {
    logger.info({ requestId: req.id, event: 'idempotent_replay', orderId: cached.response.orderId })
    return res.status(cached.statusCode).json(cached.response)
  }
```

### Step 4 — DB transaction boundary

**Decision:** Order creation, inventory reservation, and audit-log write are
one logical operation. All three succeed together or all three roll back. The
audit-log write is *inside* the transaction so it never records an event for
an order that was rolled back.

```typescript
  try {
    const result = await db.$transaction(async (tx) => {
      // Validate products exist — one query with IN clause (avoids N+1)
      const products = await tx.product.findMany({
        where: { id: { in: input.items.map((i) => i.product_id) }, active: true },
      })
      if (products.length !== input.items.length)
        throw { code: 'INVALID_PRODUCT', status: 400, message: 'One or more products not found or inactive' }

      const total = input.items.reduce((sum, item) => {
        const product = products.find((p) => p.id === item.product_id)!
        return sum + product.price * item.quantity
      }, 0)

      const order = await tx.order.create({
        data: {
          userId: currentUser.id,
          status: 'CONFIRMED',
          total,
          idempotencyKey: input.idempotency_key,
          items: { create: input.items.map((i) => ({ productId: i.product_id, quantity: i.quantity })) },
        },
      })

      // Reserve inventory — single batched update per item
      await Promise.all(
        input.items.map((item) =>
          tx.inventory.update({
            where: { productId: item.product_id },
            data: { reserved: { increment: item.quantity } },
          })
        )
      )

      // Audit log inside the transaction — rolls back if order creation fails
      await tx.auditLog.create({
        data: { userId: currentUser.id, action: 'ORDER_CREATED', resourceId: order.id },
      })

      return { orderId: order.id, status: order.status, total }
    })
```

### Step 5 — Structured log on success + idempotency record

**Decision:** Log at `info` level with the key fields from Iron Law 4. Store
the idempotency record *after* the transaction commits so a replay always
returns the real result, not a partial one.

```typescript
    logger.info({
      requestId: req.id, event: 'order_created',
      userId: currentUser.id, orderId: result.orderId, total: result.total,
    })

    const responseBody = { data: result, meta: { requestId: req.id } }
    await db.idempotencyRecord.create({
      data: { key: input.idempotency_key, statusCode: 201, response: responseBody },
    })

    return res.status(201).json(responseBody)
```

### Step 6 — Typed error responses (no swallowing)

**Decision:** Domain errors thrown inside the transaction carry a `code` and
`status`. Unknown errors get a generic 500 but are still logged with the full
stack trace so on-call has something to work with. No exception is silently
dropped.

```typescript
  } catch (err: any) {
    if (err.code && err.status) {
      logger.warn({ requestId: req.id, event: 'order_rejected', code: err.code, message: err.message })
      return res.status(err.status).json(errorBody(err.code, err.message, req.id))
    }
    logger.error({ requestId: req.id, event: 'order_create_failed', error: String(err), stack: err?.stack })
    return res.status(500).json(errorBody('INTERNAL_ERROR', 'Order creation failed', req.id))
  }
})
```

### Helper: `errorBody`

```typescript
function errorBody(code: string, message: string, requestId: string, details?: unknown) {
  return { error: { code, message, ...(details ? { details } : {}), requestId } }
}
```

### What each step enforces

| Step | Iron Law |
|---|---|
| Schema parse with Zod | Never trust the client |
| AuthN → AuthZ → rate limit | Every protected endpoint |
| Idempotency key check before writes | Every POST/PUT/PATCH |
| Single `$transaction` for order + inventory + audit | Transactions or death |
| `logger.info` / `logger.error` with structured fields | Structured logging |
| `errorBody` helper used everywhere | Consistent error format |
