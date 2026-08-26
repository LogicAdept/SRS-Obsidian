<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is `bodyToMono`?

> [!abstract] Short answer
> **`bodyToMono(Class)`** (or **`ParameterizedTypeReference`**) **decodes one HTTP body** into a **`Mono<T>`** — 0..1 value. On **`WebClient.retrieve()`** that is the **response** body; on **`ServerRequest`** it is the **inbound** body. **`retrieve()` alone does nothing** until this (or `toEntity` / `toBodilessEntity`) runs. **4xx/5xx** fail the `Mono` with **`WebClientException`** unless you add **`onStatus`**. Do **not** `.block()` on the event loop.

## Client `retrieve()` vs server `ServerRequest`

Spring *retrieve()*:

```java
Mono<Person> result = client.get()
        .uri("/persons/{id}", id)
        .accept(MediaType.APPLICATION_JSON)
        .retrieve()
        .bodyToMono(Person.class);
```

**Listing 1.** Conceptual Framework sample — one JSON object. Stream of elements: **`bodyToFlux`** — [[What is bodyToFlux]]. Client: [[What is WebClient]]. How-to: [[How do you call an external API from a WebFlux application]].

`WebClient.ResponseSpec.bodyToMono`: decode to the target type; error status → **`WebClientException`** (typically **`WebClientResponseException`**). Status + body: **`toEntity(Person.class)`**. No body: **`toBodilessEntity()`**. REST Clients: calling **`retrieve()`** with no terminal method is a **no-op**.

Generics (`List<Person>` as **one** JSON array): **`bodyToMono(new ParameterizedTypeReference<List<Person>>() {})`**, not `bodyToMono(List.class)`. A **`Mono<List<T>>`** is still **one** emission; a **`Flux<T>`** is **many**.

WebFlux.fn inbound:

```java
Mono<Person> person = request.bodyToMono(Person.class);
```

**Listing 2.** Conceptual *Functional Endpoints* shortcut for `request.body(BodyExtractors.toMono(Person.class))`. Handler: [[What is a HandlerFunction in WebFlux]].

```d2
direction: right
http: "HTTP body bytes" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
dec: "HttpMessageReader\nbodyToMono" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
mono: "Mono<T>\n(subscribe later)" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}

http -> dec -> mono
```

**Fig. 1.** Decoding starts when something **subscribes**. WebFlux controllers **return** the `Mono`; they do not call **`subscribe()`** or **`block()`**.

> [!warning] Default 4xx/5xx are errors
> `bodyToMono` never delivers the error JSON as `T` unless you **`onStatus`** (or `onErrorResume` on `WebClientResponseException`). Example: treat 404 as empty `Mono`.

> [!warning] `block()` after `bodyToMono` is not the WebFlux path
> It **does** subscribe and wait — fine on a **blocking** thread (tests, CLI). On **`reactor-http-nio-*`** it throws **`IllegalStateException`** — [[What happens if you call block on a WebFlux event loop]].

> [!warning] `subscribe()` in a controller is fire-and-forget
> The framework never sees the `Mono`. Return it so **`DispatcherHandler`** subscribes when writing the response.

> [!tip] Interview answer
> **`bodyToMono` decodes the HTTP body to `Mono<T>` — one object (or one list, with `ParameterizedTypeReference`).** After `WebClient.retrieve()`, or on `ServerRequest` in WebFlux.fn. Return the `Mono`; do not `block()` on the event loop. Many elements: `bodyToFlux`.
