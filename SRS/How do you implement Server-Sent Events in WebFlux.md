<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# How do you implement Server-Sent Events in WebFlux?

> [!abstract] Short answer
> Return a **`Flux`** of **`ServerSentEvent<T>`** (or a `Flux` of data with **`produces = TEXT_EVENT_STREAM`** / `Accept: text/event-stream`). That is Spring’s reactive stand-in for MVC **`SseEmitter`**. Encode via **`ServerSentEventHttpMessageWriter`**. Send periodic heartbeats so disconnected clients are detected.

## Annotated controller streaming

Spring WebFlux *Return Values*: `Flux<ServerSentEvent<…>>` (or another reactive type) **emits server-sent events**. The wrapper is optional when you only write **data**, but then **`text/event-stream` must be requested or declared** on the mapping (`produces`).

`ServerSentEvent` javadoc (since 5.0): `Flux<ServerSentEvent>` / `Observable<ServerSentEvent>` is the reactive equivalent of MVC **`SseEmitter`**. Fields: `id`, `event`, `data`, `retry`, `comment`.

```java
@RestController
public class StockController {

    @GetMapping(path = "/stocks", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<String>> stocks() {
        return Flux.interval(Duration.ofSeconds(1))
                .map(i -> ServerSentEvent.builder("Stock Update #" + i)
                        .id(String.valueOf(i))
                        .event("quote")
                        .build());
    }
}
```

**Listing 1.** Conceptual annotated SSE endpoint — infinite `Flux` plus `TEXT_EVENT_STREAM`. Annotated REST: [[How do you implement a reactive REST controller in WebFlux]].

`ServerSentEventHttpMessageWriter` is the `HttpMessageWriter` for `"text/event-stream"`. Strings encode without an extra encoder; objects need a JSON `Encoder`.

```d2
direction: right
flux: "Flux<ServerSentEvent>\nor Flux + produces" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
writer: "ServerSentEventHttpMessageWriter\ntext/event-stream" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
http: "HTTP response\nstreamed events" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

flux -> writer -> http
```

**Fig. 1.** Elements are written as they arrive, not buffered as one JSON array. Not a WebSocket upgrade — [[What is the difference between WebSocket and Server-Sent Events]].

Reactive Core: when streaming (`text/event-stream`, `application/x-ndjson`), **send data periodically** (comment-only / empty SSE / other no-op) as a **heartbeat** so a dropped client is noticed.

Tests: `WebTestClient` *Streaming Responses* — `accept(TEXT_EVENT_STREAM)`, then `returnResult(…)` and **`StepVerifier` + `thenCancel()`** on an infinite stream — [[How do you test a WebFlux endpoint]].

> [!warning] Declare or accept `text/event-stream` if you skip `ServerSentEvent`
> A bare `Flux<String>` is not SSE unless the media type is event-stream. Otherwise you get ordinary streaming JSON/text, not SSE fields.

> [!warning] Heartbeat disconnected clients
> Without periodic writes, proxies and the server may keep a dead stream open. Official guidance is periodic no-op SSE (comment or empty event).

> [!warning] Cancel the subscription
> An infinite `Flux.interval` keeps producing until the HTTP subscriber cancels. Tests must `thenCancel()`; production depends on client disconnect + heartbeats. Backpressure on hot sources: [[How does Spring WebFlux handle backpressure]].

> [!tip] Interview answer
> **SSE in WebFlux is a `Flux` of `ServerSentEvent` (or data + `TEXT_EVENT_STREAM`), the reactive `SseEmitter`.** The writer streams `text/event-stream`. Heartbeat so you notice dropped clients. It is not WebSocket — one-way HTTP events, cancel on disconnect.
