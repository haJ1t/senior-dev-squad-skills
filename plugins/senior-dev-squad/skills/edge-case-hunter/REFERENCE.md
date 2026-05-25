# Edge Case Hunter — Worked Example: File Upload

Full application of the 8-dimension matrix to a file upload feature.
Feature spec: "Users can upload a profile photo (JPEG/PNG/GIF, max 5 MB). The file is stored in S3, and the URL is saved to the user record."

---

## Dimension 1: Input Extremes

### EC-01: Zero-byte file
**Scenario:** User selects a file that is 0 bytes (e.g., an empty file created with `touch photo.jpg`).
**Expected:** Server rejects with 422 "File must not be empty." Client shows the error inline; no S3 write attempted.
**Actual:** Server reads Content-Length: 0, attempts `s3.putObject` with an empty buffer. S3 accepts it. A zero-byte URL is saved to the user record. Subsequent image renders a broken image tag.
**Severity:** HIGH
**Fix:** Validate `file.size > 0` before any I/O. Return 422 before opening the S3 client.

### EC-02: File exactly at the 5 MB boundary
**Scenario:** User uploads a file that is exactly 5,242,880 bytes (5 MiB).
**Expected:** Upload succeeds — the limit is "max 5 MB" and this is exactly at the boundary.
**Actual:** Server uses `file.size > 5_000_000` (5 MB in decimal). A 5 MiB file (5,242,880 bytes) exceeds the decimal limit and is incorrectly rejected.
**Severity:** MEDIUM
**Fix:** Decide on one unit (MiB or MB), document it in the spec, and apply it consistently in validation, UI copy, and error messages.

### EC-03: File with a dangerous name
**Scenario:** User uploads a file named `../../etc/passwd` or `<script>alert(1)</script>.jpg`.
**Expected:** Server strips or replaces the filename with a server-generated UUID key. The original filename is never used as an S3 key or reflected in HTML without escaping.
**Actual:** Server uses the original filename as the S3 key and includes it in the response JSON. A filename with `../` can traverse the S3 prefix. A filename with `<script>` tags is reflected in an admin dashboard without escaping — stored XSS.
**Severity:** CRITICAL
**Fix:** Generate a UUID key for S3 (`{userId}/{uuid}.{ext}`). Store the sanitized original filename in the DB for display only, HTML-escaped at render time.

### EC-04: Mismatched MIME type / magic bytes
**Scenario:** User renames `malware.exe` to `photo.jpg` and uploads it.
**Expected:** Server inspects the file's magic bytes (not just the Content-Type header or filename extension), rejects non-image files with 422.
**Actual:** Server checks only `Content-Type: image/jpeg` from the request header. The executable is stored in S3 and linked as a profile photo. If the CDN serves it with `Content-Disposition: inline`, a browser may execute it.
**Severity:** CRITICAL
**Fix:** Read the first 16 bytes on the server side; validate against known image magic bytes (`FFD8FF` for JPEG, `89504E47` for PNG, `47494638` for GIF). Reject anything that does not match.

---

## Dimension 2: Concurrency & Race Conditions

### EC-05: Double-submit — same user uploads two files simultaneously
**Scenario:** User clicks "Upload" and, while the first request is in-flight, clicks again (slow connection, impatient user). Two requests hit the server concurrently with different files.
**Expected:** Both files are stored in S3 under distinct keys. The second write to `user.avatar_url` wins (last-write-wins is acceptable); the first S3 object becomes an orphan but no data is lost.
**Actual:** Both requests read `user.version = 3`, both write `avatar_url` and `version = 4`. The second write silently overwrites the first with no conflict detection. One S3 file is orphaned (storage leak). If an orphan-cleanup job runs between the two writes it may delete the file the user just saw confirmed.
**Severity:** HIGH
**Fix:** Use optimistic locking: `UPDATE users SET avatar_url=?, version=version+1 WHERE id=? AND version=?`. The second update affects 0 rows → return 409, prompt user to retry. Track orphaned S3 keys for async cleanup.

### EC-06: Upload succeeds but DB write fails (partial state)
**Scenario:** S3 `putObject` returns 200. Immediately after, the DB connection drops before `UPDATE users SET avatar_url` commits.
**Expected:** System detects the failure, rolls back or retries the DB write. The S3 object is either cleaned up or re-linked on retry.
**Actual:** S3 has the file; the DB has the old URL. The user sees a success toast but their avatar does not change. The S3 object is orphaned permanently.
**Severity:** HIGH
**Fix:** Write an `upload_pending` record to the DB first (with the S3 key). After S3 confirms, update the record to `confirmed`. A background job sweeps `pending` records older than 10 minutes and deletes the orphaned S3 objects.

---

## Dimension 3: Network Failures

