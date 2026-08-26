<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# How do you call an external API from a WebFlux application?

> [!abstract] Short answer
> Use **`WebClient`**: fluent, **non-blocking**, Reactor-based. Inject Boot’s **`WebClient.Builder`**, `get()`/`post()`, then **`retrieve().bodyToMono` / `bodyToFlux`**. Do **not** use blocking **`RestTemplate`** (or **`RestClient`**) on the WebFlux event loop. Spring Framework 7.0 deprecates `RestTemplate` in favor of `RestClient` for **imperative** apps; reactive/streaming stays **`WebClient`**.

## `WebClient` is the reactive HTTP client

Spring WebFlux *WebClient*: a functional fluent API on Reactor — fully non-blocking, streaming, same codecs as the server. Needs an HTTP library (Reactor Netty by default).

Spring Boot *Calling REST Services*: if you are on WebFlux, **use `WebClient`**. Inject the auto-configured **`WebClient.Builder`** (shares HTTP resources and codecs with the server) rather than a one-off `WebClient.create` in every bean.

```java
@Service
public class RemoteDetailsService {

    private final WebClient webClient;

    public RemoteDetailsService(WebClient.Builder builder) {
        this.webClient = builder.baseUrl("https://example.org").build();
    }

    public Mono<Details> fetch(String name) {
        return this.webClient.get()
                .uri("/{name}/details", name)
                .retrieve()
                .bodyToMono(Details.class);
    }
}
```

**Listing 1.** Conceptual Boot pattern — `retrieve()` then `bodyToMono`. Streaming: `bodyToFlux`. Client vs test client: [[What is the difference between WebClient and WebTestClient]].

Spring *retrieve()*: default 4xx/5xx → `WebClientResponseException`; customize with `onStatus`. Prefer returning the `Mono` from a controller/service — [[How do you implement a reactive REST controller in WebFlux]].

```d2
direction: right
svc: "@Service\nWebClient.Builder" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
wc: "WebClient\nget / retrieve" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
pub: "Mono / Flux\n(no block)" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

svc -> wc -> pub
```

**Fig. 1.** The pipeline is the call; `.block()` on the event loop stalls the server — [[What happens if you call block on a WebFlux event loop]].

`RestClient` is the modern **blocking** fluent client (MVC/imperative). `RestTemplate` is classic blocking; **deprecated as of Spring Framework 7.0**. Both are wrong as the primary client **inside** a reactive WebFlux request unless you offload — [[How do you offload blocking work in WebFlux]].

> [!warning] Prefer `WebClient.Builder` over `WebClient.create` in Boot
> Boot documents sharing connections and codecs through the builder. A raw `create(baseUrl)` per call skips that setup.

> [!warning] `retrieve()` treats 4xx/5xx as errors
> The `Mono` fails with `WebClientResponseException` unless you add `onStatus` (or handle in `onErrorResume`).

> [!warning] Do not `.block()` to “make it simple”
> That is the blocking escape hatch. On Netty event-loop threads it starves other requests.

> [!tip] Interview answer
> **In WebFlux, call HTTP with `WebClient` — inject `WebClient.Builder`, `retrieve().bodyToMono`/`bodyToFlux`.** Return the publisher; do not block. `RestClient`/`RestTemplate` are for imperative stacks; `RestTemplate` is deprecated in Spring 7 in favor of `RestClient`.
