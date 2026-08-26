<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Library/Reactor #SRS

# What are common WebFlux performance mistakes?

> [!abstract] Short answer
> The expensive mistakes are **blocking the event loop** (JDBC, `Thread.sleep`, `synchronized` wait, **`.block()`**), **unbounded buffering** of a hot `Flux`, and **never returning the publisher** so the framework never subscribes. Debug **`Hooks.onOperatorDebug()`** captures a stack on **every operator** — last resort, not production default. Golden rule: **never block a loop worker**; one stall holds every request on that thread.

## Blocking and dropped publishers

Spring *Concurrency Model*: WebFlux assumes you **do not block**. Offload is an escape hatch — [[How do you offload blocking work in WebFlux]], [[Why should you not use JDBC on the WebFlux event loop]].

`.block()` / `blockFirst()` on **`reactor-http-nio-*`** → **`IllegalStateException`** (or a hang on some servlet adapters) — [[What happens if you call block on a WebFlux event loop]].

Reactor: **nothing runs until subscribe**. In a controller, **return** the `Mono`/`Flux` so `DispatcherHandler` subscribes. A service that calls `repository.save(entity)` and **drops** the `Mono` never writes. That is not “async fire-and-forget”; it is a no-op until someone subscribes.

```java
@GetMapping("/user/{id}")
public Mono<User> user(@PathVariable String id) {
    return webClient.get().uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(User.class); // return; do not block() or subscribe()
}
```

**Listing 1.** Conceptual — the framework is the subscriber.

## Backpressure, debug hooks, state

Spring: if a publisher **cannot slow down**, it must **buffer, drop, or fail**. Unbounded `onBackpressureBuffer()` / ignoring demand → **OOM**. `limitRate(n)` **batches demand**; it is not a magic DB pager. Cap buffers at the **hot** boundary — [[How does Spring WebFlux handle backpressure]].

Reactor *Debugging*: `Hooks.onOperatorDebug()` is the **easiest and slowest** mode (stack on every operator). Prefer **`checkpoint()`** or the **Reactor debug agent**. Activate global debug **in a controlled way, as a last resort**.

Spring: **inside one reactive pipeline**, stages run sequentially — you do not lock for that. **Shared mutable fields on a singleton** across requests are still a race. Dump “shared mutable state on the loop” mixes those two.

Context: security/tracing often live in **Reactor `Context`** / Micrometer, not `ThreadLocal` on a Netty worker. Dropping context loses MDC/auth on `publishOn`.

```d2
direction: down
ok: "Return Mono/Flux\nnon-blocking I/O" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
block: "JDBC / sleep / block()\non reactor-http-nio" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
buf: "Hot Flux\nunbounded buffer" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}

ok -> block: "stalls the worker"
ok -> buf: "OOM under load"
```

**Fig. 1.** Event loop: [[How does the WebFlux event loop work]]. Runtime: [[What is Reactor Netty]].

> [!warning] `subscribe()` in a controller is fire-and-forget
> The response is not that subscription. Return the publisher.

> [!warning] `limitRate` is not `@Query(limit)`
> It splits **Reactive Streams demand**. SQL pagination is a **different** knob.

> [!tip] Interview answer
> **Do not block Netty workers, do not `.block()` in a controller, bound hot streams, and return the `Mono`/`Flux` so something subscribes.** Keep `onOperatorDebug` off in production; use checkpoints or the agent.

## See also

- [[How does the WebFlux event loop work]]
- [[What happens if you call block on a WebFlux event loop]]
- [[How do you offload blocking work in WebFlux]]
- [[Why should you not use JDBC on the WebFlux event loop]]
- [[How does Spring WebFlux handle backpressure]]
- [[When should you not use WebFlux]]
- [[What is Reactor Netty]]