### EC-07: Connection drops mid-upload
**Scenario:** User is on a flaky mobile connection. The TCP connection resets after 60% of the file has been transmitted.
**Expected:** Server detects the incomplete body, discards any partial buffer, returns no response (connection closed). No partial file is written to S3.
**Actual:** Depending on the streaming upload implementation, a partial object may be written to S3 (multipart upload left open). Storage meter is charged for partial data. If the key is predictable, a retry may try to read a corrupted partial file.
**Severity:** MEDIUM
**Fix:** Use S3 multipart upload with `AbortMultipartUpload` in the error handler. Set a lifecycle rule on the bucket to abort incomplete multipart uploads after 24 hours.

### EC-08: S3 returns 503 during upload (transient)
**Scenario:** S3 returns `ServiceUnavailable` (503) while `putObject` is in progress.
**Expected:** Server retries with exponential backoff (max 3 attempts). If all retries fail, returns 503 to the client with a Retry-After header. The client shows "Upload failed — please try again."
**Actual:** Server does not retry. Returns 500 immediately. The client shows a generic "Something went wrong" with no actionable guidance.
**Severity:** HIGH
**Fix:** Wrap `s3.putObject` in a retry helper with exponential backoff (base 500 ms, factor 2, max 3). On exhaustion, surface a 503 with `Retry-After: 30`. Log the S3 error with the request ID for ops visibility.

---

## Dimension 4: Time & Timezone

### EC-09: Upload during DST spring-forward gap
**Scenario:** Server is in US/Eastern. At 02:00 clocks jump to 03:00. An upload timestamped at 02:30 is stored in the DB.
**Expected:** `uploaded_at` is stored as UTC. Display layer converts to local time. No time is lost.
**Actual:** Server stores `uploaded_at = new Date()` in local time. The timestamp `2024-03-10T02:30:00-05:00` does not exist — the local timezone skipped that hour. The ORM coerces it to an adjacent value. The audit log shows an upload at a time that never occurred.
**Severity:** MEDIUM
**Fix:** Always store timestamps as UTC in the DB. Convert to local time only at the display layer with an explicit IANA timezone string.

### EC-10: Pre-signed URL expiry during large upload
**Scenario:** The client receives a pre-signed S3 URL valid for 15 minutes. The user's file is large (4.9 MB) on a slow connection; the upload takes 17 minutes.
**Expected:** The system either issues a sufficiently long-lived pre-signed URL, or refreshes the URL before expiry, or the backend proxies the upload directly.
**Actual:** The pre-signed URL expires mid-upload. S3 returns 403. The client receives no meaningful error — just an opaque XML response. The user sees the upload "complete" on the client side (progress bar hit 100%) but no file is stored.
**Severity:** HIGH
**Fix:** Set pre-signed URL TTL to `max_upload_time * 2` (e.g., 30 minutes for a 5 MB file on a slow connection). Alternatively, proxy the upload server-side where you control the S3 credential lifetime.

---

## Dimension 5: State Corruption

### EC-11: Upload retried after timeout — duplicate S3 objects
**Scenario:** Client times out after 30 s, retries the upload. The original request completes on the server 2 seconds later.
**Expected:** The second upload is deduplicated — the server recognises it as a retry (via idempotency key) and returns the URL from the first completed upload. Only one S3 object is created.
**Actual:** No idempotency key is used. Both requests complete. Two S3 objects exist. The DB is updated twice. If the client uses the URL from the second response and the first object is cleaned up by an orphan sweep, the user's avatar breaks.
**Severity:** HIGH
**Fix:** Require clients to send an `Idempotency-Key` header (UUID generated before the first attempt). Cache `(user_id, idempotency_key) → s3_url` in Redis for 24 hours. On duplicate key, return the cached URL without re-uploading.

### EC-12: User account deleted while upload is in-flight
**Scenario:** Admin deletes the user account (GDPR erasure). Simultaneously, the user's upload completes and the server tries to write `avatar_url` to the now-deleted user record.
**Expected:** The DB write fails with a foreign-key violation or 404. The S3 object is queued for deletion. The upload response returns 410 Gone.
**Actual:** The DB update succeeds (soft-delete leaves the row). The S3 file is stored and linked to a logically-deleted user. The GDPR erasure is incomplete — personal data persists in S3.
**Severity:** CRITICAL
**Fix:** Check user status before writing to S3. Add a post-delete cleanup job that scans `avatar_url` for deleted users and queues S3 object deletions. For hard GDPR delete, include S3 key in the deletion transaction's outbox.

---

## Dimension 6: Scale Extremes

### EC-13: User uploads maximum-size file when disk (or memory buffer) is near full
**Scenario:** Server buffers the incoming multipart body to disk before forwarding to S3. Disk has 3 MB free. User uploads a 4.9 MB file.
**Expected:** Server streams directly to S3 without buffering to disk, or detects low-disk condition and returns 503 before accepting the body.
**Actual:** Server buffers to `/tmp`. Write fails mid-buffer. The framework returns a 500 with a stack trace that includes the server's filesystem path. Disk usage is now at 100%, causing unrelated services to fail.
**Severity:** CRITICAL
**Fix:** Stream directly from the request body to S3 without disk buffering (pipe the multipart stream). Implement a disk-usage health check; return 503 before accepting uploads when disk > 90%.

