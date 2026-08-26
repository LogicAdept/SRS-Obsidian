<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# What happens if you call block on a WebFlux event loop?

> [!abstract] Short answer
> **`block()` / `blockFirst()` / `blockLast()` (and `toIterable` / `toStream`) wait on the calling thread.** On a thread marked **`NonBlocking`** — Netty’s **`reactor-http-nio-*` workers**, Reactor **`parallel()` / `single()`** — that wait is **forbidden**: Reactor throws **`IllegalStateException`**. Even when it does *not* throw (unmarked servlet thread), you **pin one of the few loop workers** and can **deadlock** if the `Mono` needs that same thread to complete. **Return the publisher** from a controller. `block()` belongs at a **process boundary** (tests, `main`), not on the request loop.

## Forbidden blocking APIs

Reactor *Threading and Schedulers*: `boundedElastic` is for leftover blocking code. **`single` and `parallel` are not.** Blocking APIs on those default schedulers → **`IllegalStateException`**. Custom threads that implement **`NonBlocking`** get the same check (`Schedulers.isInNonBlockingThread()`).

Reactor Netty HTTP workers are that kind of thread. Spring’s WebFlux threading model names them **`reactor-http-nio-`**. A typical message mentions **`block()/blockFirst()/blockLast() are blocking, which is not supported in thread reactor-http-nio-…`**.

```java
@GetMapping("/user/{id}")
public User user(@PathVariable String id) {
    return webClient.get().uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(User.class)
            .block(); // IllegalStateException on Netty request threads
}
```

**Listing 1.** Conceptual anti-pattern. Spring *WebClient Synchronous Use*: **never block in an MVC or WebFlux controller** — **return** the `Mono`/`Flux`. Same for Kotlin: suspend / `Flow`.

```d2
direction: down
ctrl: "Controller on event-loop thread" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
blk: "block() waits" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
stall: "Same worker cannot run\nI/O callbacks / other requests" {
  width: 300
  height: 70
  style.fill: "#fce4ec"
}

ctrl -> blk -> stall
```

**Fig. 1.** The waited HTTP response often **must** be read on that worker — classic **self-deadlock**. Event loop: [[How does the WebFlux event loop work]]. JDBC: [[Why should you not use JDBC on the WebFlux event loop]]. Offload: [[How do you offload blocking work in WebFlux]].

Spring documents **`WebClient` + `.block()`** for **synchronous** clients (scripts, MVC threads that *may* block). That is **not** a Netty controller recipe.

Tests: `@WebFluxTest` / `WebTestClient` **`exchange()`** — no `block()` on a loop thread you own. `StepVerifier` is the unit-test subscribe.

> [!warning] ISE is not guaranteed on every “web” thread
> The throw happens when the **current thread is `NonBlocking`**. WebFlux-on-**Tomcat** may use unmarked servlet threads: `block()` then **hangs** instead of throwing — still an outage.

> [!warning] `toFuture()` is the documented exception among “sync world” operators
> Appendix: other block/iterate APIs throw on non-blocking schedulers; **`Mono.toFuture()`** does not. It still does not make a controller synchronous-safe.

> [!warning] `block()` in `main` / `CommandLineRunner` is a different thread
> Reactor Netty samples use `server.onDispose().block()` on the **startup** thread. Do not copy that into `@GetMapping`.

> [!tip] Interview answer
> **`block()` on a Netty event-loop thread throws `IllegalStateException` (thread is non-blocking) and can deadlock the worker.** Never block in a WebFlux (or MVC) controller — return `Mono`/`Flux`. Use `block()` only at the edge (tests, CLI). Need a blocking library: `subscribeOn(boundedElastic)`, not `block()` on the loop.
