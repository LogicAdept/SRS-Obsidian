<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Annotations #SRS

# How do you implement a reactive REST controller in WebFlux?

> [!abstract] Short answer
> Annotate a Spring bean with **`@RestController`**, map HTTP methods as in MVC, and **return `Mono` (0..1) or `Flux` (0..N)** — WebFlux subscribes and writes the body through `HttpMessageWriter`. Do **not** call **`.block()`** or **`.subscribe()`** in the handler. Functional **`RouterFunction`** is the other programming model, not this cue.

## Annotated REST, reactive return types

`@RestController` is `@Controller` + class-level `@ResponseBody`: every method writes the body, not a view. Spring Boot *Reactive Web Applications* shows the usual shape — same mapping annotations as MVC, repositories that already return Reactor types:

```java
@RestController
@RequestMapping("/users")
public class UserController {

    private final UserRepository users;
    private final CustomerRepository customers;

    @GetMapping("/{userId}")
    public Mono<User> getUser(@PathVariable Long userId) {
        return this.users.findById(userId);
    }

    @GetMapping("/{userId}/customers")
    public Flux<Customer> getUserCustomers(@PathVariable Long userId) {
        return this.users.findById(userId)
                .flatMapMany(this.customers::findByUser);
    }

    @DeleteMapping("/{userId}")
    public Mono<Void> deleteUser(@PathVariable Long userId) {
        return this.users.deleteById(userId);
    }
}
```

**Listing 1.** Conceptual example from Spring Boot reactive web docs — return the publisher; the framework is the subscriber.

Spring WebFlux *Return Values*: reactive types (Reactor, RxJava, …) are supported **for all** listed return values via `ReactiveAdapterRegistry`. For `Flux`, elements are **streamed as they arrive** (not buffered). `ResponseEntity<Mono<T>>` / `Mono<ResponseEntity<T>>` still work when you need status and headers. SSE uses `Flux<ServerSentEvent<…>>` or `text/event-stream` — [[How do you implement Server-Sent Events in WebFlux]].

WebFlux *Overview*: annotated controllers share `spring-web` mapping annotations with MVC. **Unlike MVC, WebFlux also supports reactive `@RequestBody` arguments.** A `String` return is still a body (REST) or a view name (`@Controller` without `@ResponseBody`).

```d2
direction: right
req: "HTTP request" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
ctrl: "@RestController\nreturns Mono / Flux" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
fw: "HandlerAdapter\nsubscribes" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
out: "HttpMessageWriter\nresponse body" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}

req -> ctrl -> fw -> out
```

**Fig. 1.** You assemble the pipeline; WebFlux subscribes when writing the response. Routing alternative: [[How do you implement functional endpoints in WebFlux]]. Error mapping: [[How do you handle errors in Spring WebFlux]].

> [!warning] Never `.block()` (or subscribe yourself) in the controller
> `block()` occupies an event-loop thread. WebFlux assumes **no blocking** — [[What happens if you call block on a WebFlux event loop]]. Returning `Mono.just(repo.findById(id).block())` is not a reactive controller.

> [!warning] Dropping the publisher does nothing
> If you build a `Mono` and neither return it nor let the framework subscribe, **nothing happens until subscribe**.

> [!warning] `Flux` JSON encoding can commit the response early
> If encoding fails mid-stream, headers may already be sent. `Flux#collectList()` trades memory for a single JSON array when you need a proper error body.

> [!tip] Interview answer
> **`@RestController` plus `@GetMapping` / `@PostMapping`, return `Mono<T>` or `Flux<T>` — same annotations as MVC, reactive body.** WebFlux subscribes and streams the result. Do not block. Functional routers are a second model; reactive `@RequestBody` is a real WebFlux difference from MVC.