### EC-14: Zero uploads in the user's history (empty state)
**Scenario:** First-time user opens their profile page before uploading an avatar.
**Expected:** A default avatar placeholder is shown. No broken image tag. No 404 logged for a missing S3 object.
**Actual:** `avatar_url` is NULL. The `<img src={user.avatarUrl}>` renders with `src="null"` (string). The browser makes a request to `GET /null`, generating a 404 on the server and a broken image icon in the UI.
**Severity:** MEDIUM
**Fix:** Use a fallback: `<img src={user.avatarUrl ?? '/assets/default-avatar.png'}>`. On the server, return the default URL from the API so clients do not need to special-case null.

---

## Dimension 7: Integration Failures

### EC-15: S3 bucket policy change blocks writes silently
**Scenario:** Ops team updates the S3 bucket policy to deny `s3:PutObject` from the app IAM role (mis-configuration during a security hardening push).
**Expected:** The upload endpoint returns a clear 503 "Storage temporarily unavailable." Ops is alerted via the error-rate monitor within 5 minutes.
**Actual:** `s3.putObject` throws an `AccessDenied` exception. The server catches it with a generic `catch (e) { return 500 }`. The error is not logged with the S3 error code. Ops sees a spike in 500s but cannot determine the root cause without checking CloudTrail.
**Severity:** HIGH
**Fix:** Catch S3 errors by code: `AccessDenied` → 503 with alert; `NoSuchBucket` → 503 with PagerDuty page; `SlowDown` → 429 with retry logic. Log the S3 error code and request ID in every catch branch.

### EC-16: Image processing service (thumbnail generator) is down
**Scenario:** After upload, the server publishes a message to a queue for async thumbnail generation. The thumbnail worker is down for 2 hours.
**Expected:** The original upload succeeds and is accessible. Thumbnails are generated once the worker recovers (queue is durable). The user sees the original image until thumbnails are ready.
**Actual:** The server waits synchronously for thumbnail generation before returning the response. The request times out after 30 s. The user receives a 504. The original file IS stored in S3 but the user has no way to know, so they upload again — creating a duplicate.
**Severity:** HIGH
**Fix:** Decouple thumbnail generation: return the upload URL immediately after S3 confirms. Publish to a durable queue (SQS, RabbitMQ). Return a placeholder thumbnail URL until the worker processes the message.

---

## Dimension 8: Human Errors

### EC-17: User pastes a URL instead of selecting a file
**Scenario:** User copies an image URL from another tab and pastes it into the file input field. The browser submits a form with an empty file input but a pasted string in a text field.
**Expected:** Server validates that the file input is not empty and that the Content-Type is `multipart/form-data` with a non-empty file part. Returns 422 "Please select a file."
**Actual:** Server reads the file part as empty. Proceeds to validate file size (0 bytes passes the `> 0` check bug from EC-01). Stores a zero-byte object.
**Severity:** MEDIUM
**Fix:** Validate file presence AND size server-side. Client-side validation on the file input helps UX but cannot be trusted.

### EC-18: User uploads the wrong file type accidentally (HEIC from iPhone)
**Scenario:** iPhone user selects a photo from their camera roll. iOS exports it as HEIC format, not JPEG. The browser sends `Content-Type: image/heic`.
**Expected:** Server either converts HEIC to JPEG/WebP before storing, or returns a user-friendly error "This file type (HEIC) is not supported. Please convert to JPEG or PNG."
**Actual:** Server's MIME allowlist blocks `image/heic` with a generic "Invalid file type" error. The user has no idea what HEIC is or how to fix it. Bounce rate for mobile users uploading avatars is measurably higher.
**Severity:** MEDIUM
**Fix:** Either add HEIC to the allowed types with server-side conversion (Sharp, ImageMagick), or return a specific, actionable error message that names the file type and suggests a fix.

---

## Edge Case Summary

| Dimension | Cases Found | CRITICAL | HIGH | MEDIUM |
|-----------|------------|---------|------|--------|
| 1. Input Extremes | 4 | 2 | 1 | 1 |
| 2. Concurrency | 2 | 0 | 2 | 0 |
| 3. Network Failures | 2 | 0 | 1 | 1 |
| 4. Time & Timezone | 2 | 0 | 1 | 1 |
| 5. State Corruption | 2 | 1 | 1 | 0 |
| 6. Scale Extremes | 2 | 1 | 0 | 1 |
| 7. Integration Failures | 2 | 0 | 2 | 0 |
| 8. Human Errors | 2 | 0 | 0 | 2 |
| **Total** | **18** | **4** | **8** | **6** |

**Dimensions covered: 8/8**

CRITICAL findings (block merge): EC-03, EC-04, EC-12, EC-13
HIGH findings (fix in PR or tracked issue): EC-01, EC-05, EC-06, EC-08, EC-10, EC-11, EC-15, EC-16
MEDIUM findings (file issue, add TODO): EC-02, EC-07, EC-09, EC-14, EC-17, EC-18
