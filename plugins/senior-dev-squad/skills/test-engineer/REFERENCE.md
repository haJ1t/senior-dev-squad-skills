# Worked Example — Password Reset Flow

This reference shows which tests to write at each pyramid level for a complete password reset feature: request a reset link → validate the token → set a new password. Every snippet is annotated with *why* it belongs at that level.

---

## Feature summary

1. User submits email → system generates a short-lived signed token, stores it, emails a link.
2. User clicks the link → system validates token exists, belongs to that email, and is not expired.
3. User submits a new password → system hashes it, saves it, invalidates the token, and logs the user in.

---

## Level 1 — Unit Tests

**What goes here:** Pure functions with no I/O. Token generation, expiry logic, password hashing rules.

**Why here:** These run in milliseconds, have no infrastructure dependencies, and catch regressions on the logic that everything else depends on.

```typescript
// token.test.ts
import { generateResetToken, isTokenExpired } from './token'

describe('generateResetToken', () => {
  it('returns a 32-byte hex string', () => {
    const token = generateResetToken()
    expect(token).toMatch(/^[0-9a-f]{64}$/)
  })

  it('returns a different value on each call', () => {
    expect(generateResetToken()).not.toBe(generateResetToken())
  })
})

describe('isTokenExpired', () => {
  it('returns false when token was created within the TTL', () => {
    const createdAt = new Date(Date.now() - 10 * 60 * 1000) // 10 min ago
    expect(isTokenExpired(createdAt, 60)).toBe(false)       // 60 min TTL
  })

  it('returns true when token age exceeds TTL', () => {
    const createdAt = new Date(Date.now() - 90 * 60 * 1000) // 90 min ago
    expect(isTokenExpired(createdAt, 60)).toBe(true)
  })

  it('returns true for a token created exactly at the TTL boundary', () => {
    const createdAt = new Date(Date.now() - 60 * 60 * 1000)
    expect(isTokenExpired(createdAt, 60)).toBe(true)
  })
})
```

**Why NOT e2e/integration here:** Expiry logic has no network or DB component. Testing it end-to-end would require controlling the system clock across processes — far slower with no additional confidence.

---

## Level 2 — Integration Tests

**What goes here:** The API endpoints that coordinate token storage, email dispatch, and DB writes. Test against a real (test) database; mock only third-party outbound calls (the email provider).

**Why here:** The unit tests above prove the logic. Integration tests prove the *wiring* — that the endpoint correctly persists the token and that the reset endpoint reads it back and invalidates it after use.

```typescript
// password-reset.integration.test.ts
import request from 'supertest'
import { app } from '../app'
import { db } from '../db'
import { sendEmail } from '../email' // mocked below

jest.mock('../email')

beforeEach(async () => {
  await db.users.create({ email: 'ada@example.com', passwordHash: 'old-hash' })
})

afterEach(async () => {
  await db.passwordResetTokens.deleteMany({})
  await db.users.deleteMany({})
})

describe('POST /auth/password-reset/request', () => {
  it('creates a token in the DB and dispatches an email', async () => {
    await request(app)
      .post('/auth/password-reset/request')
      .send({ email: 'ada@example.com' })
      .expect(200)

    const token = await db.passwordResetTokens.findOne({ userEmail: 'ada@example.com' })
    expect(token).not.toBeNull()
    expect(sendEmail).toHaveBeenCalledWith(
      expect.objectContaining({ to: 'ada@example.com', subject: expect.stringContaining('reset') })
    )
  })

  it('returns 200 even for unknown email (prevents user enumeration)', async () => {
    await request(app)
      .post('/auth/password-reset/request')
      .send({ email: 'nobody@example.com' })
      .expect(200)

    expect(sendEmail).not.toHaveBeenCalled()
  })
})

describe('POST /auth/password-reset/confirm', () => {
  it('updates the password and invalidates the token on valid input', async () => {
    const { token } = await db.passwordResetTokens.create({
      userEmail: 'ada@example.com',
      expiresAt: new Date(Date.now() + 30 * 60 * 1000),
    })

    await request(app)
      .post('/auth/password-reset/confirm')
      .send({ token, newPassword: 'Correct-Horse-Battery-9!' })
      .expect(200)

    const used = await db.passwordResetTokens.findOne({ token })
    expect(used).toBeNull() // token consumed

    const user = await db.users.findOne({ email: 'ada@example.com' })
    expect(user!.passwordHash).not.toBe('old-hash')
  })

  it('returns 400 for an expired token', async () => {
    const { token } = await db.passwordResetTokens.create({
      userEmail: 'ada@example.com',
      expiresAt: new Date(Date.now() - 1), // already expired
    })

    await request(app)
      .post('/auth/password-reset/confirm')
      .send({ token, newPassword: 'AnyPassword1!' })
      .expect(400)
  })

  it('returns 400 for a token that was already used', async () => {
    // Token was consumed in a prior request; it no longer exists in DB.
    await request(app)
      .post('/auth/password-reset/confirm')
      .send({ token: 'already-used-token', newPassword: 'AnyPassword1!' })
      .expect(400)
  })
})
```

