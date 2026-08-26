<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# How do you handle errors in Spring WebFlux?

> [!abstract] Short answer
> **Two layers.** On a `Mono`/`Flux` pipeline, recover with Reactor operators (`onErrorReturn`, `onErrorResume`, `onErrorMap`) — not `try/catch` around deferred work, and not `doOnError` (side-effect only). At the HTTP boundary, annotated controllers use `@ExceptionHandler` / `@ControllerAdvice`; lower in the `WebHandler` chain use `WebExceptionHandler` (Boot: `ErrorWebExceptionHandler`).

## Pipeline recovery (Reactor)

Reactive Streams treat `onError` as **terminal**. An error-handling operator does not resume the original sequence; it **replaces** the failed upstream with a fallback sequence.

Reactor’s *Handling Errors* guide maps try/catch patterns:

| Imperative idea | Operator |
| --- | --- |
| Catch, emit a static default | `onErrorReturn` |
| Catch, switch to another publisher | `onErrorResume` |
| Catch, wrap / change exception type | `onErrorMap` |
| Catch, log, keep the error | `doOnError` (does **not** recover) |
| Retry by re-subscribing | `retry` / `retryWhen` |

```java
@GetMapping("/orders/{id}")
public Mono<Order> getOrder(@PathVariable String id) {
    return orders.findById(id)
            .switchIfEmpty(Mono.error(new OrderNotFoundException(id)))
            .onErrorResume(OrderNotFoundException.class, ex ->
                    catalog.fallbackOrder(id))
            .onErrorMap(TimeoutException.class, ex ->
                    new UpstreamTimeoutException("order lookup", ex))
            .doOnError(ex -> log.warn("order lookup failed: {}", id, ex));
}
```

**Listing 1.** Conceptual controller method: recover or remap on the pipeline; `doOnError` only logs. Returning `Mono`/`Flux` from controllers: [[How do you implement a reactive REST controller in WebFlux]].

`retry(n)` re-subscribes to a **new** upstream sequence after an error; it is not a loop over the failed publisher.

Synchronous `try/catch` around `return orders.findById(id)` does not catch errors that occur **later**, after subscribe — assembly vs execution.

## HTTP mapping (WebFlux)

Spring WebFlux *Exceptions*: `@Controller` and `@ControllerAdvice` may declare `@ExceptionHandler` methods for exceptions from **controller methods**. Matching uses the thrown type or the **immediate cause** of a wrapper. Prefer the exception as a method argument; WebFlux handlers support the same arguments/returns as `@RequestMapping` except request-body / `@ModelAttribute` arguments (the body may already have been consumed). Support is the `@RequestMapping` **`HandlerAdapter`**, not MVC’s `HandlerExceptionResolver` — [[What does the ExceptionHandler annotation do]].

WebFlux *Reactive Core*: exceptions from `WebFilter`s and the target `WebHandler` are handled by **`WebExceptionHandler`** beans (`@Order` / `Ordered`). Built-ins include `ResponseStatusExceptionHandler` and `WebFluxResponseStatusExceptionHandler` (`@ResponseStatus` on the exception type).

Spring Boot *Reactive web*: a `WebExceptionHandler` sits **immediately before** WebFlux’s own handlers; JSON for machine clients, HTML “whitelabel” for browsers. Customize with **`ErrorWebExceptionHandler`** / `AbstractErrorWebExceptionHandler`. RFC 9457 problem details are also an option.

```d2
direction: down
pipe: "Mono/Flux operators\nonErrorReturn / Resume / Map" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
ctrl: "@ExceptionHandler\n@Controller / @ControllerAdvice" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
web: "WebExceptionHandler\n(filters + WebHandler)" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}

pipe -> ctrl: "still error after subscribe"
ctrl -> web: "no handler / filter errors"
```

**Fig. 1.** Recover in the pipeline first; leftover errors become HTTP via controller advice or the WebHandler exception chain.

> [!warning] `doOnError` is not recovery
> It peeks at the error and lets it propagate. Using it instead of `onErrorResume` still fails the request.

> [!warning] `@ControllerAdvice` is not the whole stack
> In WebFlux it cannot handle exceptions that occur **before a handler is selected**. Filters and routing misses belong on `WebExceptionHandler` / Boot’s error web handler.

> [!warning] MVC `ResponseEntityExceptionHandler` is a different stack
> Servlet exception resolvers are not how WebFlux maps errors. Use WebFlux `@ExceptionHandler` return types (including reactive publishers) or a reactive `ErrorWebExceptionHandler`.

> [!tip] Interview answer
> **Recover on the publisher with `onErrorReturn` / `onErrorResume` / `onErrorMap`; `doOnError` only logs.** Map leftover failures to HTTP with `@ExceptionHandler` on the controller or `@ControllerAdvice`. Errors from filters or before handler selection need `WebExceptionHandler` (Boot: `ErrorWebExceptionHandler`). Do not rely on `try/catch` around deferred assembly.
