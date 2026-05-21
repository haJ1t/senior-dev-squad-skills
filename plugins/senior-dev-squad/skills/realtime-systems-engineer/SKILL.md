---
name: realtime-systems-engineer
description: "WebSocket, SSE, WebTransport, reconnect, backpressure, Redis pub/sub, fan-out, presence, horizontal scaling, graceful shutdown. Use when building or debugging realtime systems."
---

# Realtime Systems Engineer

## Overview

Design and implement production-grade realtime communication layers: transport selection, connection lifecycle, delivery guarantees, horizontal scaling, and observability. Realtime systems fail in ways that are invisible until they hit production — silent disconnects, message loss under load, thundering-herd reconnects, and fan-out amplification that melts Redis. Every decision made without understanding the failure modes will surface at 3 AM.

**Core principle:** CHOOSE THE DUMBEST TRANSPORT THAT MEETS YOUR DELIVERY REQUIREMENTS, then make it bulletproof.

## The Iron Law

```
NEVER SHIP A PERSISTENT CONNECTION WITHOUT RECONNECT, HEARTBEAT, AND BACKPRESSURE
```

## When to Use

**Use this when:**
- Implementing WebSocket servers, SSE endpoints, or long-poll handlers
- Designing presence, rooms, chat, live dashboards, or collaborative editing
- Adding horizontal scaling to an existing realtime service
- Debugging dropped messages, silent disconnects, or fan-out latency spikes

**Use this ESPECIALLY when:**
- Someone says "just use Socket.IO, it handles all that" (it does not)
- The feature is "just a live counter" (fan-out to 100k connections is not just anything)
- You are adding authentication to an existing WebSocket server
- The service needs to survive a rolling deploy without dropping active connections

**Don't skip when:**
- Under time pressure — missing reconnect logic means your users silently stop receiving updates
- The client is a mobile app — lossy networks make connection hygiene 10x more important

### Transport Selection

Pick the transport before writing a single line of server code.

| Transport | Direction | Use Case | Avoid When |
|-----------|-----------|----------|-----------|
| WebSocket | Bidirectional | Chat, collab, games, presence | Client only needs server push |
| SSE | Server → Client | Dashboards, feeds, live logs | Client must send frequent messages |
| Long-poll | Server → Client | Fallback, firewalled environments | Latency < 500 ms required |
| WebTransport | Bidirectional | Gaming, video, unreliable-OK | Browser support not universal yet |

Choose SSE over WebSocket when clients only consume events — one HTTP/2 connection, automatic reconnect in the browser, no custom framing.

### Connection Lifecycle

Every connection must implement three things: handshake validation, heartbeat, and reconnect with resume.

**WebSocket server with heartbeat (Node.js / `ws`):**

```ts
import { WebSocketServer, WebSocket } from 'ws';
import { IncomingMessage } from 'http';

const HEARTBEAT_INTERVAL_MS = 30_000;
const HEARTBEAT_TIMEOUT_MS = 10_000;

const wss = new WebSocketServer({ noServer: true });

wss.on('connection', (ws: WebSocket & { isAlive?: boolean }, req: IncomingMessage) => {
  ws.isAlive = true;

  ws.on('pong', () => { ws.isAlive = true; });

  ws.on('message', (data) => handleMessage(ws, data));

  ws.on('close', () => cleanup(ws));
});

// Heartbeat sweep — terminate zombies
const heartbeat = setInterval(() => {
  wss.clients.forEach((ws: WebSocket & { isAlive?: boolean }) => {
    if (ws.isAlive === false) {
      ws.terminate();
      return;
    }
    ws.isAlive = false;
    ws.ping();
  });
}, HEARTBEAT_INTERVAL_MS);

wss.on('close', () => clearInterval(heartbeat));
```

**HTTP upgrade hook — auth before accept:**

```ts
server.on('upgrade', async (req, socket, head) => {
  try {
    const user = await authenticateUpgrade(req); // validate JWT/session here
    wss.handleUpgrade(req, socket, head, (ws) => {
      wss.emit('connection', ws, req, user);
    });
  } catch {
    socket.write('HTTP/1.1 401 Unauthorized\r\n\r\n');
    socket.destroy();
  }
});
```

Authentication MUST happen in the `upgrade` handler, not after the WebSocket handshake completes. A connected but unauthenticated socket is an open vulnerability.