**Why NOT unit here:** These tests exercise the full handler stack — middleware, DB queries, and the token lookup. A unit test with all of that mocked would prove nothing about whether the route actually works. **Why NOT e2e:** Driving a browser to exercise these endpoints adds ~10s per test run and tests the same backend contract already covered here.

---

## Level 3 — E2E Test

**What goes here:** One critical-path scenario driven through a real browser. Proves the UI, the API, and the email link all connect correctly in a deployed-like environment.

**Why here:** Only e2e can catch mismatches between the frontend form and the backend contract (e.g., wrong field name, wrong redirect URL). One test is enough — the edge cases are already covered by unit and integration tests above.

```typescript
// password-reset.e2e.test.ts  (Playwright)
import { test, expect } from '@playwright/test'
import { createTestUser, getLastEmailTo } from '../test-helpers'

test('user can reset their password via email link', async ({ page }) => {
  await createTestUser({ email: 'ada@example.com', password: 'OldPass1!' })

  // Step 1: request reset
  await page.goto('/auth/login')
  await page.getByRole('link', { name: 'Forgot password?' }).click()
  await page.getByLabel('Email').fill('ada@example.com')
  await page.getByRole('button', { name: 'Send reset link' }).click()
  await expect(page.getByText('Check your email')).toBeVisible()

  // Step 2: follow the link from the email
  const { resetUrl } = await getLastEmailTo('ada@example.com')
  await page.goto(resetUrl)

  // Step 3: submit new password
  await page.getByLabel('New password').fill('NewPass-Secure-99!')
  await page.getByLabel('Confirm password').fill('NewPass-Secure-99!')
  await page.getByRole('button', { name: 'Set new password' }).click()

  // Step 4: assert logged in with new credentials
  await expect(page).toHaveURL('/dashboard')
  await expect(page.getByText('ada@example.com')).toBeVisible()
})
```

**Why NOT integration here:** The browser drives real navigation and real form submission. There is no way to replicate "user follows the link in their email" at the integration layer without a full browser.

---

## Summary — Which level owns what

| Concern | Level | Reason |
|---------|-------|--------|
| Token is random and 64 hex chars | Unit | Pure function, no I/O |
| Expiry boundary (at/before/after TTL) | Unit | Clock-dependent logic, mock the clock |
| Token stored in DB after request | Integration | Requires real DB write |
| Unknown email returns 200 (anti-enumeration) | Integration | Security contract on the API boundary |
| Expired token rejected | Integration | DB read + business rule |
| Token consumed after use | Integration | DB mutation verified |
| Full browser journey: request → email → confirm → dashboard | E2E | Only a browser can exercise the UI + email link together |
