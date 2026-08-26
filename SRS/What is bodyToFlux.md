<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is `bodyToFlux`?

> [!abstract] Short answer
> **`bodyToFlux(Class)`** (or **`ParameterizedTypeReference`**) **decodes an HTTP body as a stream of `T`** into a **`Flux<T>`**. On **`WebClient.retrieve()`** that is the **response**; on **`ServerRequest`** it is the **inbound** body. Use it for **many elements**, not one JSON object — [[What is bodyToMono]]. **`retrieve()` alone does nothing** until this (or `toEntityFlux` / `toEntityList` / `toBodilessEntity`) runs. **4xx/5xx** fail the `Flux` with **`WebClientException`** (typically **`WebClientResponseException`**) unless you add **`onStatus`**. Do **not** `.block()` on the event loop.

## Client `retrieve()` vs server `ServerRequest`

Spring *retrieve()* — stream of decoded objects:

```java
Flux<Quote> result = client.get()
        .uri("/quotes")
        .accept(MediaType.TEXT_EVENT_STREAM)
        .retrieve()
        .bodyToFlux(Quote.class);
```

**Listing 1.** Framework sample — SSE stream as `Flux<Quote>`. One object: [[What is bodyToMono]]. Client: [[What is WebClient]]. How-to: [[How do you call an external API from a WebFlux application]].

Same `ResponseSpec` as `bodyToMono`: **`onStatus`**, **`toEntityFlux`**, **`toEntityList`**. **`toEntityList`** is **`Mono<ResponseEntity<List<T>>>`** — the **whole list at once**, not a streamed `Flux`. **`toEntityFlux`**: you **must subscribe the inner `Flux`**, or the connection is not released (javadoc).

Dump trap: **`bodyToFlux(Stock.class)` then `subscribe()`** matches the **decode** shape, but **`subscribe` in a controller** is fire-and-forget — **return the `Flux`**. A subscriber that does I/O on the event loop is the [[How do you offload blocking work in WebFlux]] smell.

SSE: `accept(TEXT_EVENT_STREAM)` + `bodyToFlux` is the **client** counterpart of [[How do you implement Server-Sent Events in WebFlux]].

WebFlux.fn inbound (shortcut for `request.body(BodyExtractors.toFlux(Person.class))`):

```java
Flux<Person> people = request.bodyToFlux(Person.class);
```

**Listing 2.** *Functional Endpoints* — decode a **streaming** request body. Handler: [[What is a HandlerFunction in WebFlux]].

```d2
direction: right
http: "HTTP body bytes" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
dec: "HttpMessageReader\nbodyToFlux" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
flux: "Flux<T>\n(0..n elements)" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}

http -> dec -> flux
```

**Fig. 1.** Decoding starts when something **subscribes**. WebFlux controllers **return** the `Flux`; they do not call **`subscribe()`** or **`block()`**.

## `Flux` vs `Mono<List<T>>`

| Need | Typical API |
| --- | --- |
| One JSON object | `bodyToMono(Person.class)` |
| Stream of elements / SSE | `bodyToFlux(Quote.class)` |
| One JSON **array** as a **list** | `bodyToMono(new ParameterizedTypeReference<List<Person>>() {})` or `toEntityList` |
| Response + status + headers, streamed body | `toEntityFlux` |

A **`Mono<List<T>>`** is **one emission** of a **complete collection**. A **`Flux<T>`** can **interleave** decode with downstream processing. **`exchangeToFlux`** if you must inspect the **raw** `ClientResponse` (Spring: **`retrieve()` is shorter** for typical decoding).

> [!warning] Default 4xx/5xx are errors
> `bodyToFlux` never delivers the error JSON as `T` unless you **`onStatus`** (or `onErrorResume` on `WebClientResponseException`). Chain **`onStatus` on `ResponseSpec` before `bodyToFlux`** — after it you have a `Flux`, not a spec.

> [!warning] `blockFirst()` / `blockLast()` is not the WebFlux path
> It **does** subscribe and wait — fine on a **blocking** thread (tests, CLI). On **`reactor-http-nio-*`** it throws **`IllegalStateException`** — [[What happens if you call block on a WebFlux event loop]].

> [!warning] Content type is not optional
> JSON array vs **`application/x-ndjson`** vs **`text/event-stream`** need the matching **`HttpMessageReader`**. Wrong `Accept` → decode failure, not a silent empty `Flux`. Empty body typically **completes empty**.

> [!tip] Interview answer
> **`bodyToFlux` decodes the HTTP body to `Flux<T>` — many elements (SSE, NDJSON, streamed JSON).** After `WebClient.retrieve()`, or on `ServerRequest` in WebFlux.fn. Return the `Flux`; do not `block()` on the event loop. One object: `bodyToMono`. One JSON array as a list: `ParameterizedTypeReference` / `toEntityList`.

## See also

- [[What is bodyToMono]]
- [[What is WebClient]]
- [[How do you call an external API from a WebFlux application]]
- [[How do you implement functional endpoints in WebFlux]]
- [[How do you implement Server-Sent Events in WebFlux]]
- [[How do you offload blocking work in WebFlux]]
- [[What happens if you call block on a WebFlux event loop]]
- [[How do you handle errors in Spring WebFlux]]
- [[Is WebClient thread-safe]]
- [[What is a HandlerFunction in WebFlux]]
- [[What is Spring WebFlux]]
