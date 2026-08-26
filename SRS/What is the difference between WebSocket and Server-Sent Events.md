<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Spring/Framework/WebFlux #SRS

# What is the difference between WebSocket and Server-Sent Events?

> [!abstract] Short answer
> **WebSocket** (RFC **6455**) is a **full-duplex** protocol: after an HTTP **`Upgrade`**, **both** sides send on **one TCP connection**. **Server-Sent Events** stay on **HTTP**: the **server streams** `text/event-stream` to the client; the **client does not push** on that stream. Use WebSocket when the **client must send as often as the server**; use SSE when you only need **server→client** (feeds, notifications). An SSE `Flux` is **not** a drop-in WebSocket.

## Duplex messaging vs HTTP stream

Spring *WebSockets*: WebSocket is a **different TCP protocol from HTTP**, designed to work **over** HTTP (ports 80/443). Handshake uses `Upgrade: websocket` → **101 Switching Protocols**. After that, **messages flow on that socket**. REST/HTTP models **many URLs, request-response**. WebSocket is usually **one connect URL**, then an **event-driven messaging** app. It has **no message semantics** unless you agree (often **STOMP**).

Spring *When to Use WebSockets*: AJAX + **HTTP streaming or long polling** is enough for many UIs. WebSocket fits **low latency + high frequency + high volume** (collab, games, trading). Restrictive **proxies** may block `Upgrade`.

SSE in WebFlux: return **`Flux<ServerSentEvent>`** (or `Flux` + `TEXT_EVENT_STREAM`) — [[How do you implement Server-Sent Events in WebFlux]]. MVC analogue: **`SseEmitter`**. Client consume: `WebClient` **`accept(TEXT_EVENT_STREAM)` + `bodyToFlux`**.

Dump “REST = new TCP per request” is **oversimple** (keep-alive, HTTP/2). The contrast is **request-response vs a long-lived stream or socket**, not always a new TCP handshake.

```java
@GetMapping(path = "/ticks", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
public Flux<ServerSentEvent<String>> ticks() {
    return Flux.interval(Duration.ofSeconds(1))
            .map(i -> ServerSentEvent.builder("tick-" + i).build());
}
```

**Listing 1.** Conceptual SSE — **server→client only**. WebFlux WebSocket: `WebSocketHandler` composing `session.receive()` and `session.send(...)`.

```d2
direction: down
http: "HTTP request-response\n(REST)" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
sse: "SSE\nHTTP, server→client stream" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
ws: "WebSocket\nfull duplex on one socket" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Heartbeats: SSE comments / dummy events to detect disconnects; WebSocket/STOMP often have **built-in heartbeats**.

> [!warning] SSE is not duplex
> The browser **EventSource** API does not send application messages upstream. For client push, use **WebSocket** (or ordinary HTTP POST).

> [!warning] WebSocket is not “faster SSE”
> Different protocol and programming model (`WebSocketHandler` vs `Flux` + `text/event-stream`). Proxies and load balancers need **upgrade** support.

> [!tip] Interview answer
> **WebSocket: two-way messages after Upgrade on one connection. SSE: one-way HTTP event stream from the server.** Pick WebSocket when the client must talk back continuously; pick SSE for server-pushed updates over HTTP.

## See also

- [[How do you implement Server-Sent Events in WebFlux]]
- [[What is bodyToFlux]]
- [[What is Spring WebFlux]]
- [[What is the EnableWebSocket annotation]]
- [[What is the difference between Spring MVC and Spring WebFlux]]
