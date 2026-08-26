<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What are router functions in WebFlux?

> [!abstract] Short answer
> A **`RouterFunction<T>`** maps an incoming **`ServerRequest`** to a **`HandlerFunction<T>`** (usually **`T = ServerResponse`**) or to an **empty `Mono`**. It is the **functional stand-in for `@RequestMapping`**, but it carries **behavior**, not only mapping metadata. Build with **`RouterFunctions.route()`**; register **`@Bean RouterFunction<?>`**. **`RouterFunctionMapping`** finds those beans, **`andOther`s** them in order, and **`DispatcherHandler`** invokes the match. Same stack as `@RestController` — they can run **side by side**.

## Mapping, not the handler body

Javadoc (since **5.0**): `@FunctionalInterface` — *represents a function that routes to a handler function.* `route(ServerRequest)` returns **`Mono<HandlerFunction<T>>`**.

Spring *Functional Endpoints*: prefer the **builder** (`GET`/`POST` shortcuts) over the one-shot `RouterFunctions.route(predicate, handler)` and hard-to-discover static imports.

```java
@Bean
public RouterFunction<ServerResponse> hi(PersonHandler handler) {
    return RouterFunctions.route()
            .GET("/hi", request -> ServerResponse.ok().bodyValue("Hi, Functional World!"))
            .GET("/person/{id}", accept(APPLICATION_JSON), handler::getPerson)
            .build();
}
```

**Listing 1.** Conceptual mix of the dump’s `bodyValue` hello-world and the official `route()` builder. Handler type: [[What is a HandlerFunction in WebFlux]]. How-to: [[How do you implement functional endpoints in WebFlux]].

Dump one-shot is also valid: `RouterFunctions.route(GET("/hi"), req -> ServerResponse.ok().bodyValue(...))`.

```d2
direction: right
req: "ServerRequest" {
  width: 150
  height: 50
  style.fill: "#e3f2fd"
}
rf: "RouterFunction.route\nmatch or empty Mono" {
  width: 240
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

**Fig. 1.** No match → empty `Mono` (try the next composed router). Match → handler builds the delayed response.

## Order, nesting, composition

Routes are **evaluated in declaration order**. Put **specific** paths **before** general ones. That differs from annotated controllers, where Spring picks the **most specific** method.

Compose with **`build()`** (one builder), **`add`**, **`and`**, **`andOther`** (beans of mixed `T`), **`andRoute`**. Share a prefix with **`path("/person", b -> …)`** (type-level `@RequestMapping` analogue). Nest any predicate with **`nest(accept(JSON), …)`**.

Boot / WebFlux Config infrastructure:

- **`RouterFunctionMapping`** — discover beans, order, `andOther`
- **`HandlerFunctionAdapter`** — `DispatcherHandler` invokes the function
- **`ServerResponseResultHandler`** — `ServerResponse.writeTo`

Standalone: `RouterFunctions.toHttpHandler(route)`. Typical apps declare **router beans**; Boot’s WebFlux starter wires the mapping.

Dump claim *“`RouterFunction` + `WebFluxConfigurer` under `@EnableWebFlux`”*: the docs **example** implements `WebFluxConfigurer` and declares `@Bean` routers. In **Boot**, keep Boot auto-config — **`WebFluxConfigurer` without `@EnableWebFlux`**. `@EnableWebFlux` is **plain Spring** (or taking **complete control**) — [[What is the EnableWebFlux annotation]]. You do **not** need a configurer **just** to expose a router bean.

> [!warning] First match wins
> A broad `GET("/**")` registered **before** `/person/{id}` steals the request. Bean **`@Order`** / `Ordered` matters across multiple router beans.

> [!warning] Not the whole WebFlux stack
> `RouterFunction` + `HandlerFunction` are **WebFlux.fn**, not “the two main components.” Annotated controllers, [[What is DispatcherHandler in WebFlux]], codecs, and [[What is a WebFilter in WebFlux]] still exist. A dump that lists only the pair is incomplete.

> [!warning] Servlet-fn is a different package
> MVC has `org.springframework.web.servlet.function.RouterFunction`. WebFlux is `…web.reactive.function.server`. Do not mix them in one app’s HTTP stack — [[Can you use Spring MVC and WebFlux in the same application]].

> [!tip] Interview answer
> **`RouterFunction` is WebFlux.fn routing: `ServerRequest` → `Mono<HandlerFunction>`.** Build with `RouterFunctions.route().GET(…).build()`, expose as `@Bean`. Order is first-match; nest with `path`/`nest`. Same `DispatcherHandler` as `@RestController`.

## See also

- [[What is a HandlerFunction in WebFlux]]
- [[How do you implement functional endpoints in WebFlux]]
- [[How do you implement a reactive REST controller in WebFlux]]
- [[What is DispatcherHandler in WebFlux]]
- [[What is the EnableWebFlux annotation]]
- [[How do you configure a WebFlux application]]
- [[What is a WebFilter in WebFlux]]
- [[What is Spring WebFlux]]
- [[What are the main components of Spring WebFlux]]
- [[Can you use Spring MVC and WebFlux in the same application]]
