<!--
reps: 0
priority: 0
-->
#Networking/Web #Messaging/PollingConsumer #SRS
# What is the difference between polling and long polling

> [!abstract] Short answer
> Polling asks the server "anything new?" on a fixed schedule and gets an immediate (often empty) answer — simple, but latency averages half the interval and idle requests waste resources. Long polling holds the request open until the server *has* something (or a timeout fires), then answers and the client immediately re-requests — near-real-time push semantics over plain HTTP, at the cost of a held connection per client.

## Mechanics and tradeoffs

| | Short polling | Long polling |
|---|---|---|
| Request lifetime | answered instantly | held until data/timeout |
| Latency | up to one full interval | one round trip after the event |
| Empty-traffic cost | high (many no-op responses) | low (each response carries data) |
| Server cost | cheap per request, many requests | many concurrent open connections |
| Infrastructure | trivially stateless | needs proxies/LBs tuned for long timeouts |

```d2
direction: down
c: "Client" { width: 160; height: 60; style.fill: "#e3f2fd" }
sp: "Short polling:\nevery N sec -> 'no' / 'no' / 'yes'" { width: 340; height: 80; style.fill: "#fff3e0" }
lp: "Long polling:\nrequest held -> event -> response ->\nre-request immediately" { width: 380; height: 90; style.fill: "#e8f5e9" }
c -> sp
c -> lp
```

**Fig. 1.** Same goal, different blocking point: the client schedules in polling; the server blocks in long polling.

## Where each fits, and what replaced it

- **Short polling** fits status checks where staleness is tolerable (dashboards refreshing every 30 s) and caches/CDNs can absorb load.
- **Long polling** was the classic workaround for "server push over HTTP 1.x" (chat, feeds before WebSocket) — it survives where proxies or legacy clients block WebSocket, and it degrades gracefully.
- **Modern successors:** **Server-Sent Events** — one long-lived HTTP stream with `text/event-stream`, built-in reconnection, unidirectional server→client; and **WebSocket** — a full-duplex upgraded TCP socket ([[What is WebSocket]], [[How does the WebSocket handshake work in Spring]]). In messaging vocabulary this whole family is a pull-consumer pattern on the client side (#Messaging/PollingConsumer's territory): the consumer decides when to ask, versus a broker pushing to a listener.

> [!warning] Long polling is not a protocol — and held requests cost real resources
> There is no "long polling" standard: it is an application pattern over ordinary HTTP, so every proxy in the path (idle timeouts, buffering) must be configured to tolerate 30–120 s requests. Server-side, each held request pins a thread or container (servlet async/SSE/Netty matter), and load balancers' connection limits become the scaling ceiling. Interview lie to avoid: "long polling keeps the TCP connection so messages are never lost" — a dropped connection loses the in-flight event unless the client re-syncs by cursor/version ([[How do you prevent duplicate message or packet delivery]] applies to the re-request).

Push alternatives: [[What is WebSocket]]; HTTP semantics underneath: [[What is HTTP]]; the polling side of broker consumers: [[What is idempotency in HTTP and in messaging]] for at-least-once interactions.

> [!tip] Interview answer
> Polling: the client asks on a timer and gets an immediate answer — simple, stateless, but latency-bound and wasteful when idle. Long polling: the server holds the request until an event or timeout, giving push-like latency over plain HTTP at the price of many held connections and infrastructure timeouts. When latency and bidirectionality matter I move to SSE or WebSocket — long polling is the compatibility fallback, not the endgame.