### Reconnect with Exponential Backoff and Resume

Clients must reconnect automatically. The reconnect algorithm must include jitter to prevent thundering-herd after a server restart.

```ts
class ReconnectingSocket {
  private ws: WebSocket | null = null;
  private attempt = 0;
  private lastEventId: string | null = null;

  connect() {
    const url = this.lastEventId
      ? `${WS_URL}?resumeFrom=${this.lastEventId}`
      : WS_URL;

    this.ws = new WebSocket(url);

    this.ws.addEventListener('open', () => { this.attempt = 0; });

    this.ws.addEventListener('message', ({ data }) => {
      const msg = JSON.parse(data);
      this.lastEventId = msg.id ?? this.lastEventId;
      this.onMessage(msg);
    });

    this.ws.addEventListener('close', ({ code }) => {
      if (code === 1001) return; // going away — deliberate, no reconnect
      this.scheduleReconnect();
    });
  }

  private scheduleReconnect() {
    const base = Math.min(30_000, 500 * 2 ** this.attempt);
    const jitter = Math.random() * base * 0.3;
    const delay = base + jitter;
    this.attempt++;
    setTimeout(() => this.connect(), delay);
  }
}
```

Store `lastEventId` in `localStorage` for cross-tab resume. The server uses it to replay missed events from a short-lived ring buffer (Redis LRANGE is sufficient for < 5 minutes of history).

### Message Delivery Guarantees

Define your delivery contract before implementation — the wrong default causes silent data loss.

| Guarantee | Mechanism | Cost |
|-----------|-----------|------|
| At-most-once | Fire and forget | Cheapest, lossy |
| At-least-once | Ack + retry queue | Duplicates possible — require idempotency |
| Exactly-once | Dedup store + ack | Expensive — only for financial events |

For at-least-once: assign a UUID to every outbound message. The client acks by sending `{ type: "ack", id: "<uuid>" }`. The server retains unacked messages in a per-connection queue and retransmits on reconnect. Expire unacked messages after a TTL (e.g., 5 minutes) to prevent unbounded growth.

### Backpressure and Flow Control

A slow client should never block a fast producer. Enforce write-side buffering limits:

```ts
function safeSend(ws: WebSocket, payload: unknown): boolean {
  // ws.bufferedAmount reflects bytes queued but not yet sent
  if ((ws as any).bufferedAmount > 64 * 1024) {
    // Client is not draining — drop or disconnect
    ws.close(1008, 'send buffer overflow');
    return false;
  }
  ws.send(JSON.stringify(payload));
  return true;
}
```

On the server side, use a per-connection message queue with a max depth. When the queue is full, drop the oldest non-critical message (e.g., presence updates) before dropping critical ones (e.g., order fills).

### Horizontal Scaling with Redis Pub/Sub Fan-Out

Stateless WebSocket servers behind a load balancer require a shared message bus. Redis pub/sub is the standard choice for < 100k concurrent connections. Above that, evaluate NATS or Kafka.

```ts
import { createClient } from 'redis';

const pub = createClient({ url: REDIS_URL });
const sub = pub.duplicate();

await pub.connect();
await sub.connect();

// When a client sends a message to room "room:42":
async function broadcast(roomId: string, message: unknown) {
  await pub.publish(`room:${roomId}`, JSON.stringify(message));
}

// Each server instance subscribes to all rooms its local clients are in:
async function joinRoom(ws: WebSocket, roomId: string) {
  const channel = `room:${roomId}`;
  await sub.subscribe(channel, (raw) => {
    // Deliver to all local clients in this room
    localRoomMembers.get(roomId)?.forEach((client) => {
      if (client.readyState === WebSocket.OPEN) client.send(raw);
    });
  });
}
```

**Sticky sessions vs. stateless:** sticky sessions (IP hash or cookie-based) let you skip Redis for small deployments, but they break during rolling deploys and uneven load distribution. Prefer stateless fan-out via Redis pub/sub for any service that must survive deploys without dropping connections.

### Graceful Shutdown and Drain

Rolling deploys must not force-close active connections. Implement a drain phase:

