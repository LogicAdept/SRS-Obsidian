<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is a `HandlerFunction` in WebFlux?

> [!abstract] Short answer
> A **`HandlerFunction<T>`** is WebFlux.fn’s **request handler**: **`Mono<T> handle(ServerRequest)`**, usually **`T = ServerResponse`**. It is the **body of a `@RequestMapping` method**. **`RouterFunction`** is the **mapping** (`@RequestMapping` annotation analogue): match → this handler; no match → empty `Mono`. Same reactive core as `@RestController` — not a replacement for `DispatcherHandler`.

## Function, not an annotation

Javadoc (since **5.0**): `@FunctionalInterface` — *represents a function that handles a request.*

Spring *Functional Endpoints*: `ServerRequest` / `ServerResponse` are **immutable**. Bodies use Reactive Streams (`Flux`/`Mono` in, any `Publisher` out).

```java
public Mono<ServerResponse> getPerson(ServerRequest request) {
    return repository.findById(request.pathVariable("id"))
            .flatMap(person -> ServerResponse.ok()
                    .contentType(MediaType.APPLICATION_JSON)
                    .bodyValue(person))
            .switchIfEmpty(ServerResponse.notFound().build());
}
```

**Listing 1.** Conceptual handler method — method reference `handler::getPerson` is a `HandlerFunction`. Routing: [[How do you implement functional endpoints in WebFlux]], [[What are router functions in WebFlux]]. Annotated REST: [[How do you implement a reactive REST controller in WebFlux]].

```d2
direction: down
req: "ServerRequest" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
hf: "HandlerFunction.handle" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
res: "Mono<ServerResponse>" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}

req -> hf -> res
```

**Fig. 1.** The router **chooses** the function; the handler **builds** the delayed response. Do not `.block()` here — [[What happens if you call block on a WebFlux event loop]].

`HandlerFilterFunction` wraps a handler (WebFlux.fn filters), distinct from servlet `Filter` and from **`WebFilter`** on the `WebHandler` chain — [[What is a WebFilter in WebFlux]].

> [!warning] Returning `Mono<Person>` is not enough
> Functional style writes **`ServerResponse`** (status, headers, body). A bare domain `Mono` is the **annotation** model (`@ResponseBody`).

> [!warning] Empty `Mono<ServerResponse>` is not 404 by itself
> Complete the pipeline with **`switchIfEmpty(ServerResponse.notFound().build())`** (or similar). An empty publisher can mean **no response started**.

> [!warning] Not `HandlerFunction` vs `DispatcherHandler`
> `DispatcherHandler` still runs the app. WebFlux.fn is **one programming model** on that core — [[What is DispatcherHandler in WebFlux]].

> [!tip] Interview answer
> **`HandlerFunction` is `ServerRequest` → `Mono<ServerResponse>` — the method body of WebFlux.fn.** `RouterFunction` maps URLs onto those functions, like `@RequestMapping` vs the method. `@RestController` returning `Mono`/`Flux` is the other model on the same stack.
