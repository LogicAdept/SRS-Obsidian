<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is WebClient?

> [!abstract] Short answer
> **`WebClient`** is Spring WebFlux’s **non-blocking, reactive HTTP client** (since **Spring Framework 5.0**): a **functional fluent API** on Reactor that returns **`Mono` / `Flux`**. Default transport is **Reactor Netty**. Imperative apps use **`RestClient`**; **`RestTemplate` is deprecated as of Framework 7.0**.

## Client, not a controller annotation

Spring *WebClient*: fully non-blocking, **streaming**, same **codecs** as the WebFlux server. You compose the request with lambdas; Reactor runs it — you do not start threads yourself.

REST Clients chapter: non-blocking I/O, **Reactive Streams back pressure**, high concurrency with few threads, fluent lambdas, **sync and async** use, streaming up or down.

Typical call:

```java
WebClient client = WebClient.create("https://example.org");

Mono<Person> result = client.get()
        .uri("/persons/{id}", id)
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .bodyToMono(Person.class);
```

**Listing 1.** Conceptual Spring `retrieve()` sample — body only. Stream: `bodyToFlux`. Entity: `toEntity`. How-to in an app: [[How do you call an external API from a WebFlux application]]. Decode: [[What is bodyToMono]], [[What is bodyToFlux]].

Create: `WebClient.create()`, `create(baseUrl)`, or `WebClient.builder()` (defaults, filters, codecs, `ClientHttpConnector`). **Once `build()` returns, the client is immutable**; `mutate()` clones settings onto a new builder.

Boot: inject auto-configured **`WebClient.Builder`** so the client shares Netty loops and codecs with the server.

```d2
direction: down
app: "Your code\nget / post / retrieve" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
wc: "WebClient\n(immutable instance)" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
conn: "ClientHttpConnector\nNetty / JDK / Jetty / HC" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

app -> wc -> conn
```

**Fig. 1.** `WebClient` is a facade; an HTTP library does the I/O. Default: **`WebClient.create()` → Reactor Netty**. Also: JDK `HttpClient`, Jetty, Apache HttpComponents, or any `ClientHttpConnector`.

| Client | Role |
| --- | --- |
| **`WebClient`** | Reactive / streaming (and you *can* `.block()` for a sync wait) |
| **`RestClient`** | Modern **blocking** fluent client |
| **`RestTemplate`** | Classic blocking template — **deprecated in 7.0**, remove later |

Full comparison: [[What is the difference between RestTemplate WebClient and RestClient]]. Tests: [[What is the difference between WebClient and WebTestClient]].

Default Reactor Netty `HttpClient` joins global **`HttpResources`** (event loops + pool) — same loops as a Netty WebFlux server unless you install custom `LoopResources`.

> [!warning] `retrieve()` turns 4xx/5xx into errors
> Default: `WebClientResponseException` (status subclasses). Override with `onStatus`, or handle downstream (`onErrorResume`).

> [!warning] `.block()` is the sync hatch, not the WebFlux path
> REST Clients lists synchronous use; on a Netty **event-loop** thread that wait stalls other work — [[What happens if you call block on a WebFlux event loop]].

> [!warning] `RestTemplate` was not deprecated in Spring 5
> 5.0 added `WebClient` as the reactive alternative. **Deprecation is Framework 7.0 → `RestClient`**. WebFlux request handling still must not use blocking clients on the loop.

> [!warning] Default codec buffer is 256 KB
> Larger bodies throw `DataBufferLimitException`. Raise `defaultCodecs().maxInMemorySize(...)` on the builder.

> [!tip] Interview answer
> **`WebClient` is the WebFlux HTTP client: fluent, non-blocking, `retrieve().bodyToMono`/`bodyToFlux`, Reactor Netty by default.** Share one built instance (`mutate()` to copy). `RestClient` is the blocking replacement for `RestTemplate` (deprecated in Spring 7). Do not `.block()` on the event loop.
