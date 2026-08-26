<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# How do you implement functional endpoints in WebFlux?

> [!abstract] Short answer
> Use **WebFlux.fn**: a **`HandlerFunction`** (`ServerRequest` → `Mono<ServerResponse>`) plus a **`RouterFunction`** built with **`RouterFunctions.route()`**. Register one or more **`RouterFunction` beans**; Boot/`DispatcherHandler` maps them. This is the **alternative to `@RestController`**, on the same reactive core.

## Handler + router

Spring *Functional Endpoints*: `HandlerFunction` is the body of a `@RequestMapping` method. `RouterFunction` is the mapping — it returns a matching handler or empty `Mono`. Prefer the **`route()` builder** (`GET`/`POST` shortcuts) over hard-to-discover static imports; `RouterFunctions.route(predicate, handler)` is the one-shot form.

```java
public class PersonHandler {

    public Mono<ServerResponse> hello(ServerRequest request) {
        return ServerResponse.ok().bodyValue("Hi, Functional World!");
    }

    public Mono<ServerResponse> getPerson(ServerRequest request) {
        return repository.findById(request.pathVariable("id"))
                .flatMap(person -> ServerResponse.ok()
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(person))
                .switchIfEmpty(ServerResponse.notFound().build());
    }
}

@Bean
public RouterFunction<ServerResponse> personRoutes(PersonHandler handler) {
    return RouterFunctions.route()
            .GET("/hi", handler::hello)
            .GET("/person/{id}", accept(APPLICATION_JSON), handler::getPerson)
            .build();
}
```

**Listing 1.** Conceptual mix of official `bodyValue` hello-world and the `route()` builder / `Mono<ServerResponse>` handlers. Annotated twin: [[How do you implement a reactive REST controller in WebFlux]]. Handler type: [[What is a HandlerFunction in WebFlux]].

`ServerRequest` / `ServerResponse` are **immutable**. Request body via `bodyToMono`/`bodyToFlux`; response body any Reactive Streams `Publisher`.

```d2
direction: right
req: "HTTP request" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
rf: "RouterFunction\nmatch or empty" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
hf: "HandlerFunction\nMono<ServerResponse>" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

req -> rf -> hf
```

**Fig. 1.** `RouterFunctionMapping` discovers beans, `andOther`s them, `HandlerFunctionAdapter` invokes, `ServerResponseResultHandler` writes. Same `DispatcherHandler` as annotated controllers — they can run **side by side**. Nested routes: [[What are router functions in WebFlux]].

Standalone: `RouterFunctions.toHttpHandler(route)`. Typical apps (including Boot WebFlux starter) use WebFlux config + `@Bean RouterFunction`.

> [!warning] Handlers return `Mono<ServerResponse>`
> Completing with a raw `String` is not enough. Build the response (`ok().bodyValue(...)`, `body(publisher, Class)`, `notFound().build()`).

> [!warning] Prefer `route().GET(...)` over mystery statics
> Spring recommends the builder so you do not hunt `RequestPredicates` imports. Both styles are valid.

> [!warning] Not a second HTTP stack
> Functional endpoints still sit on WebFlux’s `WebHandler` / Netty (or Servlet adapter). They are not Spring MVC `RouterFunction` servlet-fn unless you chose that stack.

> [!tip] Interview answer
> **WebFlux.fn: `RouterFunction` routes to a `HandlerFunction` that returns `Mono<ServerResponse>`.** Declare router beans; Boot’s `DispatcherHandler` picks them up. Use `RouterFunctions.route().GET(...).build()`. Same foundation as `@RestController`, different programming model — you own routing as code, not annotations.