```ts
process.on('SIGTERM', async () => {
  // 1. Stop accepting new connections
  wss.close();

  // 2. Notify all clients to reconnect (code 1012 = service restart)
  wss.clients.forEach((ws) => ws.close(1012, 'server restarting'));

  // 3. Wait for clients to drain (max 30 s)
  const deadline = Date.now() + 30_000;
  while (wss.clients.size > 0 && Date.now() < deadline) {
    await new Promise((r) => setTimeout(r, 500));
  }

  // 4. Clean up pub/sub subscriptions
  await sub.quit();
  await pub.quit();

  process.exit(0);
});
```

Clients that receive close code 1012 should reconnect immediately (no backoff delay) because the server is restarting intentionally.

### Observability for Socket Services

Standard HTTP metrics (request rate, latency) do not capture realtime health. Instrument these:

- **Active connections** — gauge, per server instance and per room
- **Message throughput** — counter (inbound + outbound), labelled by message type
- **Reconnect rate** — counter; a spike means a bug or deployment event
- **Heartbeat timeout evictions** — counter; sustained non-zero means network issues
- **Send buffer depth** — histogram per connection; p99 > 32 KB signals slow consumers
- **Fan-out latency** — time from `pub.publish()` to last subscriber delivery

Emit structured logs on connect, disconnect, auth failure, and buffer overflow. Include `connectionId`, `userId`, `roomId`, and `durationMs` on disconnect events.

## Red Flags — STOP and Follow Process

If you catch yourself thinking:
- "We'll add reconnect logic later" — silent disconnects are invisible to users and to you
- "Redis pub/sub can handle any scale" — it cannot; benchmark your fan-out at target concurrency first
- "Authentication can go after the handshake" — this creates an unauthenticated socket window
- "We don't need heartbeats, TCP keepalive is enough" — TCP keepalive operates at the OS level and does not detect application-layer zombies
- "At-most-once is fine, it's just UI state" — it will not be fine when the UI silently drifts from server state
- No backpressure limit on the send buffer

**ALL of these mean: STOP. Return to the relevant section above.**

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Socket.IO handles reconnect automatically" | Socket.IO reconnect does not resume missed messages; you still need a replay buffer. |
| "We only have 1000 users, no need for Redis" | A single deploy event creates a thundering reconnect herd even at 1000 connections. |
| "Heartbeats waste bandwidth" | A 46-byte ping every 30 seconds is cheaper than debugging ghost connections at 2 AM. |
| "Sticky sessions are simpler than pub/sub" | Sticky sessions break silently on instance failure and uneven pod restarts. |
| "We'll add observability after launch" | You cannot diagnose a 10% message-drop rate you cannot measure. |

## Your Human Partner's Signals You're Doing It Wrong

**Watch for these redirections:**
- "Users are complaining the feed stops updating" — you have no reconnect or heartbeat
- "We're seeing duplicate messages" — at-least-once delivery without idempotency keys
- "The new deploy dropped everyone" — no graceful shutdown drain
- "It works on my machine but not under load" — no backpressure, fan-out untested at scale
- "Why is Redis CPU at 100%?" — fan-out is linear per subscriber; you need channel batching or a broker

**When you see these:** STOP. Return to the relevant section above.

## Related Skills

- **backend-senior-engineer** — API design, database patterns, and service architecture that sit beneath the realtime layer
- **distributed-systems-architect** — consistency models, partition tolerance, and broker selection at scale
- **performance-engineer** — profiling fan-out hot paths, benchmarking Redis pub/sub throughput, and load-testing socket servers
- **observability-pro** — metric instrumentation, alerting on reconnect rate and buffer depth, and distributed tracing across async message paths

## Verification

- [ ] Transport choice is documented with explicit rationale
- [ ] WebSocket server implements ping/pong heartbeat with zombie termination
- [ ] Authentication happens in the `upgrade` handler, not post-handshake
- [ ] Client reconnect uses exponential backoff with jitter
- [ ] Reconnect stores and sends `lastEventId` for resume
- [ ] Message delivery guarantee is explicit (at-most / at-least / exactly once)
- [ ] At-least-once messages have idempotency keys and a server-side ack queue
- [ ] Send buffer depth is bounded; slow clients are disconnected or backpressured
- [ ] Fan-out uses Redis pub/sub (or equivalent broker) — no in-process broadcast across instances
- [ ] Graceful shutdown sends close code 1012 and drains before process exit
- [ ] Active connections, reconnect rate, and fan-out latency are instrumented
- [ ] Load test confirms behavior at 2x expected peak concurrent connections
