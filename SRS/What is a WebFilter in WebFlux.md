<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS

# What is a `WebFilter` in WebFlux?

> [!abstract] Short answer
> **`WebFilter`** is the **WebHandler-chain interceptor**: **`Mono<Void> filter(ServerWebExchange, WebFilterChain)`**. It runs **before and after** the target **`WebHandler`** (usually **`DispatcherHandler`**). Declare it as a **bean**; order with **`@Order` / `Ordered`**. It is **not** a servlet `Filter`, **not** MVC `HandlerInterceptor`, and **not** WebFlux.fn **`HandlerFilterFunction`**.

## Chain around `webHandler`

Javadoc (since **5.0**): interception-style processing for cross-cutting needs (security, timeouts, …). Kotlin: consider **`CoWebFilter`**.

Spring *Reactive Core*: `WebHttpHandlerBuilder` auto-detects 0..N **`WebFilter`**, 0..N **`WebExceptionHandler`**, one **`webHandler`**.

Boot *Web Filters*: every `WebFilter` bean filters each exchange. **`WebFilterChainProxy` (Spring Security)** default order **`-100`**.

```java
@Component
public class RequestIdFilter implements WebFilter {

    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        String id = UUID.randomUUID().toString();
        exchange.getResponse().getHeaders().add("X-Request-Id", id);
        return chain.filter(exchange);
    }
}
```

**Listing 1.** Conceptual — must **return** `chain.filter(exchange)` (or a completing `Mono`). Dropping the chain `Mono` never reaches the controller. Front controller: [[What is DispatcherHandler in WebFlux]].

```d2
direction: right
f1: "WebFilter" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
f2: "WebFilter" {
  width: 140
  height: 50
  style.fill: "#e3f2fd"
}
dh: "DispatcherHandler" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}

f1 -> f2 -> dh
```

**Fig. 1.** Security’s `WebFilterChainProxy` is one of these filters — [[How does Spring Security work with WebFlux]], [[What is SecurityWebFilterChain]].

| Mechanism | Stack |
| --- | --- |
| **`WebFilter`** | WebFlux `WebHandler` API |
| Servlet **`Filter`** | Servlet container — **do not mix blocking servlet I/O** into WebFlux |
| **`HandlerInterceptor`** | Spring MVC |
| **`HandlerFilterFunction`** | WebFlux.fn only (around a `HandlerFunction`) |

> [!warning] Must subscribe the chain
> `chain.filter(exchange)` is a `Mono`. Ignoring it is a hang/empty response, not a no-op pass-through.

> [!warning] Not a servlet `Filter`
> Spring: mapping servlet filters or using the Servlet API in WebFlux **causes runtime issues**. Use `WebFilter` (or Security’s reactive chain).

> [!warning] `@WebFluxTest` vs Security
> Slice tests **do not** pick up a custom **`SecurityWebFilterChain` `@Bean`** unless you `@Import` it — [[What is the WebFluxTest annotation]].

> [!tip] Interview answer
> **`WebFilter` is WebFlux’s chained interceptor on `ServerWebExchange` — bean + `@Order`.** Security rides it (`WebFilterChainProxy`). Servlet `Filter` / MVC interceptor / `HandlerFilterFunction` are different APIs.

## See also

- [[What is DispatcherHandler in WebFlux]]
- [[What are the main components of Spring WebFlux]]
- [[How does Spring Security work with WebFlux]]
- [[What is SecurityWebFilterChain]]
- [[What is a HandlerFunction in WebFlux]]
- [[How do servlet filters interceptors and AOP differ in Spring]]
- [[What is Spring WebFlux]]
